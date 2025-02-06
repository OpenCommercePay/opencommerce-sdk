# OpenCommerce StableCoins SDK

The OpenCommerce SDK enables AI agents to interact with services and external tools via real-time, on-demand calls. With a simple SDK integration, agent developers gain access to a wide range of tools—including agents, data sources, and APIs—without requiring any pre-configuration.

The SDK autonomously handles payments for every service call, abstracting payment and authentication processes entirely from the agent.

## Features

- **Instant Start**: Begin without complex setup or preconfiguration.
- **Ready-Made Agents**: Access essential, pre-built agents on demand.
- **Financial Abstraction**: Manages all financial interactions with service providers.
- **Seamless Integration**: Easily works with agent frameworks like LangChain.
- **Streamlined Funding**: Simplified options for agent funding.

## Installation

```bash
pip install opencommerce-sdk
```


## Quick Start

```python
from opencommerce_sdk import OpenCommerceAccountToolkit
```


## Initialize the Account Toolkit

```python
sdk = OpenCommerceAccountToolkit(network='testnet')
```
- Replace 'testnet' with 'production' for using real USDC


## Use a service 
```python
service_response = sdk.use_service('service_id', {'parameter_key': 'parameter_value'})
```
- Replace 'service_id' with the actual service ID
- Replace 'parameter_key' and 'parameter_value' with the required parameters for the service

## Usage
For detailed usage instructions and examples, please refer to the [Usage Guide](https://github.com/OpenCommerce-xyz/opencommerce-sdk/tree/main/examples).

## Available Services 
You can find a complete list of services and their parameters in the [Service Directory ](https://github.com/OpenCommerce-xyz/opencommerce-sdk/tree/main/service_directory).


## License
This project is licensed under the MIT License.

## Contact
For support or inquiries, please open an issue on GitHub or contact Your Name. You can also contact idan@opencommerce.xyz
