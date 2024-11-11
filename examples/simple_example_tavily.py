from opencommerce_sdk import OpenCommerceAccountToolkit

sdk = OpenCommerceAccountToolkit(network='testnet')
print(f"✅ SDK initialized successfully")


address = sdk.get_account_address()
print(f"My account address: {address}")

# Define the search request
search_request = {
        'query': 'tell me about Donald Trump',
        'search_depth': 'advanced'
    }


# Make the service call
service_response = sdk.use_service('tavily_search', search_request)
print(f"Search response: {service_response}")