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

## ArgoCD 
ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes.

- Register repository
```bash
argocd login --core
```

- Set config context
```bash
kubectl config set-context --current --namespace=argocd
```

- Add ArgoCD UI ip to etc/hosts. You can do this for any application that you want to access from the host machine and you have provided and ingress or a load balancer manifest.
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

- Create a developer GITHUB_PASSWORD token in your Github account and export the local environment variable:
```bash
export GITHUB_USERNAME=<username>
export GITHUB_PASSWORD=<password>
```

- Add access to the Github container repository
```bash
kubectl create secret docker-registry ghcr-creds --docker-server=https://ghcr.io --docker-username=$GITHUB_USERNAME --docker-password=$GITHUB_PASSWORD --docker-email=$GITHUB_USERNAME -n argocd
kubectl create secret docker-registry ghcr-creds --docker-server=https://ghcr.io --docker-username=$GITHUB_USERNAME --docker-password=$GITHUB_PASSWORD --docker-email=$GITHUB_USERNAME -n apps
kubectl create secret docker-registry ghcr-creds --docker-server=https://ghcr.io --docker-username=$GITHUB_USERNAME --docker-password=$GITHUB_PASSWORD --docker-email=$GITHUB_USERNAME -n infra
kubectl create secret docker-registry ghcr-creds --docker-server=https://ghcr.io --docker-username=$GITHUB_USERNAME --docker-password=$GITHUB_PASSWORD --docker-email=$GITHUB_USERNAME -n external-secrets
```

## Deploy Infrastructure and Apps
The infrastructure and apps directories represent separate git repositories. The infrastructure repository would contain some basic infrastructure such as databases or caches. The apps repository would contain the applications that would be deployed to the infrastructure. In production environments, these would be separate repositories.

To deploy the infrastructure and apps, run the following commands:

```bash
# Register repository
argocd login --core

# Set config context
kubectl config set-context --current --namespace=argocd

# Add repo
argocd repo add https://github.com/devunderslash/devops-sre-platform
```

## App of Apps Pattern
The App of Apps pattern is a way to manage
- Multiple applications
- Multiple environments
- Multiple clusters

There are two ways of doing this:
1. Using an ArgoCD Application resource and specifying each application in the spec
2. Using an ArgoCD ApplicationSet resource and specifying each application in the spec

This playground uses the ArgoCD ApplicationSet resource to manage the applications and an ArgoCD Application resource to manage the infrastructure such as databases and caches.

To deploy the infrastructure and apps, run the following commands:

```bash
kubectl apply -f config/
```

## Vault
Vault is a tool for securely accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, or certificates.
```bash
# the Playground comes with a single node vault cluster vault/vault-0

# get Vault status
kubectl -n vault exec -it vault-0 -- /bin/sh -c "vault status"

# You can find the Vault token in cluster-keys.json (after you run ./playground.sh up)
```



### Common Issues

Vault commands with this solution as not accessible from the host machine. To access the vault commands, run the following command:
```bash
    kubectl -n vault exec -it vault-0 -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=<vault-token> && vault kv get argocd/example-secret"
    kubectl -n vault exec -it vault-0 -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=<vault-token> && vault kv list argocd"
```


### References
- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)
- [Vault](https://www.vaultproject.io/)
- [External Secrets Operator](https://external-secrets.io/latest/provider/kubernetes/)

