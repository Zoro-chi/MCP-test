from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize FastMCP Server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0 "


async def make_request(url: str) -> dict[str, Any] | None:
    """
    Make request to the specified URL and return the JSON response.
    """

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Request error: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    return None


def format_alert(feature: dict) -> str:
    """
    Format the alert information into a readable string.
    """
    props = feature["properties"]

    return f"""
        Event: {props.get("event", "Unknown Event")}
        Area: {props.get("areaDesc", "Unknown Area")}
        Severity: {props.get("severity", "Unknown Severity")}
        Description: {props.get("description", "No description available")}
        Instruction: {props.get("instruction", "No instruction provided")}
        """


@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a specific state.

    Args:
        state (str): Two Letter US State code (e.g., "CA" for California).
    """
    url = f"{NWS_API_BASE}/alerts/active/area={state}"
    data = await make_request(url)

    # Log to file instead of print
    with open("data_log.txt", "a") as f:
        f.write(f"Data for {state}: {data}\n\n")

    if not data or "features" not in data:
        return "No alerts found."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"
