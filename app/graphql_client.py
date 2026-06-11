import httpx
import os

DATAGRAPH_URL = os.getenv("DATAGRAPH_URL", "http://localhost:4000")


def run_query(query: str, variables: dict = None) -> dict:
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = httpx.post(DATAGRAPH_URL, json=payload)
    response.raise_for_status()
    result = response.json()

    if "errors" in result:
        raise ValueError(result["errors"])

    return result["data"]
