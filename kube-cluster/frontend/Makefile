##
## You provide this to build and push your docker images
##

REPO=aliaoco
FRONTENDIMAGE=dsc-frontend
LOGSIMAGE=dsc-logs

# Usage: make build-rest
build-frontend: Dockerfile-frontend
	docker build -t $(FRONTENDIMAGE) -f Dockerfile-frontend .
	docker tag $(FRONTENDIMAGE) $(REPO)/$(FRONTENDIMAGE)
	docker push $(REPO)/$(FRONTENDIMAGE)

# Usage: make build-logs
build-logs: Dockerfile-logs
	docker build -t $(LOGSIMAGE) -f Dockerfile-logs .
	docker tag $(LOGSIMAGE) $(REPO)/$(LOGSIMAGE)
	docker push $(REPO)/$(LOGSIMAGE)

run-logs: .env
	docker run --rm --env-file=.env -it aliaoco/lab7-logs bash

run-frontend: 
	docker run --rm -it -e RABBITMQ_HOST=10.0.0.100 \
	-v /Users/anna/repos/dsc_project/kube-cluster/frontend/.:/code \
	aliaoco/dsc-frontend bash

deploy: logs-deployment.yaml \
	../rabbitmq/rabbitmq-service.yaml ../rabbitmq/rabbitmq-deployment.yaml \
	frontend-deployment.yaml frontend-service.yaml frontend-ingress.yaml 
	kubectl apply -f frontend-ingress.yaml
	kubectl apply -f frontend-service.yaml
	kubectl apply -f ../rabbitmq/rabbitmq-service.yaml
	sleep 15
	kubectl apply -f ../rabbitmq/rabbitmq-deployment.yaml
	kubectl apply -f frontend-deployment.yaml
	kubectl apply -f logs-deployment.yaml
	# kubectl port-forward --address 0.0.0.0 service/rabbitmq 5672:5672 &
	# ps augxww | grep port-forward

deploy-frontend: frontend-deployment.yaml frontend-service.yaml frontend-ingress.yaml 
	kubectl apply -f frontend-deployment.yaml
	kubectl apply -f frontend-service.yaml
	kubectl apply -f frontend-ingress.yaml

clean:
	kubectl delete deploy frontend &
	kubectl delete svc frontend &
	kubectl delete deploy logs &
	kubectl delete ingress frontend-ingress &
	kubectl delete svc rabbitmq &
	kubectl delete deploy rabbitmq &