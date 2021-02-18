param privateEndpointSubnetId string
param privateZoneId string
param namePrefix string = 'datalake'

resource datalake 'Microsoft.Storage/storageAccounts@2019-06-01' = {
  location: resourceGroup().location
  name: '${namePrefix}${uniqueString(resourceGroup().id)}'
  identity: {
    type: 'SystemAssigned'
  }
  kind: 'StorageV2'
  sku: {
    name: 'Standard_GRS'
  }
  properties: {
    accessTier: 'Hot'
    isHnsEnabled: true
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'Logging,Metrics'
    }
  }
}

resource datalake_pe 'Microsoft.Network/privateEndpoints@2020-06-01' = {
  location: resourceGroup().location
  name: '${datalake.name}-endpoint'
  properties: {
    subnet: {
      id: privateEndpointSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${datalake.name}-endpoint'
        properties: {
          privateLinkServiceId: datalake.id
          groupIds: [
            'blob',
            'dbf'
          ]
        }
      }
    ]
  }
}

resource datalake_pe_dns_reg 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2020-06-01' = {
  name: '${datalake_pe.name}/default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'privatelink_blob_dbf_core_windows_net'
        properties: {
          privateDnsZoneId: privateZoneId
        }
      }
    ]
  }
}
