# Dockerfiles and Docker Compose files for containerization of the application
This directory contains the Dockerfiles and Docker Compose files for containerization of the application.

## Pre-Requisites
- Docker
- Docker Compose

## Straight image build and run with Docker
1. Build the image from dockerfile.backend (**NOTE**: This must be run from the root of the repository):
```bash
docker build -f containerization/Dockerfile.backend -t backend-app .
```

2. Run the container:
```bash
docker run -p 5001:5001 backend-app
```

3. The application should be running on http://127.0.0.1:5001/



