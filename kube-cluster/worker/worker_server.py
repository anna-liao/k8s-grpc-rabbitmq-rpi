#
# Worker server
#
import pickle
import jsonpickle
import platform
from PIL import Image
import io
import os
import sys
import pika
import redis
import hashlib
import face_recognition
import base64

hostname = platform.node()
infoKey = "{}.worker.info".format(hostname)
debugKey = "{}.worker.debug".format(hostname)

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


# worker_msg = {
#   "filename" : <filename or url>,
#   "imghash" : imghash,
#   "ser_img" : serialized_img
# }

def process_msg(msg):

    filename = msg["filename"]
    imghash = msg["imghash"]
    ser_img = msg["ser_img"]
    log_debug("filename: {}".format(filename), rmq)
    log_debug("imghash: {}".format(imghash), rmq)
    log_debug("ser_img: {}".format(ser_img), rmq)

    try:
        img = base64.b64decode(ser_img)
        ioBuffer = io.BytesIO(img)
    except Exception as e:
        log_debug("process_msg deserialize img failed: {}".format(e), rmq)
        return

    if redisNameToHash.get(filename) is None:
        redisNameToHash.set(filename, imghash)

    # Check if imghash has been scanned already
    if redisHashToFaceRec.scard(imghash) > 0:
        # add the name to the set of origin names/urls for that image
        redisHashToName.sadd(imghash, filename)
        log_info("redisHashToName.sadd({}, {})".format(imghash, filename), rmq)
    else:
        redisHashToName.sadd(imghash, filename) 
        process_img(imghash, ioBuffer)

def process_img(imghash, img_stream):
    log_debug("process_img({})".format(imghash), rmq)
    img = face_recognition.load_image_file(img_stream)
    
    # Extract list of faces in image
    unknown_face_encodings = face_recognition.face_encodings(img)
    # print("face encodings: {}".format(unknown_face_encodings))

    if len(unknown_face_encodings) == 0:
        log_debug("process_img(): No faces detected.", rmq)
        return

    for unknown_face_encoding in unknown_face_encodings:
        log_debug("process_img(), unknown_face_encoding = {}".format(unknown_face_encoding), rmq)

        # Add face and image to Redis
        try:
            redisHashToFaceRec.sadd(imghash, jsonpickle.encode(unknown_face_encoding))
            log_info("redisHashToFaceRec.sadd({}, {})".format(imghash, unknown_face_encoding), rmq) 
        except Exception as e:
            log_debug("ERROR: process_img(), redisHashToFaceRec.sadd(imghash, unknown_face_encoding), {}".format(e), rmq)
            return
        
            # Compare face_encoding to face_encodings for all other images in redisHashToFaceRec 
            # For each image containing any matching face, you would add the images (hashes) of 
            # each image to the other such that eventually we can determine the set of images that contain matching faces.
            #
        try:
            for imgkey in redisHashToFaceRec.keys():
                if type(imgkey) is str:
                    imgkey = imgkey.encode()
                if type(imghash) is str:
                    imghash = imghash.encode()
                if imgkey == imghash:
                   continue 
                for pickled_known_face_encoding in redisHashToFaceRec.smembers(imgkey):
                    known_face_encoding = jsonpickle.decode(pickled_known_face_encoding)
                    match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
                    if len(match_results) > 0:
                        redisHashToHashSet.sadd(imghash, imgkey)
                        log_info("redisHashToHashSet.sadd({}, {})".format(imghash, imgkey), rmq)
                        redisHashToHashSet.sadd(imgkey, imghash)
                        log_info("redisHashToHashSet.sadd({}, {})".format(imgkey, imghash), rmq)
        except Exception as e:
            log_debug("ERROR: process_img() process face_encoding, {}".format(e), rmq)
        
        
    
rabbitMQ = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitMQHost)
)
rmq = rabbitMQ.channel()
rmq.exchange_declare(exchange='logs', exchange_type='topic')
rmq.queue_declare(queue='toWorker')
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    msg = jsonpickle.decode(body)
    print(" [x] Received %r" % msg)
    process_msg(msg)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


rmq.basic_qos(prefetch_count=1)
rmq.basic_consume(queue='toWorker', on_message_callback=callback)

rmq.start_consuming()