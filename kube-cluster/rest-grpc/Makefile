REPO=aliaoco
GRPCBASEIMAGE=dsc-grpc-base
RESTGRPCIMAGE=dsc-rest-grpc

build-base: Dockerfile-grpc-base
	docker build -t $(GRPCBASEIMAGE) -f Dockerfile-grpc-base .
	docker tag $(GRPCBASEIMAGE) $(REPO)/$(GRPCBASEIMAGE)
	docker push $(REPO)/$(GRPCBASEIMAGE)

build: Dockerfile-rest-grpc
	docker build -t $(RESTGRPCIMAGE) -f Dockerfile-rest-grpc .
	docker tag $(RESTGRPCIMAGE) $(REPO)/$(RESTGRPCIMAGE)
	docker push $(REPO)/$(RESTGRPCIMAGE)

run: 
	docker run --rm -it -e RABBITMQ_HOST=10.0.0.100 \
	-v /Users/anna/repos/dsc_project/kube-cluster/rest-grpc/.:/code \
	dsc-rest-grpc /bin/bash

run-kube:
	kubectl apply -f worker-deployment.yaml
