param windowsVMUsername string
param windowsVMPassword string {
  secure: true
}

module vnet './networking/vnet.bicep' = {
  name: 'vnet'
  params: {
    name: 'vnet'
  }
}

module bastion './networking/bastion.bicep' = {
  name: 'bastion'
  params: {
    bastionName: 'bastion'
    bastionSubnetId: vnet.outputs.bastionSubnetId
  }
}

module dataLake './data/adlsgen2.bicep' = {
  name: 'datalake'
  params: {
    namePrefix: 'datalake'
    privateEndpointSubnetId: vnet.outputs.dataLakeSubnetId
    privateZoneId: vnet.outputs.dataLakePrivateZoneId
  }
}

module databricks './compute/databricks.bicep' = {
  name: 'databricks'
  params: {
    name: 'databricks'
    vnetId: vnet.outputs.vnetId
    pricingTier: 'standard'
    managedResourceGroupId: '${subscription().id}/resourceGroups/databricks-rg-${resourceGroup().name}-${uniqueString(resourceGroup().id)}'
    publicSubnetName: vnet.outputs.databricksPublicSubnetName
    privateSubnetName: vnet.outputs.databricksPrivateSubnetName
  }
}

module testVM './compute/windows2019.bicep' = {
  name: 'testvm'
  params: {
    enableAcceleratedNetworking: true
    vmName: 'data1-win2019'
    vmSize: 'Standard_DS2_v2'
    subnetId: vnet.outputs.computeSubnetId
    zone: '1'
    username: windowsVMUsername
    password: windowsVMPassword
  }
}