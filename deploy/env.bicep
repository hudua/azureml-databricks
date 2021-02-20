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

module egressLb './networking/egressLb.bicep' = {
  name: 'egressLb'
  params: {
    name: 'egressLb'
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
    pricingTier: 'premium'
    managedResourceGroupId: '${subscription().id}/resourceGroups/databricks-rg-${resourceGroup().name}-${uniqueString(resourceGroup().id)}'
    publicSubnetName: vnet.outputs.databricksPublicSubnetName
    privateSubnetName: vnet.outputs.databricksPrivateSubnetName
    loadbalancerId: egressLb.outputs.lbId
    loadBalancerBackendPoolName: egressLb.outputs.lbBackendPoolName
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