generate: dsc.proto
	# python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. lab6.proto
	protoc --python_out=. dsc.proto
	python3 -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ dsc.proto

install:
	pip3 install grpcio grpcio_tools futures

clean::
	-rm -f dsc_pb2.py dsc_pb2_grpc.py
	-rm -rf __pycache__
