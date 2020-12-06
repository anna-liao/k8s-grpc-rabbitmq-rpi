##
from flask import Flask, request, Response
import jsonpickle
import base64
import pickle
import platform
import io, os, sys
import pika, redis
import hashlib, requests

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

##
## Set up redis connections
##
# k: img_name, v: img_hash
redisNameToHash = redis.Redis(host=redisHost, db=1)
# k: img_hash, set: origin name or url of image
redisHashToName = redis.Redis(host=redisHost, db=2)

# k: img_hash, set: list or set of facerec data for image
redisHashToFaceRec = redis.Redis(host=redisHost, db=3)
# k: img_hash, set: set of images containing matching faces
redisHashToHashSet = redis.Redis(host=redisHost, db=4)

##
## Setup rabbitmq connection
##
def getRMQ():
    rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost)
    )
    rabbitMQChannel = rabbitMQ.channel()

    rabbitMQChannel.queue_declare(queue='toWorker')
    # topic RMQ example
    rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
    return rabbitMQChannel

infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())

def log_debug(message, channel, key=debugKey):
    print("DEBUG:", message, file=sys.stderr)
    # May want to check return error code of basic_publish()
    output = channel.basic_publish(exchange='logs', routing_key=key, body=message)
    # print("log_debug basic_publish output: ", output)

def log_info(message, channel, key=infoKey):
    print("INFO:", message, file=sys.stderr)
    # May want to check return error code of basic_publish()
    output = channel.basic_publish(exchange='logs', routing_key=key, body=message)
    # print("log_info basic_publish output: ", output)

def worker_data(message, channel):
    print(" [x] Sent {}".format(message))
    output = channel.basic_publish(exchange='', routing_key='toWorker', body=message)
    print("worker_data basic_publish output: ", output)

# Initialize Flask application
app = Flask(__name__)

with getRMQ() as rmq:
    log_debug("Creating REST frontend", rmq)
    rmq.close()

# /scan/image/filename POST
# Scan picture passed as content of request with specified filename
# Compute hash of contents
# Send hash and image to worker using toWorker rabbitmq exchange
# Worker will add filename to Redis database
# Reponse is JSON: { 'hash' : "abcdef...128" }
@app.route('/scan/image/<string:filename>', methods=['POST'])
def scan_image(filename):
    r = request
    rmq = getRMQ()
    log_debug("scan_image().filename is {}".format(filename), rmq)
    
    # Compute hash of contents
    try:
        imghash = hashlib.sha224(r.data).hexdigest()
        log_debug("scan_image().imghash is {}".format(imghash), rmq)
    except Exception as e:
        log_debug("scan_image(): Error computing hash, {}".format(e), rmq)
        return

    # Serialize image object
    try:
        ser_img = base64.b64encode(r.data).decode('utf-8')
        log_debug("type(ser_img) is {}".format(type(ser_img)), rmq)
    except Exception as e:
        log_debug("serializing img failed: {}".format(e), rmq)
        return 

    # Construct msg to worker
    try:
        worker_msg = {
            "filename": filename,
            "imghash": imghash,
            "ser_img": ser_img
        }
    except Exception as e:
        log_debug("scan_image() worker_msg failed: {}".format(e), rmq)
        return

    worker_msg_pickled = jsonpickle.encode(worker_msg)
    log_debug("/scan/image/{} => worker_msg: {}".format(filename, worker_msg), rmq)
    worker_data(worker_msg_pickled, rmq)    
    
    # Construct REST response
    # hash response to identify provided image for subsequent `match` queries
    response = {
        'hash' : imghash
    }
    log_info("/scan/image/{} => hash = {}".format(filename, imghash), rmq)
    response_pickled = jsonpickle.encode(response)
    rmq.close()
    return Response(response=response_pickled, status=200, mimetype="application/json")

# /scan/url POST
# Request contains json msg with URL specifying image
# { "url" : "http://whatever.jpg" }
# REST server will retrieve image and use URL as filename
@app.route('/scan/<string:url>', methods=['POST'])
def scan_url(url):
    r = request
    rmq = getRMQ()

    # print("scan_url() r.data is {}".format(r.data))
    # print("scan_url() jsonpickle.decode(r.data) is {}".format(jsonpickle.decode(r.data)))

    url = jsonpickle.decode(r.data)["url"]
    log_debug("scan_url(), url is {}".format(url), rmq)
    url_request = requests.get(url, allow_redirects=True)
    # img = open('img', 'wb').write(url_request.content)
    img = url_request.content

    # Compute hash of contents
    try:
        imghash = hashlib.sha224(img).hexdigest()
        print("scan_url().imghash is", imghash)
    except Exception as e:
        log_debug("scan_url(): Error computing hash, {}".format(e), rmq)
        return

    # Serialize image object
    try:
        ser_img = base64.b64encode(img).decode('utf-8')
        print("type(ser_img) is {}".format(type(ser_img)))
    except Exception as e:
        log_debug("serializing img failed: {}".format(e), rmq)
        return 

   # Construct msg to worker
    try:
        worker_msg = {
            "filename": url,
            "imghash": imghash,
            "ser_img": ser_img
        }
    except Exception as e:
        log_debug("scan_url() worker_msg failed: {}".format(e), rmq)
        return

    worker_msg_pickled = jsonpickle.encode(worker_msg)
    log_debug("/scan/url:{} => worker_msg: {}".format(url, worker_msg), rmq)
    worker_data(worker_msg_pickled, rmq)

    # Construct REST response
    # hash response to identify provided image for subsequent `match` queries
    response = {
        'hash' : imghash
    }
    log_info("/scan/url:{} => hash = {}".format(url, imghash), rmq)
    response_pickled = jsonpickle.encode(response)

    rmq.close()

    return Response(response=response_pickled, status=200, mimetype="application/json")

# /match/hash GET
# Input: hash
# Output: list of image name or URL that contains matching faces
#         If hash doesn't match or no faces in image, empty list is returned
@app.route('/match/<string:hashval>', methods=['GET'])
def getMatch(hashval):
    rmq = getRMQ()
    r = request
    status = 200
    try:
        print("hashval is {}".format(hashval))
        items = redisHashToHashSet.smembers(hashval)
        print("items are {}".format(items))
        response = []
        for item in items:
            members = redisHashToName.smembers(item)
            print("members are {}".format(members))
            names = [ x.decode("utf-8") for x in members if x is not None ]
            print("names are {}".format(names))
            response += names
    except redis.RedisError as exp:
        log_debug("Exception retrieving members: {}".format(exp), rmq)
        status = 406

    if redisHashToName.scard(hashval) > 0:
        for item in redisHashToName.smembers(hashval):
            log_debug("redis item: {}".format(item), rmq)
            response += item            

    response_pickled = jsonpickle.encode(response)
    log_info("/match/{} => {}".format(hashval, response_pickled), rmq)
    rmq.close()

    return Response(response=response_pickled, status=200, mimetype="application/json")

# GKE load balancer health check
@app.route('/', methods=['GET'])
def hello():
    return '<h1> Face Rec Server</h1><p> Use a valid endpoint </p>'

# start flask app
app.run(host="0.0.0.0", port=5000)