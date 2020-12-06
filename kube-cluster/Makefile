# To run project:
# make deploy
# kubectl logs -f <logs-pod>
# bash rest-grpc/sample-get.sh

deploy: rest-grpc/frontend-deployment.yaml rest-grpc/frontend-service.yaml \
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

clean:
	kubectl delete deploy frontend &
	kubectl delete svc frontend &
	kubectl delete ingress frontend-ingress &
	kubectl delete deploy logs &
	kubectl delete deploy rabbitmq &
	kubectl delete svc rabbitmq &

deploy-v1: frontend/frontend-deployment.yaml frontend/frontend-service.yaml \
	frontend/frontend-ingress.yaml \
	frontend/logs-deployment.yaml \
	grpc/grpc-deployment.yaml \
	rabbitmq/rabbitmq-service.yaml rabbitmq/rabbitmq-deployment.yaml
	kubectl apply -f frontend/frontend-ingress.yaml	
	kubectl apply -f frontend/frontend-service.yaml
	kubectl apply -f rabbitmq/rabbitmq-service.yaml
	sleep 15
	kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
	kubectl apply -f frontend/frontend-deployment.yaml
	kubectl apply -f frontend/logs-deployment.yaml
	kubectl apply -f grpc/grpc-deployment.yaml
	# kubectl logs -f <logs-pod>

clean-v1:
	kubectl delete deploy frontend &
	kubectl delete svc frontend &
	kubectl delete ingress frontend-ingress &
	kubectl delete deploy logs &
	kubectl delete deploy grpc-client &
	kubectl delete deploy rabbitmq &
	kubectl delete svc rabbitmq &
