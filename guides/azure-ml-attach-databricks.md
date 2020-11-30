This guide provides step-by-step instructions on attaching Azure Databricks as remote compute for Azure ML. 

Reference is here: https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/intro-to-pipelines/aml-pipelines-use-databricks-as-compute-target.ipynb (Section 3: Running a Python script in Databricks that currenlty is in local computer)

* Go to Compute --> Attached compute --> New --> Azure Databricks

![alt text](/guides/images/amladb1.PNG)

* Provide a compute name and select the Databricks workspace. Enter the Databricks access token from Databricks workspace's User Settings page

![alt text](/guides/images/amladb2.PNG)

* You will need a compute instance in Azure ML as well. If you haven't already done so, you can create one under Compute --> Compute instances. See for more details: https://github.com/hudua/azureml-databricks/blob/main/guides/1_azureml_guide_data_designer.pdf

* Then under Notebooks, you should create a new folder in your user directory

![alt text](/guides/images/amladb3.PNG)

* Create a sample .py file in the newly created folder, which is one that you would put your Python code to execute with Databricks. To start you can put something like this here:

```python
print('this is where you can run code to remote compute in Databricks!')
a = 1 + 1
print(a)
```
![alt text](/guides/images/amladb4.PNG)
![alt text](/guides/images/amladb5.PNG)

