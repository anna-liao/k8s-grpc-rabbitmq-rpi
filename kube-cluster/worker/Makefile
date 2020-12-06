REPO=aliaoco
WORKERIMAGE=lab7-worker

build: Dockerfile-worker
	docker build -t $(WORKERIMAGE) -f Dockerfile-worker .
	docker tag $(WORKERIMAGE) $(REPO)/$(WORKERIMAGE)
	docker push $(REPO)/$(WORKERIMAGE)

run: 
	docker run --rm -it -e REDIS_HOST=10.0.0.100 \
	-e RABBITMQ_HOST=10.0.0.100 \
	-v /Users/anna/repos/lab-7-facerec-kube-anna-liao/worker/.:/code \
	lab7-worker /bin/bash

run-kube:
	kubectl apply -f worker-deployment.yaml
