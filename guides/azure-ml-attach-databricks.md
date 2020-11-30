This guide provides step-by-step instructions on attaching Azure Databricks as remote compute for Azure ML. Reference is here: https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/intro-to-pipelines/aml-pipelines-use-databricks-as-compute-target.ipynb (Section 3: Running a Python script in Databricks that currenlty is in local computer)

* Go to Compute --> Attached compute --> New -- Azure Databricks

* Provide a compute name and select the Databricks workspace. Enter the Databricks access token, from Databricks workspace, under User Settings

* You will need a compute instance in Azure ML as well. If you haven't already done so, you can create one under Compute --> Compute instances. See for more details

* Then under Notebooks, you can upload the notebook provided in this repo folder, or copy code from below

```python
dbutils.widgets.text("para", "0.23")
para = dbutils.widgets.get("para")


```

