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


## Standard Operating for Grafana Observability Pipelines
For the Observability pipelines the attempt here is to display a pipeline that takes inputs from the main workflow and then applies them based on product/region. For example if you were to use a Grafana instance that is in US-EAST-1 for product-1 and contains the prod and uat environments you may have a deployments directory that looks like this:
```
deployments/
├── product-1
│   ├── us-east-1
│   │   |-- main.tf - This would be the main terraform configuration for the region
|   |   |-- prod
|   |   |   |-- main.tf
|   |   |-- uat
|   |   |   |-- main.tf
```
The pipeline would then take the inputs from the main workflow for example:
```
terraform_directory: "observability/grafana/deployments/product-1/us-east-1"
github_token: ${{ secrets.GITHUB_TOKEN }}
aws_region: "us-east-1"
```

This would then be used in the pipeline to apply the terraform configuration to the correct environment. This is a simple example but the idea is to show how you can use the inputs from the main workflow to apply the correct configuration to the correct environment. Ideally the reuasable actions could be in a central repo and used in workflows across the organisation.

## Standard Operating for Application Pipelines
For the backend you can see that there is a single pipeline that runs both tests and then builds and signs the image. These would generally be 2 separate pipelines but for the sake of simplicity they are combined. The standard operating procedure for production would be to have a pipeline that runs the tests and then a separate pipeline that builds and signs the image. The image would then be pushed to a registry and then deployed to the environment. The stages at which each is triggered is dependent on the workflow: 
- Tests and vaildation should be run on all PR's and upon merge to main branch when the PR is reviewed and approved. 
- The build and sign of the image should be run upon merge to the main branch and then the deployment should be run upon the image being pushed to the registry.

### Image Signing
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


![GH Actions Settings](.github/workflows/gh_actions_settings.png)

TODO:
- Add more details on how to setup the CI/CD pipeline
- Create SAST test using bandit
- Create example for deploying to ECR

## Resources
- [Github Actions](https://docs.github.com/en/actions)
- [Reusable Actions](https://medium.com/@gallaghersam95/the-best-terraform-cd-pipeline-with-github-actions-6ecbaa5f3762) 
- [Reusable Actions example](https://github.com/GallagherSam/best-terraform-cd-article/tree/main)
- [Cosign](https://www.civo.com/learn/supply-chain-security)
- [Cosign Implementation](https://github.blog/security/supply-chain-security/safeguard-container-signing-capability-actions/)
- [Cosign Github Action](https://github.com/avisi-cloud/cosign-tutorial/blob/main/.github/workflows/release.yml)
- [Slack integration](https://axolo.co/blog/p/top-4-github-action-slack-integration)
