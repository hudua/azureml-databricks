In this guide, we will go over building a scalable Azure ML Designer pipeline, and then running it through pipeline endpoint.

First, go to Azure ML Designer and construct a sample pipeline as such. See this guide for more information on how to use Azure ML Designer: https://github.com/hudua/azureml-databricks/blob/main/guides/1_azureml_guide_data_designer.pdf Here is the entire pipeline that you can build out in Designer:

![alt text](/guides/images/pipeline1.PNG)

You can upload the sample dataset in datastore, per the Designer guide above: https://github.com/hudua/azureml-databricks/blob/main/data/sample_text.csv

* Dataset: you would to point it to a dataset (for example) in a datastore that you have connected with, using latest version

![alt text](/guides/images/pipeline12.PNG)


* Process text: use the text column to clean

![alt text](/guides/images/pipeline3.PNG)


* Execute Python Script: you can import your custom Python script

* Feature hashing: Here you process text to vectors

![alt text](/guides/images/pipeline4.PNG)


* Export data: you would save the output back to the datastore

![alt text](/guides/images/pipeline5.PNG)


Then submit the run - please note that each module of run is containerized for repeatability so will take a couple of minute for the end-to-end run.

Once the run is complete, you can see the output in the storage account (referenced as the datastore).
![alt text](/guides/images/pipeline6.PNG)

Then publish it and you should be able to consume it in the Notebooks (or anywhere else) through these commands.

![alt text](/guides/images/pipeline7.PNG)

