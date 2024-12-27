# Twingate Resource Automation Tool

A Python tool that automatically creates Twingate resources by scanning connector IP addresses in your specified network.

## Description

This tool leverages the Twingate GraphQL API to automate the creation of resources based on connector IP addresses. It scans both public and private IPs associated with connectors in your specified network and creates corresponding Twingate resources with standardized naming conventions.

This is a work from a YouTube tutorial by [NetworkChuck](https://blog.networkchuck.com/posts/building-a-hacker-dropbox-access-any-network/), and here is the [YouTube Video](https://youtu.be/1lZ3FQSv-wI?si=KK7Pho4wkA3ps3ky)  

## Features

- Automatically discovers and creates resources for:
  - Public IP addresses of connectors
  - Private IP addresses of connectors
- Standardized naming convention:
  - Public IPs: `Resource-Public-{IP}` (dots replaced with dashes)
  - Private IPs: `Resource-Private-{IP}` (dots replaced with dashes)
- Comprehensive error handling and logging
- Uses GraphQL for efficient API interactions
- Configuration via environment variables

## Usage

1. Clone the repository
2. Create a `.env` file with the required variables using the `.example.env` file as a reference
3. Install the required dependencies using `poetry install`
4. Run the script using `poetry run python3 main.py`

## Notes

- This script is designed to work with Twingate's GraphQL API. Ensure your API key has the necessary permissions to create resources.
- The script will log all actions and errors to the console.
- The script will create resources in the network specified in the `.env` file.
- The script will create resources for both public and private IPs associated with connectors in the specified network.
- The script will use the Twingate API to create resources.
- The script will create resources for all connectors in the specified network.


## Credits

- [NetworkChuck](https://blog.networkchuck.com/posts/building-a-hacker-dropbox-access-any-network/) for the tutorial
- [Twingate](https://twingate.com/) for the API


