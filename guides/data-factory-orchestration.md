This guide provides documentation on how to set up automatically scheduling of Databricks job through Azure Data Factory through trigger with file creation in storage account.

#### Job parameterization with Azure Databricks

You can use widgets in Databricks to set up parameterization. More details here: https://docs.microsoft.com/en-us/azure/databricks/notebooks/widgets

```python
dbutils.widgets.text("para", "0.23")
para = dbutils.widgets.get("para")
```

Once you have a notebook, e.g. with parameterization, ready to go, you can go to the Azure Data Factory workspace.

#### Azure Data Factory linked service

First, create an Azure Databricks linked service in Azure Data Factory:

* Create a new linked service
* You can select the relevant Databricks service and get the token here
* Test the connection and then save

#### Azure Data Factory pipeline of Databricks notebook

Second, create a pipeline with Databricks run notebook:

* Create a new pipeline
* Select the Databricks - Notebook option and drag it to the designer
* You can select the notebook you want to run
* There is option for you to manually specify parameter values (linked via the widgets) or generate them dynamically based on Data Factory input

#### Azure Data Factory trigger

Third, create a trigger that is monitoring storage:

* Click through new trigger
* Select new trigger
* Mark the trigger based on event
* Fill in the necessary information on the storage account, container, and blob file name pattern

#### Publishing

Finally, you should be able to publish via Azure Data Factory. Try to upload a file with the proper naming convention and see the run.


