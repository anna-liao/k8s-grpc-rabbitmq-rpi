##
## You provide this to build and push your docker images
##

REPO=aliaoco
RESTIMAGE=lab7-rest
LOGSIMAGE=lab7-logs

# Usage: make build-rest
build-rest: Dockerfile-rest
	docker build -t $(RESTIMAGE) -f Dockerfile-rest .
	docker tag $(RESTIMAGE) $(REPO)/$(RESTIMAGE)
	docker push $(REPO)/$(RESTIMAGE)

# Usage: make build-logs
build-logs: Dockerfile-logs
	docker build -t $(LOGSIMAGE) -f Dockerfile-logs .
	docker tag $(LOGSIMAGE) $(REPO)/$(LOGSIMAGE)
	docker push $(REPO)/$(LOGSIMAGE)

run-logs: .env
	docker run --rm --env-file=.env -it aliaoco/lab7-logs bash

run-test: 
	docker run --rm -it -e REDIS_HOST=10.0.0.100 \
	-e RABBITMQ_HOST=10.0.0.100 \
	-v /Users/anna/repos/lab-7-facerec-kube-anna-liao/rest/.:/code \
	aliaoco/lab7-rest bash

run: rest-deployment.yaml \ 
	rest-service.yaml \
	rest-ingress.yaml \
	logs-deployment.yaml
	kubectl apply -f rest-deployment.yaml
	kubectl apply -f rest-service.yaml
	kubectl apply -f logs-deployment.yaml
	kubect apply -f rest-ingress.yaml

clean:
	kubectl delete deploy rest
	kubectl delete svc rest
	kubectl delete deploy logs
	kubectl delete ingress lab7-ingress
	sleep 5
	kubectl get po