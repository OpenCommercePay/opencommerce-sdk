# OpenCommerce SDK Guide

Simple guide to using OpenCommerce SDK directly and with LangChain integration.

## Basic Usage

```python
from opencommerce_sdk import OpenCommerceAccountToolkit

# Initialize SDK (automatically creates account if needed)
sdk = OpenCommerceAccountToolkit(network='testnet')

# Get account address
address = sdk.get_account_address()

# Use a service
response = sdk.use_service('gpt_researcher', {
    'query': 'tell me about Tesla stock'
})
```

## LangChain Integration

### Setup

```python
from langchain.agents import Tool, AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from opencommerce_sdk import OpenCommerceAccountToolkit

# Initialize SDK
sdk = OpenCommerceAccountToolkit(network='testnet')

# Create tool
tools = [
    Tool(
        name="GPTResearcher",
        func=lambda query: sdk.use_service('gpt_researcher', {'query': query}),
        description="Tool for getting detailed stock analysis information"
    )
]

# Setup LangChain components
llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)
```

### Using the Agent

```python
# Run analysis
response = await agent.arun(
    "Provide comprehensive stock analysis data for Tesla, focusing on financial metrics"
)
```

## Key Components
- `OpenCommerceAccountToolkit`: Main SDK interface
- `network`: Use 'testnet' for development
- `Tool`: LangChain class for tools
- `AgentType.ZERO_SHOT_REACT_DESCRIPTION`: LangChain agent that uses a simple prompt to determine which tools to use without requiring examples. Makes decisions based on tool descriptions.

## Available Services

Currently available services:
- `gpt_researcher`: AI research tool for stock analysis
- `tavily_search` : Search engine tailored for AI agents

## Environment Setup

```bash
pip install opencommerce-sdk langchain langchain-openai
```

Required environment variables:
```bash
OPENAI_API_KEY=your_openai_key
```