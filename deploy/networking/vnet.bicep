param name string = 'vnet'

module nsgCompute 'nsg/nsg-compute.bicep' = {
  name: 'nsgCompute'
  params: {
    name: 'nsg-compute'
  }
}

module nsgBastion 'nsg/nsg-bastion.bicep' = {
  name: 'nsgBastion'
  params: {
    name: 'nsg-bastion'
  }
}

module nsgDatabricks 'nsg/nsg-databricks.bicep' = {
  name: 'nsgDatabricks'
  params: {
    namePublic: 'nsg-databricks-public'
    namePrivate: 'nsg-databricks-private'
  }
}

module privatezone_datalake_blob 'privatezone.bicep' = {
  name: 'datalake_blob_private_zone'
  scope: resourceGroup()
  params: {
    zone: 'privatelink.blob.core.windows.net'
    vnetId: vnet.id
  }
}

module privatezone_datalake_dfs 'privatezone.bicep' = {
  name: 'datalake_dfs_private_zone'
  scope: resourceGroup()
  params: {
    zone: 'privatelink.dfs.core.windows.net'
    vnetId: vnet.id
  }
}

resource vnet 'Microsoft.Network/virtualNetworks@2020-06-01' = {
  location: resourceGroup().location
  name: name
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'AzureBastionSubnet'
        properties: {
          addressPrefix: '10.0.1.0/27'
          networkSecurityGroup: {
            id: nsgBastion.outputs.nsgId
          }
        }
      }
      {
        name: 'datalake'
        properties: {
          addressPrefix: '10.0.2.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
      {
        name: 'databricks-public'
        properties: {
          addressPrefix: '10.0.3.0/24'
          networkSecurityGroup: {
            id: nsgDatabricks.outputs.publicNsgId
          }
          delegations: [
            {
              name: 'databricks-delegation-public'
              properties: {
                serviceName: 'Microsoft.Databricks/workspaces'
              }
            }
          ]
        }
      }
      {
        name: 'databricks-private'
        properties: {
          addressPrefix: '10.0.4.0/24'
          networkSecurityGroup: {
            id: nsgDatabricks.outputs.privateNsgId
          }
          delegations: [
            {
              name: 'databricks-delegation-private'
              properties: {
                serviceName: 'Microsoft.Databricks/workspaces'
              }
            }
          ]
        }
      }
      {
        name: 'compute'
        properties: {
          addressPrefix: '10.0.10.0/24'
          networkSecurityGroup: {
            id: nsgCompute.outputs.nsgId
          }
        }
      }
    ]
  }
}

output vnetId string = vnet.id
output dataLakeSubnetId string = '${vnet.id}/subnets/datalake'
output computeSubnetId string = '${vnet.id}/subnets/compute'
output bastionSubnetId string = '${vnet.id}/subnets/AzureBastionSubnet'

output databricksPublicSubnetName string = 'databricks-public'
output databricksPrivateSubnetName string = 'databricks-private'

output dataLakeBlobPrivateZoneId string = privatezone_datalake_blob.outputs.privateZoneId
output dataLakeDfsPrivateZoneId string = privatezone_datalake_dfs.outputs.privateZoneId
