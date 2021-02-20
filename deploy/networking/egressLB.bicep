param name string

var loadBalancerBackendPoolName = 'lbBackendPool'
var loadBalancerBackendPoolId = resourceId('Microsoft.Network/loadBalancers/backendAddressPools', name, loadBalancerBackendPoolName)

var loadBalancerFrontendConfigName = 'frontendConfig'
var loadBalancerFrontendConfigId = resourceId('Microsoft.Network/loadBalancers/frontendIPConfigurations', name, loadBalancerFrontendConfigName)


resource lbPublicIp 'Microsoft.Network/publicIPAddresses@2020-06-01' = {
  name: '${name}-publicip'
  location: resourceGroup().location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

resource lb 'Microsoft.Network/loadBalancers@2020-06-01' = {
  name: name
  location: resourceGroup().location
  sku: {
    name: 'Standard'
  }
  properties: {
    frontendIPConfigurations: [
      {
        name: loadBalancerFrontendConfigName
        properties: {
          publicIPAddress: {
            id: lbPublicIp.id
          }
        }
      }
    ]
    backendAddressPools: [
      {
        name: loadBalancerBackendPoolName
      }
    ]
    outboundRules: [
      {
        name: 'databricks-outbound-rule'
        properties: {
          allocatedOutboundPorts: 0
          protocol: 'All'
          enableTcpReset: true
          idleTimeoutInMinutes: 4
          backendAddressPool: {
            id: loadBalancerBackendPoolId
          }
          frontendIPConfigurations: [
            {
              id: loadBalancerFrontendConfigId
            }
          ]
        }
      }
    ]
  }
}

output lbId string = lb.id
output lbBackendPoolName string = loadBalancerBackendPoolName