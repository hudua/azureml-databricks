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

* Then in your user root directory, create a new notebook and bring in this set of code. This should run, as validated with Azure ML SDK version 1.18.0 per code below. Recall that the user directory should be per code below:

- notebook.ipynb

- example/test.py


```python
import os
import azureml.core
from azureml.core.compute import DatabricksCompute
from azureml.core import Workspace, Experiment
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import DatabricksStep

# Check core SDK version number
print("SDK version:", azureml.core.VERSION)

subscription_id = '<sub>'
resource_group = '<rg>'
workspace_name = '<ws>'

workspace = Workspace(subscription_id, resource_group, workspace_name)

databricks_compute = DatabricksCompute(workspace=workspace, name='<name of Databricks compute you gave>')

python_script_name = "test.py"
source_directory = "./example"

dbPythonInLocalMachineStep = DatabricksStep(
    name="DBPythonInLocalMachine",
    existing_cluster_id = '<Databricks-cluster-id>',
    python_script_name=python_script_name,
    source_directory=source_directory,
    run_name='DB_Python_Local_demo',
    compute_target=databricks_compute,
    allow_reuse=True
)

steps = [dbPythonInLocalMachineStep]
pipeline = Pipeline(workspace=workspace, steps=steps)
pipeline_run = Experiment(workspace, 'DB_Python_Local_demoFriday2').submit(pipeline)
pipeline_run.wait_for_completion()

```
