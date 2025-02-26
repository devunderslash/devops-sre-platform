# Kubernetes Playground
This is a small Kubernetes playground to show how to deploy a simple application to a Kubernetes cluster. This will also show how to use Vault, External Secrets Operator (ESO) and ArgoCD to show how secrets management and GitOps can be used in a project.

## Pre-Requisites
- Docker
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
# Also add any application that you want to access from the host machine, eg:
echo "127.0.0.1 attendance-api.playground.io" | sudo tee -a /etc/hosts
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


```bash
# Add repo
argocd repo add https://github.com/devunderslash/devops-sre-platform.git --username $GITHUB_USERNAME --password $GITHUB_PASSWORD
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

## Postgres
Postgres is deployed via the bitnami helm chart which can be found in the helm_postgres directory. Once it has been deployed by ArgoCD, you can access the Postgres database using the following command:
```bash
# Get the postgres password
kubectl get secret --namespace infra playground-postgres-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d 
kubectl -n infra exec -it playground-postgres-postgresql-0 -- /bin/bash
```

Some useful commands to validate db is running:
```bash
# login to the db
psql -U pguser backend-db # password is in the secret
# list databases
\l
# list tables
\dt
# list users
\du
```

### Example Application
The example application is a simple attendance API that is deployed using the ArgoCD Application resource. The application is a simple REST API that allows you to create, read, update and delete attendance records.

The application is deployed when the ArgoCD playground_appset_list.yaml is applied. The application is deployed to the apps namespace and can be accessed using the following command:
```bash
kubectl -n apps get svc attendance-api
```

The application can be used with some of the following commands:
```bash
curl -X GET http://attendance-api.playground.io/api/players
```
To POST a new player, run the following command:
```bash
curl -X POST http://attendance-api.playground.io/api/players -d '{"id": "1", "name": "John Doe", "dob": "2000-05-15", "joined_group_date": "2023-01-06"}' -H "Content-Type: application/json"
```


### Common Issues

Vault commands with this solution as not accessible from the host machine. To access the vault commands, run the following command:
```bash
    kubectl -n vault exec -it vault-0 -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=<vault-token> && vault kv get argocd/example-secret"
    kubectl -n vault exec -it vault-0 -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=<vault-token> && vault kv list argocd"
```


### References
- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)
- [ArgoCD Deployment Patterns](https://platform.cloudogu.com/en/blog/gitops-repository-patterns-part-6-examples/)
- [Vault](https://www.vaultproject.io/)
- [External Secrets Operator](https://external-secrets.io/latest/provider/kubernetes/)
- [ESO Implementation](https://colinwilson.uk/2022/08/22/secrets-management-with-external-secrets-argo-cd-and-gitops/)

