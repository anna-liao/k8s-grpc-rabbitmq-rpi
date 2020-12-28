# IoT Raspberry Pi Kubernetes

This project demonstrates the use of Kubernetes, REST API, gRPC, and RabbitMQ to get sensor measurements from a sensor board installed on a Raspberry Pi.

![System Diagram](https://github.com/anna-liao/k8s-grpc-rabbitmq-rpi/blob/main/dsc_sysdiag.pdf)

To run project:
make deploy-k8s
kubectl logs -f <logs-pod>
bash rest-grpc/sample-get.sh