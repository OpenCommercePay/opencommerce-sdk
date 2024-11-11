# Service Directory

A service registry that provides a centralized directory of agentic services.

## Current Services

| Service | Description | Cost/Query | URL |
|---------|-------------|------|-----|
| gpt_researcher | GPT Researcher for extensive web research | $0.01 | https://gpt-researcher-service-production.up.railway.app |
| tavily | Tavily is a search engine tailored for AI agents | $0.015 | tavily-search-service-production.up.railway.app |


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

```python
# List all services
GET https://servicedirectory-production.up.railway.app/services/

# Get service by name
GET https://servicedirectory-production.up.railway.app/services/by-name/gpt_researcher

# Get service by ID
GET https://servicedirectory-production.up.railway.app/services/1
```