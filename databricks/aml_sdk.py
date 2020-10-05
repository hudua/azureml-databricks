# Databricks notebook source
dbutils.library.installPyPI("azureml-sdk")
dbutils.library.restartPython() 

# COMMAND ----------

import azureml.core
from azureml.core import Workspace, Experiment, Dataset
from azureml.core.authentication import ServicePrincipalAuthentication

#svc_pr_password = os.environ.get("AZUREML_PASSWORD")

svc_pr = ServicePrincipalAuthentication(
  tenant_id="",
  service_principal_id="",
  service_principal_password=""
)

ws = Workspace(
  subscription_id="",
  resource_group="",
  workspace_name="",
  auth=svc_pr
)

# COMMAND ----------

for a in ws.datasets:
  print(a)

# COMMAND ----------


