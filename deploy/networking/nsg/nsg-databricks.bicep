param namePublic string
param namePrivate string

resource nsgPublic 'Microsoft.Network/networkSecurityGroups@2020-06-01' = {
  name: namePublic
  location: resourceGroup().location
}

resource nsgPrivate 'Microsoft.Network/networkSecurityGroups@2020-06-01' = {
  name: namePrivate
  location: resourceGroup().location
}

output publicNsgId string = nsgPublic.id
output privateNsgId string = nsgPrivate.id