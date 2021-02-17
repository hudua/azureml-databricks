# Overview

This deployment creates:

1. Networking
    * **Virtual Network** - Creates a network isolate for this demo environment
    * **Bastion + Public IP** - Provides secure access to virtual machines without any public IPs attached to any VM
    * **NAT Gateway + Public IP** - [Required for Azure Databricks No Public IP configuration](https://docs.microsoft.com/en-us/azure/databricks/security/secure-cluster-connectivity)
    * **Network Security Groups (NSGs)** - Required for controlling inbound and outbound network traffic
2. Data
    * **Azure Data Lake Gen 2 + Private Endpoints**
3. Compute
    * **Azure Databricks**
    * **Windows 2019 VM [used for testing]**


# Bicep

Bicep is a Domain Specific Language (DSL) for deploying Azure resources declaratively. It aims to drastically simplify the authoring experience with a cleaner syntax and better support for modularity and code re-use. Bicep is a transparent abstraction over ARM and ARM templates, which means anything that can be done in an ARM Template can be done in bicep (outside of temporary known limitations). All resource types, apiVersions, and properties that are valid in an ARM template are equally valid in Bicep on day one.

Bicep compiles down to standard ARM Template JSON files, which means the ARM JSON is effectively being treated as an Intermediate Language (IL).

# Installation

1. Install Bicep - https://github.com/Azure/bicep/blob/main/docs/installing.md

2. Install Azure CLI - https://docs.microsoft.com/en-us/cli/azure/install-azure-cli


# Deployment

Create an Azure Resource Group

```bash
az group create -n testml -l canadacentral
```

Compile Bicep to ARM template

```bash
bicep build env.bicep
```

Deploy ARM Template

```bash
az deployment group create --template-file env.json -g testml
```