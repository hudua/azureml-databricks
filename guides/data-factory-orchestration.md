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

* Create a new linked service: Manage --> Linked services --> New --> Compute --> Databricks
![alt text][/guides/images/1.PNG]

* You can select the relevant Databricks service and get the token here. Selet existing interactive cluster for now. Once you enter the access token, you should be able to select cluster ID.
![alt text][/guides/images/2.PNG]
![alt text][/guides/images/3.PNG]

* Test the connection and then save

#### Azure Data Factory pipeline of Databricks notebook

Second, create a pipeline with Databricks run notebook:

* Create a new pipeline: Author --> Pipelines --> New pipeline
![alt text][/guides/images/4.PNG]

* Select the Databricks - Notebook option and drag it to the designer
![alt text][/guides/images/5.PNG]

* You can select Databricks linked service and then the notebook you want to run
![alt text][/guides/images/6.PNG]
![alt text][/guides/images/7.PNG]

* There is option for you to manually specify parameter values (linked via the widgets) or generate them dynamically based on Data Factory input
![alt text][/guides/images/8.PNG]

#### Azure Data Factory trigger

Third, create a trigger that is monitoring storage:

* Click through trigger and select new trigger
![alt text][/guides/images/9.PNG]

* Mark the trigger based on event
* Fill in the necessary information on the storage account, container, and blob file name pattern
![alt text][/guides/images/10.PNG]

* You might need to register Event.Grid resource provider in the subscription

#### Publishing

Finally, you should be able to publish via Azure Data Factory. Try to upload a file with the proper naming convention and see the run.
![alt text][/guides/images/11.PNG]

