# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import dsc_pb2 as dsc__pb2


class DscStub(object):
    """rpc Add (addMsg) returns (addReply) {}
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Humidity = channel.unary_unary(
                '/dsc.Dsc/Humidity',
                request_serializer=dsc__pb2.humidityMsg.SerializeToString,
                response_deserializer=dsc__pb2.humidityReply.FromString,
                )
        self.Temp = channel.unary_unary(
                '/dsc.Dsc/Temp',
                request_serializer=dsc__pb2.tempMsg.SerializeToString,
                response_deserializer=dsc__pb2.tempReply.FromString,
                )
        self.Pressure = channel.unary_unary(
                '/dsc.Dsc/Pressure',
                request_serializer=dsc__pb2.pressureMsg.SerializeToString,
                response_deserializer=dsc__pb2.pressureReply.FromString,
                )


class DscServicer(object):
    """rpc Add (addMsg) returns (addReply) {}
    """

    def Humidity(self, request, context):
        """rpc ImageHW (imageMsg) returns (imageReply) {}

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Temp(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Pressure(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DscServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Humidity': grpc.unary_unary_rpc_method_handler(
                    servicer.Humidity,
                    request_deserializer=dsc__pb2.humidityMsg.FromString,
                    response_serializer=dsc__pb2.humidityReply.SerializeToString,
            ),
            'Temp': grpc.unary_unary_rpc_method_handler(
                    servicer.Temp,
                    request_deserializer=dsc__pb2.tempMsg.FromString,
                    response_serializer=dsc__pb2.tempReply.SerializeToString,
            ),
            'Pressure': grpc.unary_unary_rpc_method_handler(
                    servicer.Pressure,
                    request_deserializer=dsc__pb2.pressureMsg.FromString,
                    response_serializer=dsc__pb2.pressureReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dsc.Dsc', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Dsc(object):
    """rpc Add (addMsg) returns (addReply) {}
    """

    @staticmethod
    def Humidity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dsc.Dsc/Humidity',
            dsc__pb2.humidityMsg.SerializeToString,
            dsc__pb2.humidityReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Temp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dsc.Dsc/Temp',
            dsc__pb2.tempMsg.SerializeToString,
            dsc__pb2.tempReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Pressure(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dsc.Dsc/Pressure',
            dsc__pb2.pressureMsg.SerializeToString,
            dsc__pb2.pressureReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
