# usage: python3 grpc-client.py [h/t/p]
# h = humidity
# t = temp
# p = pressure

import grpc
import argparse
import logging

import dsc_pb2
import dsc_pb2_grpc

rpi_addr = "10.0.0.75"

parser = argparse.ArgumentParser(description='gRPC client')
parser.add_argument('sensor', type=str, help='sensor type: h, t, or p')
args = parser.parse_args()

def humidity(stub):
    response = stub.Humidity(dsc_pb2.humidityMsg(h=1))

def temp(stub):
    response = stub.Temp(dsc_pb2.tempMsg(t=1))

def pressure(stub):
    response = stub.Pressure(dsc_pb2.pressureMsg(p=1))

def run():
    with grpc.insecure_channel('{}:50051'.format(rpi_addr)) as channel:
        stub = dsc_pb2_grpc.DscStub(channel)
        if args.sensor == 'h':
            humidity(stub)
        elif args.sensor == 't':
            temp(stub)
        elif args.sensor == 'p':
            pressure(stub)

if __name__ == '__main__':
    logging.basicConfig()
    run()
