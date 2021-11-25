This section covers how to run a PyTorch experiment using GPU on Azure Machine Learning. For this example, images are used for image classification but NLP based text dataset can be used as well.

The data

Here are a few steps to do this: 

1. Create a compute cluster in Azure ML, by going to Compute --> Compute clusters --> Create new. Be sure to select a GPU SKU.
2. Create a datastore (to storage account) connection in Azure ML, by going to Datastores --> New datstore.
3. Create a dataset in Azure ML, by going to Datasets --> Create dataset from datastore. Be sure to pick File as Dataset type (and select all the files). The name used for this repo is: pytorchdataset

By assumption, the dataset folder is expected to be organized as such, and data can be downloaded here: https://azureopendatastorage.blob.core.windows.net/testpublic/temp/fowl_data.zip

```sh
fowl_data
--train
----chickens
----turkeys
--val
----chickens
----turkeys
```

Alternatively, one can uncomment the other download_data() method to download data as part of the Python script (instead of accessing a dataset to storage account on Azure).

The script will train an image classification PyTorch model on fowl images of chickens and turkeys. Then the model will be saved and registered to Azure ML as the central model registry.

A reference Jupyter Notebook example is here: https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/ml-frameworks/pytorch/train-hyperparameter-tune-deploy-with-pytorch/train-hyperparameter-tune-deploy-with-pytorch.ipynb

Some documentation for this example is here: https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-pytorch
