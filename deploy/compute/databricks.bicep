param name string
param pricingTier string {
  allowed: [
    'trial'
    'standard'
    'premium'
  ]
}
param vnetId string
param publicSubnetName string
param privateSubnetName string

param loadbalancerId string
param loadBalancerBackendPoolName string

param managedResourceGroupId string

resource databricks 'Microsoft.Databricks/workspaces@2018-04-01' = {
  name: name
  location: resourceGroup().location
  sku: {
    name: pricingTier
  }
  properties: {
    managedResourceGroupId: managedResourceGroupId
    parameters: {
      customVirtualNetworkId: {
        value: vnetId
      } 
      customPrivateSubnetName: {
        value: privateSubnetName
      }
      customPublicSubnetName: {
        value: publicSubnetName
      }
      enableNoPublicIp: {
        value: true
      }
      loadBalancerId: {
        value: loadbalancerId
      }
      loadBalancerBackendPoolName: {
        value: loadBalancerBackendPoolName
      }
    }
  }
}