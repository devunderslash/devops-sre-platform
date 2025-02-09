# Github Actions CI/CD Pipeline
This repository contains the CI/CD pipelines for the repository. Pipelines are defined in the `.github/workflows` directory. The pipelines will undertake multiple jobs such as building application images and running tests.

## Pre-Requisites
- Github Actions

## Running the CI/CD Pipeline
The CI/CD pipeline will run automatically when a pull request is created if that has been setup, otherwise it can be run manually using "workflow_dispatch:".

### Note
Please ensure you have the following repository settings allowed to create a package:

- Go to the repository settings
- Go to the "Actions" -> "General" tab
- Allow Actions to create and approve Pull Requests

<!-- image -->
![GH Actions Settings](.github/workflows/gh_actions_settings.png)

