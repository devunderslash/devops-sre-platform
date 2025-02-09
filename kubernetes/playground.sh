#!/bin/bash

# set function, e for exit on error, u for exit on unset variable, o for exit on pipefail
set -euo pipefail

# set ENV variables
ARGOCD_NAMESPACE="argocd"
INFRA_NAMESPACE="infra"
VAULT_NAMESPACE="vault"
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


playground_down() {
    # Delete the namespaces
    namespaces=($ARGOCD_NAMESPACE $INFRA_NAMESPACE $APPS_NAMESPACE, $VAULT_NAMESPACE, $ESO_NAMESPACE)
    for ns in "${namespaces[@]}"; do
        delete_namespace $ns
    done
}


# Run the main method
main "$@"