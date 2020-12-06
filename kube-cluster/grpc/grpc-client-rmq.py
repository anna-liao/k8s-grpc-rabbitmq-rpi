# usage: python3 grpc-client.py [h/t/p]
# h = humidity
# t = temp
# p = pressure

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

def frontend_response(message, channel):
    print(" [x] Sent {}".format(message))
    output = channel.basic_publish(exchange='', routing_key='toFrontend', body=message)
    print("frontend_response basic_publish output: ", output)

def process_msg(msg):
    sensor = msg["sensor"]
    log_debug("sensor: {}".format(sensor), rmq)

    with grpc.insecure_channel('{}:50051'.format(rpi_addr)) as channel:
        stub = dsc_pb2_grpc.DscStub(channel)
        if sensor == 'humidity':
            print("%s %%rH" % humidity(stub))
        elif sensor == 'temp':
            print("%s C" % temp(stub))
        elif sensor == 'pressure':
            print("%s Millibars" % pressure(stub))

def humidity(stub):
    return stub.Humidity(dsc_pb2.humidityMsg(h=1))

def temp(stub):
    return stub.Temp(dsc_pb2.tempMsg(t=1))

def pressure(stub):
    return stub.Pressure(dsc_pb2.pressureMsg(p=1))


rabbitMQ = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitMQHost)
)
rmq = rabbitMQ.channel()
rmq.exchange_declare(exchange='logs', exchange_type='topic')
rmq.queue_declare(queue='toGRPC')
rmq.queue_declare(queue='toFrontend')
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