# Service Directory

A service registry that provides a centralized directory of agentic services.

## Current Services

| Service | Description | Cost | URL |
|---------|-------------|------|-----|
| gpt_researcher | GPT Researcher for stock analysis | $0.01 | https://gpt-researcher-service-production.up.railway.app |

## Service Schema

Each service in the directory contains:
```json
{
    "name": "string",
    "url": "string",
    "service_metadata": {
        "cost": "number",
        "description": "string",
        "address": "string"
    },
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## Public API Endpoints

Base URL: `https://servicedirectory-production.up.railway.app`

- List all services: `GET /services/`
- Get service by ID: `GET /services/{service_id}`
- Get service by name: `GET /services/by-name/{name}`

## Example Usage

See [example queries and responses](https://github.com/OpenCommerce-xyz/opencommerce-sdk/blob/main/sdk/service_directory.py) for detailed API usage.