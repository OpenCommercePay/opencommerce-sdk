from opencommerce_sdk import OpenCommerceAccountToolkit
# Initialize OpenCommerce SDK
sdk = OpenCommerceAccountToolkit(network='testnet')
print("✅ SDK initialized successfully")

# Obtain account address
address = sdk.get_account_address()
print(f"My account address: {address}")

# Define URLs for Tavily extract service
urls = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Artificial_general_intelligence"
]

# Define the service request
extract_request = {
    'query': 'tell me about AI',
    'urls': urls
}

# Make the service call
service_response = sdk.use_service('tavily_search', extract_request)
print(f"Search response: {service_response}")
