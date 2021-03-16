In this guide, we will go over building a scalable Azure ML Designer pipeline, and then running it through pipeline endpoint.

First, go to Azure ML Designer and construct a sample pipeline as such. See this guide for more information on how to use Azure ML Designer: https://github.com/hudua/azureml-databricks/blob/main/guides/1_azureml_guide_data_designer.pdf

You can upload the sample dataset here.

* Import data: you would to point it to a CSV (for example) in a datastore that you have connected with
* Process text: use the text column to clean
* Execute Python Script: you can import your custom Python script
* Feature hashing: Here you process text to vectors
* Export data: you would save the output back to the datastore

Then submit the run - please note that each module of run is containerized for repeatability so will take a couple of minute for the end-to-end run.

Once the run is complete, you can see the output in the storage account (referenced as the datastore).

Then publish it and you should be able to consume it in the Notebooks (or anywhere else) through these commands.

