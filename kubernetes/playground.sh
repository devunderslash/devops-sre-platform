#!/bin/bash

# set function, e for exit on error, u for exit on unset variable, o for exit on pipefail
set -euo pipefail

# set ENV variables
ARGOCD_NAMESPACE="argocd"
INFRA_NAMESPACE="infra"
VAULT_NAMESPACE="vault"
VSO_NAMESPACE="vault-secrets"
ESO_NAMESPACE="external-secrets"
APPS_NAMESPACE="apps"

# main method
main() {
    # Check if the script is called with an argument
    if [ $# -ne 1 ]; then
        echo "Usage: $0 <action>"
        echo "  Available commands: up, down"
        exit 1
    fi

    action="$1"
    # Check the provided action and perform the corresponding command
    case "$action" in
        "up")
            playground_up
        ;;
        "down")
            playground_down
        ;;
        *)
            echo "Invalid command: $action"
            echo "Available commands: up, down"
            exit 1
        ;;
    esac
}

playground_up() {

    # Check if Docker, Minikube and Helm are installed
    dependencies=(docker minikube helm)
    for dep in "${dependencies[@]}"; do
        assert_command_is_installed "$dep"
    done

    # Check if Docker is running
    assert_docker_is_running

    # Start Minikube
    start_minikube

    # Create the namespaces
    namespaces=($ARGOCD_NAMESPACE $INFRA_NAMESPACE $APPS_NAMESPACE)
    for ns in "${namespaces[@]}"; do
        create_namespace $ns
    done

    # Deploy ArgoCD
    deploy_argocd $ARGOCD_NAMESPACE

    # Helm installs (following params - repo_name repo_url release_name chart_path namespace)
    
    # Install external-secrets 
    helm_install "external-secrets" "https://charts.external-secrets.io" "external-secrets" "external-secrets/external-secrets" $ESO_NAMESPACE 

    # Install Vault
    helm_install "hashicorp" "https://helm.releases.hashicorp.com" "vault"  "hashicorp/vault" $VAULT_NAMESPACE

    # Install Vault Secrets Operator
    helm_install "hashicorp" "https://helm.releases.hashicorp.com" "vault-secrets-operator"  "hashicorp/vault-secrets-operator" $VSO_NAMESPACE

    # Vault Operations
    # wait
    wait_for_pod $VAULT_NAMESPACE "vault-0"

    # Init Vault
    initialize_vault $VAULT_NAMESPACE "vault-0" "cluster-keys.json"

    # un-seal vault
    VAULT_UNSEAL_KEY=$(jq -r ".unseal_keys_b64[]" cluster-keys.json)
    unseal_vault $VAULT_NAMESPACE "vault-0" $VAULT_UNSEAL_KEY

    # Setting up Secret backend & role
    VAULT_ROOT_TOKEN=$(jq -r ".root_token" cluster-keys.json)
    configure_vault_backend $VAULT_NAMESPACE "vault-0" $VAULT_ROOT_TOKEN "argocd"

    # Validate Vault
    # Create an example vault secret if it does not exist
    if kubectl -n vault exec -it vault-0 -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=$VAULT_ROOT_TOKEN && vault kv list argocd/ | grep example-secret" >/dev/null;then 
      print_message "example-secret already exists"
    else 
      print_message "creating example-secret in Vault"
      kubectl -n vault exec -it vault-0 -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=$VAULT_ROOT_TOKEN && vault kv put argocd/example-secret foo=bar"
    fi


    # Setup External Secrets Operator
    # Create a secret 'external-secrets/vault-creds.token' for ESO auth.
    if kubectl -n external-secrets get secret vault-creds > /dev/null;then 
      print_message "vault-creds secret already exists in external-secret"
    else 
      print_message "creating vault-creds secret in external-secret"
      kubectl -n external-secrets create secret generic vault-creds --from-literal=token=$VAULT_ROOT_TOKEN
      print_message "vault-creds secret is: $VAULT_ROOT_TOKEN"
    fi


    if kubectl -n $APPS_NAMESPACE get secret vault-creds > /dev/null;then 
      print_message "vault-creds secret already exists in $APPS_NAMESPACE"
    else 
      print_message "creating vault-creds secret in $APPS_NAMESPACE"
      kubectl -n $APPS_NAMESPACE create secret generic vault-creds --from-literal=token=$VAULT_ROOT_TOKEN
    fi

    if kubectl -n $INFRA_NAMESPACE get secret vault-creds > /dev/null;then 
      print_message "vault-creds secret already exists in $INFRA_NAMESPACE"
    else 
      print_message "creating vault-creds secret in $INFRA_NAMESPACE"
      kubectl -n $INFRA_NAMESPACE create secret generic vault-creds --from-literal=token=$VAULT_ROOT_TOKEN
    fi

		print_message "setting up external secrets"

    # wait for external-secrets-webhook pod
    es_pod=$(kubectl -n $ESO_NAMESPACE get pod -l 'app.kubernetes.io/name=external-secrets-webhook' -o jsonpath='{.items[0].metadata.name}')
    wait_for_pod "external-secrets" $es_pod

		# wait for es webhook deployment
    kubectl -n $ESO_NAMESPACE rollout status deployment external-secrets-webhook --timeout=120s

    # Create ClusterSecretStore & ExternalSecret
    kubectl -n $ESO_NAMESPACE apply -f eso    

}


# A standard print
print_message() {
  local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  local prefix="[Playgr0und]"
  echo -e "$timestamp $prefix ${@:1}"
}

# Assert a command is installed...
assert_command_is_installed() {
  local command_name="$1"
  print_message "Checking if $command_name is installed."
  if command -v "$command_name" >/dev/null 2>&1; then
    print_message "$command_name is installed."
  else
    print_message "$command_name is not installed."
    exit 1
  fi
}

# Assert Docker is running...
assert_docker_is_running() {
  print_message "Checking if Docker is running..."
  if ! docker info &> /dev/null; then
    echo "Docker is not running. Please start Docker before proceeding."
    exit 1
  else 
    print_message "Docker is running."
  fi
}

# Start Minikube 
start_minikube() {
    if minikube status | grep -q "Running"; then
        print_message "Minikube is running."
    else
        print_message "Minikube is not running."
        print_message "Starting Minikube"
        minikube start --interactive=False > /dev/null
        minikube addons enable ingress > /dev/null
    fi
}

# Create a Namespace
create_namespace() {
    local ns="$1"
    if ! (kubectl get namespace $ns > /dev/null); then 
      print_message "Creating namespace $ns."
      kubectl create namespace $ns > /dev/null
    else
      print_message "$ns already exists"
    fi
}

# Delete a Namespace
delete_namespace() {
  local ns="$1"
    if  (kubectl get namespace $ns > /dev/null); then 
      print_message "Deleting NS $ns"
      kubectl delete namespace $ns > /dev/null
    else
      print_message "$ns does not exist. Nothing to be cleaned up."
    fi

}

# Deploy argoCD from manifest
deploy_argocd(){
    local ns="$1"
    kubectl apply -n $ns -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml >/dev/null
}

helm_install(){
    local repo_name="$1"        # Repo name
    local repo_url="$2"         # Helm Chart repo URL
    local release_name="$3"     # Release name
    local chart_path="$4"       # Helm Chart Name
    local namespace="$5"        # Namespace

    # Check if the release is already installed
    if ! (helm list -n $namespace | grep -q $release_name); then
        print_message "Installing $release_name in $namespace"
        # Add the Helm repo
        helm repo add $repo_name $repo_url >/dev/null
        # Update the Helm repositories
        helm repo update > /dev/null
        # Create the namespace if it doesn't exist
        kubectl create namespace "$namespace" --dry-run=client -o yaml | kubectl apply -f - > /dev/null
        # Install the Helm chart
        helm install $release_name $chart_path -n $namespace >/dev/null
        print_message "$release_name installed in $namespace namespace"
    else
        print_message "$release_name already installed in $namespace namespace"
    fi
}

wait_for_pod() {
  local namespace="${1:-default}"
  local pod_name="$2"
  local polling_interval="${3:-5}"
  local max_wait_time=300  # Maximum wait time in seconds

  local start_time
  start_time=$(date +%s)  # Get the current timestamp in seconds

  # if the pod isn't created yet, give it a couple seconds
  while ! $(kubectl -n $namespace get pods | grep -q $pod_name); do
    echo $pod_name not found, looping 'sleep 2' until found...
    sleep 2
  done

  while true; do
    # Calculate the elapsed time
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if [ "$elapsed_time" -ge "$max_wait_time" ]; then
      print_message "Timeout: Max wait time of $max_wait_time seconds exceeded. Pod $pod_name not scheduled."
      exit 1
    fi

    status=$(kubectl get pod -n $namespace $pod_name -o jsonpath='{.status.phase}')

    if [ "$status" == "Running" ]; then
      print_message "Pod $pod_name scheduled and running."
      break
    elif [ "$status" == "Succeeded" ] || [ "$status" == "Failed" ]; then
      print_message "Pod $pod_name terminated with status: $status."
      break
    elif [ "$status" == "Pending" ]; then
      print_message "Pod $pod_name pending. Waiting to be scheduled..."
    else
      print_message "Pod $pod_name in unknown state: $status. Exiting..."
      exit 1
    fi

    sleep $polling_interval
  done
}

# Vault operations
initialize_vault() {
    local namespace="$1"
    local pod_name="$2"
    local output_file="$3"
    local key_shares=1
    local key_threshold=1

    # Check if already initialized
    if is_vault_initialized "$namespace" "$pod_name"; then
        print_message "$namespace/$pod_name Vault is already initialized."
    else
        print_message "Initializing $namespace/$pod_name Vault."
        kubectl -n $namespace exec -it $pod_name -- vault operator init -key-shares=$key_shares -key-threshold=$key_threshold -format=json > $output_file
        print_message "$namespace/$pod_name Vault initialized."
    fi
}

is_vault_initialized() {
  local namespace="$1"
  local pod_name="$2"

  vault_status_json=$(kubectl -n "$namespace" exec "$pod_name" -- vault status -format=json)
  # Use 'jq' to parse the JSON and check if 'initialized' is 'true'
  initialized=$(echo "$vault_status_json" | jq -r '.initialized')

  if [ "$initialized" == "true" ]; then
    print_message "$namespace/$pod_name" is initiliazed.
    return 0  # Success, Vault is initialized
  else
    print_message "$namespace/$pod_name" is not initiliazed.
    return 1  # Failure, Vault is not initialized
  fi
}

unseal_vault() {
  local namespace="$1"
  local pod_name="$2"
  local unseal_key="$3"

  # Check if Vault is sealed
  if is_vault_sealed "$namespace" "$pod_name"; then
    print_message "$namespace/$pod_name is sealed. Unsealing..."
    kubectl -n "$namespace" exec "$pod_name" -- vault operator unseal "$unseal_key"
    print_message "$namespace/$pod_name Vault unsealed."
  else
    print_message "$namespace/$pod_name Vault is not sealed. No need to unseal."
  fi
}

is_vault_sealed() {
  local namespace="$1"
  local pod_name="$2"

  vault_status_json=$(kubectl -n "$namespace" exec "$pod_name" -- vault status -format=json)
  # Use 'jq' to parse the JSON and check if 'initialized' is 'true'
  sealed=$(echo "$vault_status_json" | jq -r '.sealed')

  if [ "$sealed" == "true" ]; then
    print_message "$namespace/$pod_name" is sealed.
    return 0  # Success, Vault is initialized
  else
    print_message "$namespace/$pod_name" is not sealed.
    return 1  # Failure, Vault is not initialized
  fi
}

configure_vault_backend() {
  local namespace="$1"
  local pod_name="$2"
  local root_token="$3"
  local backend_path="$4"

  # Check if the backend is already configured
  if kubectl exec -it $pod_name -n $namespace -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=$root_token  && vault secrets list | grep $backend_path"; then 
    print_message "Path $backend_path already exists"
  else
    print_message "Enabling secrets"
    kubectl exec -it $pod_name -n $namespace -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=$root_token  && vault secrets enable -path=$backend_path kv-v2"
    print_message "Enabling app role"
    kubectl exec -it $pod_name -n $namespace -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=$root_token  && vault auth enable approle"
    print_message "Create read+list policy for $backend_path"
    kubectl exec -it $pod_name -n $namespace -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=$root_token && echo 'path \"$backend_path/*\" { capabilities = [\"read\", \"list\"] }' | vault policy write $backend_path-read-policy -"

    print_message "Write approle token policy"
    kubectl exec -it $pod_name -n $namespace -- /bin/sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=$root_token && vault write auth/approle/role/$backend_path token_policies=\"$backend_path-read-policy\""
  fi
}



playground_down() {
    # Delete the namespaces
    namespaces=($ARGOCD_NAMESPACE $INFRA_NAMESPACE $APPS_NAMESPACE, $VAULT_NAMESPACE, $ESO_NAMESPACE)
    for ns in "${namespaces[@]}"; do
        delete_namespace $ns
    done
}


# Run the main method
main "$@"