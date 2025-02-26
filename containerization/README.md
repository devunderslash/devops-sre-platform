# Dockerfiles and Docker Compose files for containerization of the application
This directory contains the Dockerfiles and Docker Compose files for containerization of the application.

## Pre-Requisites
- Docker
- Docker Compose

## Straight image build and run with Docker
1. Build the image from dockerfile.backend (**NOTE**: This must be run from the root of the repository):
```bash
# change directory to the root of the repository
cd ..
# build the image
docker build -f containerization/Dockerfile.backend -t backend .
```

2. Run the container:
```bash
docker run -p 5001:5001 backend
```

3. The application should be running on http://127.0.0.1:5001/

## Running with Docker Compose
From the root of the repository, run the following command:
```bash
docker-compose -f containerization/docker-compose.yml up
```

The application should be running on http://127.0.0.1:5001/

To bring down the containers, run:
```bash
docker-compose -f containerization/docker-compose.yml down
```




