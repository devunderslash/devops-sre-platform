# Kubernetes Playground
This is a small Kubernetes playground to show how to deploy a simple application to a Kubernetes cluster. This will also show how to use Vault, External Secrets Operator (ESO) and ArgoCD to show how secrets management and GitOps can be used in a project.

## Pre-Requisites
- Kubernetes
- Helm
- Kubectl
- MiniKube

## Installation
A simple bash script has been to do the following:

1. Set Namespaces
2. Ensure required prerequisites are installed (Docker, Helm and Minikube)
3. Checks Docker is running
4. Starts Minikube
5. Creates the namespaces
6. Deploys ArgoCD
7. Installs helm charts for Vault and ESO
8. Initialize and unseal Vault

To run the script, run the following command:
```bash
./playground.sh up
```

To tear down the playground, run the following command:
```bash
./playground.sh down
```

Then run minikube stop to completely stop the minikube cluster.
```bash
minikube stop
```

## Deploy Infrastructure and Apps
To deploy the infrastructure and apps, run the following command:

TODO - Add stuff here

## ArgoCD 
ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes.

- Register repository
argocd login --core

- Set config context
kubectl config set-context --current --namespace=argocd

- Add ArgoCD UI ip to etc/hosts
```bash
echo "127.0.0.1 argocd.playground.io" | sudo tee -a /etc/hosts
```

- Run minikube tunnel
```bash
minikube tunnel
```

- Open ArgoCD UI
```bash
http://argocd.playground.io
```

- Login with the following credentials:
```bash
# The default username is 'admin' and password is stored as a secret which can be retrieved using:
kubectl -n argocd get secret argocd-initial-admin-secret  --template={{.data.password}} | base64 --decode
```

- Add the application to ArgoCD
```bash

