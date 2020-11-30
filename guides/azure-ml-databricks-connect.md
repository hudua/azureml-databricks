This guide provides step-by-step instructions on using Databricks Connect with Azure ML. 

Reference for Databricks Connect is here: https://docs.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect

Note that the runtime version of Databricks should match up with the Databricks Connect version. As well, Databricks runtime uses Python 3.7 so that should be used for Azure ML notebook as well.

For this guide, Databricks runtime 7.1 is used and thus Databricks Connect version 7.1.* is used.

* You will need a compute instance in Azure ML as well. If you haven't already done so, you can create one under Compute --> Compute instances. See for more details: https://github.com/hudua/azureml-databricks/blob/main/guides/1_azureml_guide_data_designer.pdf

* Under Azure ML Notebook, open up terminal

![alt text](/guides/images/adbc1.PNG)

* Execute the following code in terminal, while clicking through to continue as needed. It installs Python 3.7 and sets up a new kernel for Azure ML Notebook.

```console
apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt-get update
sudo apt install python3.7

sudo apt-get install python3-pip

python3.7 -m pip install ipykernel
python3.7 -m ipykernel install --user

python3.7 -m pip uninstall pyspark
python3.7 -m pip install -U databricks-connect==7.1.*

databricks-connect configure
```

On the databricks-connect configuration side, you will need to enter the following:

1) Host: https://adb-5555555555555555.19.azuredatabricks.net/
2) Token: From Databricks Workspace User Settings
3) Cluster ID: from Databricks Workspace Cluster --> Advanced Settings --> Tags (Enter it manually)
4) Org ID: the part in URL after .net/?o= https://adb-5555555555555555.19.azuredatabricks.net/?o=123...
5) Keep port

You can run a test to verify

```console
databricks-connect test
```

* Create a new notebook with Azure ML and select the Python 3 kernel. It should now display Python 3.7.9

![alt text](/guides/images/adbc2.PNG)

* Your Databricks Connect should be set up now! Try a few lines of code as below

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

df = spark.sql('select * from test')

df.show(5)
```
