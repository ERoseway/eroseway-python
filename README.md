# Eroseway Python API client

Eroseway API Client for Python.

## Requirements

- Python 3.7+


# Usage

```Python

import eroseway

api_client = eroseway.APIClient(
    clinic_id='MY_CLINIC_ID',
    api_key='MY_API_KEY',
    api_secret='MY_API_SECRET'
)

users = api_client(
    'get',
    'users',
    {'filters-q': ['lyra']}
)

```
