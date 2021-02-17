param zone string
param vnetId string
param registrationEnabled bool = false

resource privateZone 'Microsoft.Network/privateDnsZones@2018-09-01' = {
  name: zone
  location: 'global'
}

resource virtualNetworkLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2018-09-01' = {
  name: '${privateZone.name}/${uniqueString(vnetId)}'
  location: 'global'
  properties: {
    virtualNetwork: {
      id: vnetId
    }
    registrationEnabled: registrationEnabled
  }
}

output privateZoneId string = privateZone.id