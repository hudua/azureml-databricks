# Databricks notebook source
dbutils.library.installPyPI("azureml-sdk", version = '1.8.0')
dbutils.library.installPyPI("azureml-train-automl-runtime", version = '1.8.0')
dbutils.library.installPyPI('azure-mgmt-resource', version="10.2.0")
dbutils.library.restartPython() 

# COMMAND ----------

import azureml.core
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml.train.automl import AutoMLConfig
from azureml.train.automl.run import AutoMLRun

import os
import random
import time
import json
import pandas as pd
import numpy as np
import logging

# COMMAND ----------

# MAGIC %md Loading data to Pandas

# COMMAND ----------

df = pd.read_csv('/dbfs/FileStore/shared_uploads/hudua@microsoft.com/sample.csv')

# COMMAND ----------

# MAGIC %md Connecting to Azure ML for AutomML tracking

# COMMAND ----------

secret = dbutils.secrets.get(scope="secrets", key = "spsecret2")

# COMMAND ----------

svc_pr = ServicePrincipalAuthentication(tenant_id="",service_principal_id="",service_principal_password=secret)

# COMMAND ----------

ws = Workspace(
        workspace_name="azure-ml-hudua",
        subscription_id =  "",
        resource_group = "", 
        auth = svc_pr
    )

# COMMAND ----------

print("Found workspace {} at location {}".format(ws.name, ws.location))

# COMMAND ----------

project_folder = './Sample_ML'

if not os.path.isdir(project_folder):
    os.mkdir(project_folder)
    
print('Projects will be created in {}.'.format(project_folder))

# COMMAND ----------

# MAGIC %md now let's do automated ML with Databricks (local) compute

# COMMAND ----------

automl_config = AutoMLConfig(task='classification',                             
                             primary_metric='accuracy',
                             debug_log='automl_ResourceType.log',                    
                             experiment_timeout_minutes=20,
                             training_data=df,
                             label_column_name="class",
                             enable_early_stopping=True,
                             n_cross_validations=5,                             
                             verbosity=logging.INFO
                            )

# COMMAND ----------

experiment_name = 'automl_classification_experiment'

experiment = Experiment(ws, experiment_name)

local_run = experiment.submit(automl_config, show_output=False)
local_run.wait_for_completion()

# COMMAND ----------

best_run, fitted_model = local_run.get_output()
print(best_run)
print(fitted_model)

# COMMAND ----------

# MAGIC %md This is just to study overfitting (so using same training dataset for predictions. In practice, you should divide dataset into train and test)

# COMMAND ----------

X_test

# COMMAND ----------

X_test = df.reset_index(drop=True)
X_test['predictions'] = fitted_model.predict(X_test[['sepal_length','sepal_width','petal_length','petal_width']])

# COMMAND ----------

X_test

# COMMAND ----------


