import grpc
import logging

import dsc_pb2
import dsc_pb2_grpc

from sense_hat import sense_hat

class DscServicer(dsc_pb2_grpc.DscServicer):

    def Humidity(self, request, context):
        sense = SenseHat()
        humidity = sense.get_humidity()
        return dsc_pb2.humidityReply(humidity=humidity)

    def Temp(self, request, context):
        sense = SenseHat()
        temp = sense.get_temperature()
        return dsc_pb2.tempReply(temp=temp)

    def Pressure(self, request, context):
        sense = SenseHat()
        pressure = sense.get_pressure()
        return dsc_pb2.pressureReply(pressure=pressure)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dsc_pb2_grpc.add_DscServicer_to_server(
        DscServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()