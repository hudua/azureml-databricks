This guide provides instruction on how to use the Data Factory API Python library to trigger a pipeline run based on parameters:

1) How to construct the pipeline activity in Azure Data Factory
2) How to trigger in Databricks

#### Pipeline activity

Assuming there is a created pipeline that copies from source to sink (being storage account), set up two parameters here, one being the custom query and the other being the output file name. You can get to the pipeline parameter settings by clicking outside of the activity box.
![alt text](/guides/images/adf_0.PNG)
![alt text](/guides/images/adf_1.PNG)

In the source, set up custom query and use this as the query value: @pipeline().parameters.query
![alt text](/guides/images/adf_2.PNG)

In the sink setting, open the sink dataset, set up a parameter called name and you can optionally give it a default value
![alt text](/guides/images/adf_3.PNG)

Continuing in the sink dataset, under Connection setting, select the container and input @dataset().name as the file name. Then, uncheck binary (if checked) and click column names in the first row.
![alt text](/guides/images/adf_4.PNG)
![alt text](/guides/images/adf_5.PNG)

Then finally, in the activity settings, enter @pipeline().parameters.filename as the now avaiable sink parameter.
![alt text](/guides/images/adf_6.PNG)

#### Databricks to run script to automate

This set of code should work, tested for runtime 7.3 LTS. You will need a service principal that has data factory contributor access (ideally) to ADF service.


```python
dbutils.library.installPyPI("azure-mgmt-resource")
dbutils.library.installPyPI("azure-mgmt-datafactory")
dbutils.library.installPyPI("azure-identity")
dbutils.library.restartPython()

from azure.identity import ClientSecretCredential

credentials = ClientSecretCredential(client_id='', client_secret='', tenant_id='')

from azure.mgmt.datafactory import DataFactoryManagementClient

adf_client = DataFactoryManagementClient(credentials, "<subscription id>")

run_response = adf_client.pipelines.create_run("<resource group>", "<adf-name>", "<pipeline-name>", parameters={'query': 'select top 5 stop_no from anomalies', 'filename': 'anomalies2.csv'})
```
