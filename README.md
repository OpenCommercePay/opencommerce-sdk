# OpenCommerce SDK

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
sdk = OpenCommerceAccountToolkit()
```



## Use a service 
```python
service_response = sdk.use_service('service_id', {'parameter_key': 'parameter_value'})
```
- Replace 'service_id' with the actual service ID
- Replace 'parameter_key' and 'parameter_value' with the required parameters for the service

## Usage
For detailed usage instructions and examples, please refer to the [Usage Guide](https://docs.opencommerce.com/usage).

## Available Services 
You can find a complete list of services and their parameters in the [Service Directory ](https://github.com/opencommerce/sdk/Service_Directory).

## Documentation
* [Installation Guide ](https://github.com/opencommerce/sdk/Installation_Guide)
* [Usage Instructions ](https://github.com/opencommerce/sdk/Usage_Instructions)
* [API Reference ](https://github.com/opencommerce/sdk/API_Reference)
* [Service Directory ](https://github.com/opencommerce/sdk/Service_Directory)

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

## Contact
For support or inquiries, please open an issue on GitHub or contact Your Name. You can also contact idan@opencommerce.xyx