
from flask import Flask, request, Response
import jsonpickle
import platform
import io, os, sys
import pika

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({})".format(rabbitMQHost))

##
## Setup rabbitmq connection
##
def getRMQ():
    rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost)
    )
    rabbitMQChannel = rabbitMQ.channel()

    rabbitMQChannel.queue_declare(queue='toGRPC')
    rabbitMQChannel.queue_declare(queue='toFrontend')
    # topic RMQ example
    rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
    return rabbitMQChannel

infoKey = "{}.frontend.info".format(platform.node())
debugKey = "{}.frontend.debug".format(platform.node())

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

def grpc_request(message, channel):
    print(" [x] Sent {}".format(message))
    output = channel.basic_publish(exchange='', routing_key='toGRPC', body=message)
    print("grpc_request basic_publish output: ", output)

# Initialize Flask application
app = Flask(__name__)

with getRMQ() as rmq:
    log_debug("Creating REST frontend", rmq)
    rmq.close()

@app.route('/sensor/<string:sensor>', methods=['GET'])
def get_sensor(sensor):
    r = request
    rmq = getRMQ()
    log_debug("get_sensor().sensor is {}".format(sensor), rmq)

    # Construct msg to grpc
    try:
        grpc_msg = {
            "sensor": sensor
        }
    except Exception as e:
        log_debug("get_sensor() grpc_msg failed: {}".format(e), rmq)
        return

    grpc_msg_pickled = jsonpickle.encode(grpc_msg)
    log_debug("/sensor/{} => grpc_msg: {}".format(sensor, grpc_msg), rmq)
    grpc_request(grpc_msg_pickled, rmq)
    rmq.close()
    response = {
        'msg': 'OK'
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5000)