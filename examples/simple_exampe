from opencommerce_sdk import OpenCommerceAccountToolkit

# Initialize the SDK
# the SDK will automatically create an account if it doesn't exist
sdk = OpenCommerceAccountToolkit(network='testnet')
print(f"✅ SDK initialized successfully")

# Get the account address
address = sdk.get_account_address()
print(f"My account address: {address}")

# Use a service
# you can use any service from the service directory (https://github.com/opencommerce-xyz/sdk/service-directory)
service_response = sdk.use_service('gpt_researcher', {'query': 'tell me about Doland Trump'})
print(f"Service response: {service_response}")
