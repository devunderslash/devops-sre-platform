# CSRE Grafana Observability

This repository contains the Grafana dashboards and alerts modules for observability. Below are detailed instructions on how to manage alerts and test dashboards locally.

Table of Contents
=================

   * [Grafana Observability](#csre-grafana-observability)
      * [Structure and Application](#structure-and-application)
      * [Alerts](#alerts)
         * [Alert Components](#alert-components)
      * [Dashboards](#dashboards)
      * [Test Locally](#test-locally)
      * [FAQ](#faq)
      

## Structure and Application
The deployment directory contains both dashboards and alerts pertaining tothe organisations structure, for example if the org has multiple products, regions, environments and customers. The structure of the deployment directory is as follows:

**product/region/env/customer/**

Under the customer level is where the user can add dashboard and alert groupings which will be the same folder name that is defined in a `<grouping-name_folder.tf>`, for example - devops_folder.tf. This is because Grafana items (dashboards and alerts) can be logically divided into folders. This is done to make it easier to manage and view the items in the Grafana UI.

## Datasources
The datasources are defined at the region level and will be within the common_grafana_assets folder. There can be multiple datasources that can be used by various resources within a region and they can be defined in the datasources.tf file. There are currently 2 datasource types that are supported and they are Prometheus and InfluxDB and modules are defined for these. Follow these instructions to add a new datasource:

1. **Create a new datasource file**: Place it in the appropriate directory under `deployments`, following the structure: `product/region/common_grafana_assets`.

2. **Define the datasource**: Add the datasource `datasources.tf>` to the folder, naming it as desired.

3. **Use the datasource module**: Utilize the module in `modules/grafana-<datasource type>-datasource/main.tf` to correctly populate the datasource parameters. Use other datasources in the deployment directory as a reference.

4. **Create a PR for the datasource**: Create a PR for the datasource and get it reviewed. Merge the PR once approved.

5. **Add secrets to Vault (Example)**: Add the secrets to Vault for the datasource. The secrets are defined in the datasource module. Example:
```bash
vault kv put -mount=<mount_name> product/product-grafana-observability/grafana-datasource-tokens TF_VAR_influxdb_token="test" TF_VAR_prometheus_token="test"
```

6. **Update Pipeline variables**: Update the pipeline variables to include the new datasource secrets to be used in a pipeline (github actions, jenkins, etc).

7. **Merge the PR**: Once the PR is merged, the CI pipeline will automatically apply the Terraform configuration.

8. **View datasources**: Once the apply is successful, you can view the datasources in your Grafana instance.


## Alerts
The alerts leverage a module defined in the `modules/grafana-alerts` directory. Ensure you use this module when creating new alerts. Follow these steps to add a new alert:

1. **Create a new alert file**: Place it in the appropriate directory under `deployments`, following the structure: `product/region/environment/customer/alert_grouping_folder`.

2. **Add a new folder (if needed)**: If a new grouping folder is required, add the folder under the customer directory and add the folder name to a new tf file under this directory - `<dashboard/alert_name>_folder.tf`. Also, include `local_vars.tf` if needed.

3. **Define the alert**: Add the alert `<alert_name_alerts.tf>` to the folder, naming it as desired.

4. **Use the alert module**: Utilize the module in `modules/grafana-alert/main.tf` to correctly populate the alert parameters. Use other alerts in the deployment directory as a reference.

5. **Create a PR for the alert**: Create a PR for the alert and get it reviewed. Merge the PR once approved.

6. **The CI pipeline will automatically apply the Terraform configuration**: Once the PR is merged, the CI pipeline will automatically apply the Terraform configuration.

7. **View alerts**: Once the apply is successful, you can view the alerts in your Grafana instance.

### Alert Components
With Grafana alerts there is common assets required for the alerts to use. These common assets are added within the region directory and contain items that the alerts require in order to work such as contact_points, notification_policy and notification_templates. This will allow the alerts to get a message to a contact point, whilst informing of the correct level of severity and also make use of reusable message formats.

## Dashboards

Create the dashboard in Grafana and export it as a json. We need to persist the dashboards hence, we add them on this repo under the respective product folders. We follow this folder structure: `product/region/environment/customer/<grafana_folder>/dashboards_json`. To add a new dashboard, follow these steps:

1. **Create a new dashboard file**: As it is a Visual construct it is best to create the dashboard in Grafana and then export it to a json file. Place the json file in the appropriate directory under `deployments`, following the structure: `product/region/environment/customer/<grafana_folder>/dashboards_json`.

2. **Add a new folder (if needed)**: If a new grouping folder is required, add the folder under the customer directory and add the folder name to a new tf file under this directory - `<grafana_folder_name>_folder.tf` as we can see [here](TODO - add example for folder). Also, include `local_vars.tf` file ([example](TODO - add variables example)) for common variables if needed.

3. **Define the dashboard**: Add the dashboard to the `dashboards_json` folder, naming it as desired. Example:

![Dashboard Example](resources/dashboards.png)

4. **Add the dashboard to the dashboards.tf file**: Create an entry in the dashboards.tf to point to the location of the dashboard json ([sample](TODO, add example)) and also the folder that it belongs to and the dashboard module takes care of the rest.

5. **Create a PR for the dashboard**: Create a PR for the dashboard and get it reviewed. Merge the PR once approved.

6. **The CI pipeline will automatically apply the Terraform configuration**: Once the PR is merged, the CI pipeline will automatically apply the Terraform configuration.

7. **View dashboards**: Once the `apply` job is successful, you can view the dashboards in your Grafana instance.



## Test Locally

You will need the following tools to test the dashboards locally:
- Docker
- Terraform

To test the dashboards locally, follow these steps:

1. **Run a local Grafana instance using Docker**:
   ```bash
   docker run -d -p 3000:3000 --name=grafana -e "GF_INSTALL_PLUGINS=grafana-piechart-panel,grafana-worldmap-panel" grafana/grafana
   ```
2. **Access Grafana**: Open your browser and navigate to [http://localhost:3000](http://localhost:3000).

3. **Login**: Use the credentials:
   - Username: `admin`
   - Password: `admin`

4. **Generate a new API key**: This will be used for authentication.

5. **Set the environment variables**: Set the following environment variables:
   ```bash
   export GRAFANA_AUTH=<grafana_service_token>
   export GRAFANA_URL=http://localhost:3000
   ```

6. **Set secrets used by any Datasources added**: Set the secrets in the environment variables if you have added datasources. For example:
   ```bash
   export TF_VARS_prometheus_token=<password>
   export TF_VARS_influxdb_token=<password>
   ```

7. **Comment out the backend section in the provider.tf file**: This is to ensure that the local Grafana instance is used.

8. **Apply the Terraform configuration**: Run the Terraform apply command:
   ```bash
   cd deployments/product/region
   terraform apply
   ```
9. **View dashboards**: Once the apply is successful, you can view the dashboards in your local Grafana instance.

By following these steps, you can effectively manage and test Grafana alerts and dashboards for observability.


## Creating a New Pipeline (General steps)
To create a new pipeline, follow these steps:

1. **Create S3 bucket**: Create an S3 bucket to store the Terraform state files. This will reside in the bucket named `org-terraform-state-management-<region>`. For example `org-terraform-state-management-useast1`. Ensure tht there is also a product bucket inside this bucket. For example `org-terraform-state-management-useast1/product`.

2. **Define the pipeline**: Generally for pipelines it would be ideal to have a single pipeline with the ability to inject different variables for different regions 


4. **Confirm variables and secrets are available in your secret manager**: Ensure that the variables are available in Vault/ SSM Param Store/ Other secret store.

6. **Trigger the pipeline**: Trigger pipeline for first run


## FAQ
- Why is the common assets folder containing the contact_points and notification_policies not set at the environment level?
  - This is due to a limitation with the default policy under the grafana-default-email which is a singular resource that can only be set once. This seems to be a limitation of Grafana currently and so we have to set this at the region level. This is also the same for the contact_points as they are used in the notification_policy. Therefore the environment level contact points and policies for all environments are set at the region level (uat, prod in us-east-1 for example).

- Why can't I just use the Terraform provider for Grafana to create Dashboards, you know like DataDog?
  - This is due to the fact that the Grafana provider for Terraform is not as mature as the DataDog provider. The Grafana provider is just not as good and I very much welcome anyone to build a module to do this for us. 

- How should I create dashboards in Grafana then?
   - The best way to create dashboards is to create them in Grafana and then export them as a json file. This json file can then be added to the repository and Terraform will take care of the rest. This seems to be the industry standard way of doing this and is the best way to manage dashboards in Grafana currently.

## Resources
- [Grafana API](https://grafana.com/docs/grafana/latest/http_api/)
- [Terraform Provider](https://registry.terraform.io/providers/grafana/grafana/latest/docs)
- [Prebuilt dashboards](https://logit.io/blog/post/top-grafana-dashboards-and-visualisations/)

## TODO:
- Add examples for module folder
- Add README for the modules
- Add versioning to the modules
