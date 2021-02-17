param name string

resource nsg 'Microsoft.Network/networkSecurityGroups@2020-06-01' = {
  name: name
  location: resourceGroup().location
}

output nsgId string = nsg.id