from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from config import settings
from gql_query import QUERY_REMOTE_NETWORKS, MUTATION_CREATE_RESOURCE

# Twingate API configuration settings loaded from environment variables
API_URL = settings.API_URL
API_KEY = settings.API_KEY
TARGET_NETWORK_NAME = settings.TARGET_NETWORK_NAME

def setup_client():
    """
    Initialize and configure the GraphQL client with API credentials.
    
    Returns:
        Client: Configured GraphQL client instance
    """
    transport = RequestsHTTPTransport(
        url=API_URL,
        headers={"X-API-KEY": API_KEY},
        use_json=True,
    )
    return Client(transport=transport, fetch_schema_from_transport=True)

def get_target_network(client):
    """
    Query the Twingate API to find the target network by name.
    
    Args:
        client (Client): GraphQL client instance
    
    Returns:
        dict: Network details if found, None otherwise
    """
    response = client.execute(QUERY_REMOTE_NETWORKS)
    print(response)
    for edge in response["remoteNetworks"]["edges"]:
        network = edge["node"]
        if network["name"] == TARGET_NETWORK_NAME:
            return network
    return None

def create_resource(client, name, address_value, remote_network_id):
    """
    Create a new Twingate resource with the specified parameters.
    
    Args:
        client (Client): GraphQL client instance
        name (str): Name for the new resource
        address_value (str): IP address for the resource
        remote_network_id (str): ID of the network to create resource in
    
    Returns:
        dict: Created resource details
        
    Raises:
        Exception: If resource creation fails
    """
    params = {
        "name": name,
        "address": address_value,
        "remoteNetworkId": remote_network_id
    }
    response = client.execute(MUTATION_CREATE_RESOURCE, variable_values=params)
    if not response["resourceCreate"]["ok"]:
        raise Exception(f"Failed to create resource: {response['resourceCreate']['error']}")
    return response["resourceCreate"]["entity"]

def automate_resource_creation():
    """
    Main function to automate Twingate resource creation.
    
    This function:
    1. Sets up the GraphQL client
    2. Finds the target network
    3. For each connector in the network:
        - Creates a resource for its public IP (if any)
        - Creates resources for all private IPs
    """
    client = setup_client()

    # Find target network
    print(f"Searching for target network: {TARGET_NETWORK_NAME}...")
    target_network = get_target_network(client)

    if not target_network:
        print(f"Network '{TARGET_NETWORK_NAME}' not found.")
        return

    print(f"Found network: {target_network['name']}")
    remote_network_id = target_network['id']

    # Process each connector in the network
    for connector_edge in target_network["connectors"]["edges"]:
        connector = connector_edge["node"]
        public_ip = connector.get("publicIP")
        private_ips = connector.get("privateIPs", [])

        # Create resource for public IP if available
        if public_ip:
            resource_name = f"Resource-Public-{public_ip.replace('.', '-')}"
            print(f"Creating Resource for public IP: {public_ip}...")
            resource = create_resource(client, resource_name, public_ip, remote_network_id)
            print(f"Resource created: {resource['name']} (ID: {resource['id']}, Address: {resource['address']['value']})")

        # Create resources for all private IPs
        for private_ip in private_ips:
            resource_name = f"Resource-Private-{private_ip.replace('.', '-')}"
            print(f"Creating Resource for private IP: {private_ip}...")
            resource = create_resource(client, resource_name, private_ip, remote_network_id)
            print(f"Resource created: {resource['name']} (ID: {resource['id']}, Address: {resource['address']['value']})")

if __name__ == "__main__":
    try:
        # automate_resource_creation()
        print("Hello World")
    except Exception as e:
        print(f"Error: {e}")
