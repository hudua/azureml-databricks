This guide follows this general reference: https://docs.microsoft.com/en-us/azure/machine-learning/how-to-network-security-overview

Here is a general reference referencing Azure Databricks as well:

![adbaad](/networking/images/arch.PNG)

#### Azure ML workspace private endpoint
In the first step, here are the instructions to set up private endpoint (Private IP) for Azure ML workspace.

* Create an Azure ML workspace: https://ms.portal.azure.com/#create/Microsoft.MachineLearningServices
* Once the service is created, go to private endpoint connections under settings, and click on Private endpoint
![adbaad](/networking/images/private.PNG)
* Give the private endpoint a name and region
![adbaad](/networking/images/region.PNG)
* Select Microsoft.MachineLearningServices/workspaces as the type and find the resource itself
![adbaad](/networking/images/settings.PNG)
* Pick the virtual network and subnet with a private DNS (default)
![adbaad](/networking/images/network.PNG)

#### Accessing Azure ML workspace with private endpoint-endpoint
Once you have private endpoint enabled, you will reach an error when on ml.azure.com (public IP). You will need a jumpbox VM like using Bastion or Windows Virtual Desktop that has access to the subnet.

#### Creating compute
After you visit Azure ML through for example Bastion, you can create a compute as usual. For either computer instance and computer cluster, Be sure to go to enable virtual network under advanced settings and pick the right subnet.

![adbaad](/networking/images/compute.PNG)

#### Accessing data in storage account
With the right storage account, you can allow access from select network, under settings -> firewalls and virtual networks. You can configure network security so only services within certain subnets can access storage account (including the compute services in Azure ML).

![adbaad](/networking/images/storage.PNG)

#### Creating datastore
You can create a datastore as normal: 
* Be sure to select Yes for using workspace managed identity for data preview and profiling.
![adbaad](/networking/images/mi.PNG)
* The managed identity that is created for Azure ML is called the same as the workspace. Depending on permissions, you might need to give it something like "Storage Blob Data Reader" role assignment for the storage account.

#### Creating a dataset and running compute
Once the datastore is created per above, you should be able to create dataset and run compute (e.g. Notebook VM, AutoML, Designer) as normal.


