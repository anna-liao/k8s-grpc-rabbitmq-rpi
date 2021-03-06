generate-proto: dsc.proto
	# python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. lab6.proto
	protoc --python_out=. dsc.proto
	python3 -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ dsc.proto

install:
	pip3 install grpcio grpcio_tools futures

clean-proto:
	-rm -f dsc_pb2.py dsc_pb2_grpc.py
	-rm -rf __pycache__

deploy-k8s: rest-grpc/frontend-deployment.yaml rest-grpc/frontend-service.yaml \
	rest-grpc/frontend-ingress.yaml \
	rest-grpc/logs-deployment.yaml \
	rabbitmq/rabbitmq-service.yaml rabbitmq/rabbitmq-deployment.yaml
	kubectl apply -f rest-grpc/frontend-ingress.yaml	
	kubectl apply -f rest-grpc/frontend-service.yaml
	kubectl apply -f rabbitmq/rabbitmq-service.yaml
	sleep 15
	kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
	kubectl apply -f rest-grpc/frontend-deployment.yaml
	kubectl apply -f rest-grpc/logs-deployment.yaml
	# kubectl logs -f <logs-pod>

clean-k8s:
	kubectl delete deploy frontend &
	kubectl delete svc frontend &
	kubectl delete ingress frontend-ingress &
	kubectl delete deploy logs &
	kubectl delete deploy rabbitmq &
	kubectl delete svc rabbitmq &