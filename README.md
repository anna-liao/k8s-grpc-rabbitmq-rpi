# IoT Raspberry Pi Kubernetes

This project demonstrates the use of Kubernetes, REST API, gRPC, and RabbitMQ to get sensor measurements from a sensor board installed on a Raspberry Pi.

![System Diagram](dsc_sysdiag.pdf?raw=true "System Diagram")

To run project:
```
make deploy-k8s
kubectl logs -f <logs-pod>
bash rest-grpc/sample-get.sh
```
