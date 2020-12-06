# usage: python3 grpc-client.py [h/t/p]
# h = humidity
# t = temp
# p = pressure

from flask import Flask, request, Response
import jsonpickle

import grpc
import argparse
import logging
import pika
import platform
import io, os, sys

import dsc_pb2
import dsc_pb2_grpc

rpi_addr = "10.0.0.75"
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

    # topic RMQ example
    rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
    return rabbitMQChannel

hostname = platform.node()
infoKey = "{}.grpc.info".format(hostname)
debugKey = "{}.grpc.debug".format(hostname)

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

"""
def frontend_response(message, channel):
    print(" [x] Sent {}".format(message))
    output = channel.basic_publish(exchange='', routing_key='toFrontend', body=message)
    print("frontend_response basic_publish output: ", output)
"""

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

    with grpc.insecure_channel('{}:50051'.format(rpi_addr)) as channel:
        stub = dsc_pb2_grpc.DscStub(channel)
        if sensor == 'humidity':
            humidity_reading = humidity(stub) 
            sense_value = "{} %%rH".format(humidity_reading) 
            log_debug(sense_value, rmq)
        elif sensor == 'temp':
            temp_reading = temp(stub)
            sense_value = "{} C".format(temp_reading) 
            log_debug(sense_value, rmq)
        elif sensor == 'pressure':
            pressure_reading = pressure(stub)
            sense_value = "{} Millibars".format(pressure_reading)
            log_debug(sense_value, rmq)

    rmq.close()
    response = {
        'sensor': sensor,
        'value' : sense_value
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

def humidity(stub):
    return stub.Humidity(dsc_pb2.humidityMsg(h=1))

def temp(stub):
    return stub.Temp(dsc_pb2.tempMsg(t=1))

def pressure(stub):
    return stub.Pressure(dsc_pb2.pressureMsg(p=1))

# start flask app
app.run(host="0.0.0.0", port=5000)

""" 
def run():
    with grpc.insecure_channel('{}:50051'.format(rpi_addr)) as channel:
        stub = dsc_pb2_grpc.DscStub(channel)
        if args.sensor == 'h':
            print("%s %%rH" % humidity(stub))
        elif args.sensor == 't':
            print("%s C" % temp(stub))
        elif args.sensor == 'p':
            print("%s Millibars" % pressure(stub))

if __name__ == '__main__':
    logging.basicConfig()
    run()
 """