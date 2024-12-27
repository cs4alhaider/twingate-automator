from gql import gql

QUERY_REMOTE_NETWORKS = gql("""
query GetRemoteNetworkDetails {
  remoteNetworks(after: null, first: 10) {
    edges {
      node {
        id
        name
        connectors {
          edges {
            node {
              id
              name
              publicIP
              privateIPs
              remoteNetwork {
                id
                name
              }
            }
          }
        }
      }
    }
  }
}
""")

MUTATION_CREATE_RESOURCE = gql("""
mutation CreateResource($name: String!, $address: String!, $remoteNetworkId: ID!) {
  resourceCreate(
    name: $name,
    address: $address,
    remoteNetworkId: $remoteNetworkId
  ) {
    ok
    error
    entity {
      id
      name
      address {
        type
        value
      }
    }
  }
}
""")
