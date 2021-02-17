param name string

resource natGatewayPublicIp 'Microsoft.Network/publicIPAddresses@2020-06-01' = {
  name: '${name}-publicip'
  location: resourceGroup().location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
  zones: [
    '1'
  ]
}

resource natGateway 'Microsoft.Network/natGateways@2020-06-01' = {
  name: name
  location: resourceGroup().location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIpAddresses: [
      {
        id: natGatewayPublicIp.id
      }
    ]
  }
  zones:[
    '1'
  ]
}

output natGatewayId string = natGateway.id