REPO=aliaoco
GRPCBASEIMAGE=dsc-grpc-base
GRPCIMAGE=dsc-grpc

build-base: Dockerfile-grpc-base
	docker build -t $(GRPCBASEIMAGE) -f Dockerfile-grpc-base .
	docker tag $(GRPCBASEIMAGE) $(REPO)/$(GRPCBASEIMAGE)
	docker push $(REPO)/$(GRPCBASEIMAGE)

build: Dockerfile-grpc
	docker build -t $(GRPCIMAGE) -f Dockerfile-grpc .
	docker tag $(GRPCIMAGE) $(REPO)/$(GRPCIMAGE)
	docker push $(REPO)/$(GRPCIMAGE)

run: 
	docker run --rm -it -e RABBITMQ_HOST=10.0.0.100 \
	-v /Users/anna/repos/dsc_project/kube-cluster/grpc/.:/code \
	dsc-grpc /bin/bash

run-kube:
	kubectl apply -f worker-deployment.yaml
