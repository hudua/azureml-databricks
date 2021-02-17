param bastionName string = 'bastion'
param bastionSubnetId string

resource bastionPublicIP 'Microsoft.Network/publicIPAddresses@2020-06-01' = {
  location: resourceGroup().location
  name: '${bastionName}-publicip'
  sku: {
      name: 'Standard'
  }
  properties: {
      publicIPAddressVersion: 'IPv4'
      publicIPAllocationMethod: 'Static'
  }
}

resource bastion 'Microsoft.Network/bastionHosts@2020-06-01' = {
  location: resourceGroup().location
  name: bastionName
  properties: {
      dnsName: uniqueString(resourceGroup().id)
      ipConfigurations: [
          {
              name: 'IpConf'
              properties: {
                  subnet: {
                      id: bastionSubnetId
                  }
                  publicIPAddress: {
                      id: bastionPublicIP.id
                  }
              }
          }
      ]
  }
}