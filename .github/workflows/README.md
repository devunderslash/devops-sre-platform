# Github Actions CI/CD Pipeline
This repository contains the CI/CD pipelines for the repository. Pipelines are defined in the `.github/workflows` directory. The pipelines will undertake multiple jobs such as building application images and running tests.

## Pre-Requisites
- Github Actions
- Act installed locally (Optional)

## Running the CI/CD Pipeline
The CI/CD pipeline will run automatically when a pull request is created if that has been setup, otherwise it can be run manually using "workflow_dispatch:".

### Note
Please ensure you have the following repository settings allowed to create a package:

- Go to the repository settings
- Go to the "Actions" -> "General" tab
- Allow Actions to create and approve Pull Requests

## Standard Operating for Application Pipelines
For the backedn you can see that there is a single pipeline that runs both tests and then builds and signs the image. These would generally be 2 separate pipelines but for the sake of simplicity they are combined. The standard operating procedure for production would be to have a pipeline that runs the tests and then a separate pipeline that builds and signs the image. The image would then be pushed to a registry and then deployed to the environment. The stages at which each is triggered is dependent on the workflow: 
- Tests and vaildation should be run on all PR's and upon merge to main branch when the PR is reviewed and approved. 
- The build and sign of the image should be run upon merge to the main branch and then the deployment should be run upon the image being pushed to the registry.

## Image Signing
For the Image signing step to work you will need to do the following:
- Generate a cosign key pair and add a password
```bash
cosign generate-key-pair
```
- Copy the public key to the repository secrets
- Add the key to the repository secrets as `COSIGN_PUBKEY`

- Copy the private key to the repository secrets
- Add the key to the repository secrets as `COSIGN_KEY`

- Copy the password to the repository secrets
- Add the key to the repository secrets as `COSIGN_PASSWORD`


<!-- image -->
![GH Actions Settings](.github/workflows/gh_actions_settings.png)

TODO:
- Add more details on how to setup the CI/CD pipeline
- Create SAST test using bandit
- Create example for deploying to ECR
