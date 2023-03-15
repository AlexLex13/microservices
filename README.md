A microservice application for generating an audio file from a video. The following services are implemented: authorization, gateway, converter, auth. Messaging between them is implemented using RabbitMQ. Each service is deployed in a Docker-container, which are managed with the help of Kubernetes.