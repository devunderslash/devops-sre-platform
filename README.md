# DevOps-SRE-Platform-Project

This is a sample project for a DevOps SRE and Platform Engineering practcies. The project takes the applied practices of DevOps, SRE, and Platform Engineering and applies them to a simple project. This ill display the full SDLC of a project from the initial development to the deployment and monitoring of the application. It is split up into various folders and each folder represents a different part of the project. Here is a brief overview of each folder:

- **backend**: This is a sample backend REST API for a team attendance tracker. It is built using Flask. This is to display the Dev elements of a DevOps project. It incorporates up to date practices with the use of SOLID principles, DRY code, and a clean codebase. It also includes tests for the main functionality of the API and instructions as to how to both run the application and the tests simply and easily.

- **containerization**: This directory contains the Dockerfiles and Docker Compose files for containerization of the application.

- **github-actions**: This repository contains the CI/CD pipelines for the repository. Pipelines are defined in the `.github/workflows` directory. The pipelines will undertake multiple jobs such as building application images and running tests.

- **kubernetes**: This directory contains a small K8s setup to run the application in a Kubernetes cluster. It will also run Vault, External Secrets Operator (ESO) and ArgoCD to show how secrets management and GitOps can be used in a project.

- **infrastructure**: This directory contains the Terraform code to deploy the application to AWS. It will display the IaC practices to deploy the application to a simple 3 tier architecture on AWS, with a VPC, Subnets, Security Groups, and EC2 instances. This will be built out to also include an EKS deployment and also an example of a more simpler solution such as Lightsail.

- **monitoring**: This directory contains the monitoring setup for the application. It will include Prometheus and Grafana to show how monitoring can be setup for the application. It will also include a simple alerting setup to show how alerts can be setup for the application.

TODO - Security, testing, and more

## How to follow along
I have designated my commit commits as per the type of work being undertook, here are the mappings:
- DEV - Development work
- DEVOPS - DevOps work
- SRE - SRE work
- PLATFORM - Platform Engineering work
- SEC - Security work
- TEST - Testing work

## Pre-Requisites

- Python 3.6 or higher
- Docker
- Docker Compose
- Kubernetes
- Terraform
- AWS CLI
- Helm
- Kubectl
- Vault
- ArgoCD

## Installation

1. Clone the repository

2. Follow the README in each direction in the order above to setup the application or the infrastructure.

3. Enjoy the project!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- [Paul Devlin] 






