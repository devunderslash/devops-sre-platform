# SECRET_KEY=your_secret_key
# DATABASE_URL="sqlite:///your_database.db"
# SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite3"

#!/bin/bash

# Set the address of your Vault instance
VAULT_ADDR="http://127.0.0.1:8200"

# get VAULT_ROOT_TOKEN env var
VAULT_TOKEN=$(jq -r ".root_token" cluster-keys.json)

 echo "Loading secrets into Vault"

# Function to confirm vault is running
confirm_vault_is_running() {
    # Check if Vault is running
    kubectl -n vault exec -it vault-0 -- /bin/sh -c "export VAULT_ADDR=${VAULT_ADDR} && export VAULT_TOKEN=${VAULT_TOKEN} && vault status"

    # If Vault is not running, exit
    if [ $? -ne 0 ]; then
      echo "Vault is not running. Exiting..."
      exit 1
    fi

    echo "Vault is running"
}

# Function to load secrets from a .env file into Vault
load_secrets() {
#  check .env file exists
    if [ ! -f .env ]; then
        echo "No .env file found. Exiting..."
        exit 1
    fi

    while IFS= read -r line; do
    # set up count
        # Skip empty lines and comments
        if [ -z "$line" ] || [[ "$line" == \#* ]]; then
            echo "Skipping line: ${line}"
            continue
        fi

        # Split the line into path and key-value pairs
        IFS=' ' read -r path key_values <<< "$line"
        echo "Path: ${path}"
        
        # Set the Vault path
        vault_path="argocd${path}"

        # Set the secret values
        secret_values=""
        for key_value in $key_values; do
            secret_values="${secret_values} ${key_value}"
        done

        # Construct the full command
        command="export VAULT_ADDR=${VAULT_ADDR} && export VAULT_TOKEN=${VAULT_TOKEN} && vault kv put ${vault_path} ${secret_values}"
        echo "Executing command: ${command}"

        # Execute the command
        kubectl -n vault exec vault-0 -- /bin/sh -c "${command}"
        wait $!

        echo "Secrets for path ${vault_path} loaded into Vault"
        
    done < .env
}


# Confirm Vault is running, if not exit
confirm_vault_is_running

# Load secrets
load_secrets


echo "Secrets loaded into Vault"