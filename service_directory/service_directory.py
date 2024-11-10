import httpx
import asyncio
from typing import List

BASE_URL = "https://servicedirectory-production.up.railway.app"

# Fetch all services from the service directory.
async def get_all_services() -> List[dict]:
    """Fetch all services from the service directory."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/services/")
        if response.status_code != 200:
            raise httpx.HTTPError(f"Failed to fetch services: {response.status_code}")
        return response.json()

# Fetch a specific service by ID from the service directory.
async def get_service(service_id: int) -> dict:
    """Fetch a specific service by ID from the service directory."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/services/{service_id}")
        if response.status_code != 200:
            raise httpx.HTTPError(f"Failed to fetch service: {response.status_code}")
        return response.json()

# Main function to run the service directory example.
async def main():
    try:
        # Get and print all services
        print("\nFetching all services...")
        services = await get_all_services()
        print("All services:")
        for service in services:
            # Print all available fields for each service
            print(f"- Service details: {service}")

        # Get and print a specific service (example with ID 1)
        print("\nFetching service with ID 1...")
        service = await get_service(1)
        print(f"Single service details:\n{service}")

    except httpx.HTTPError as e:
        print(f"Error occurred: {e}")
    except KeyError as e:
        print(f"Error accessing data field: {e}")

if __name__ == "__main__":
    asyncio.run(main())
