# agent_reach/channels/coingecko.py
"""Cryptocurrency price channel for Agent-Reach using CoinGecko API."""

from typing import Optional
import urllib.request
import json
from agent_reach.channels.base import Channel
from agent_reach.config import Config


class CoingeckoChannel(Channel):
    """Get cryptocurrency prices from CoinGecko."""
    
    name = "coingecko"
    description = "Get cryptocurrency prices (e.g., Bitcoin) from CoinGecko"
    tier = 0  # Zero config needed
    backends = ["CoinGecko API"]

    def can_handle(self, url: str) -> bool:
        return False  # Not URL-handling channel

    def check(self, config=None):
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    price = data.get("bitcoin", {}).get("usd")
                    if price is not None:
                        return "ok", f"Bitcoin price: ${price:,.2f}"
                    else:
                        return "error", "Unexpected response format from CoinGecko"
                else:
                    return "error", f"CoinGecko API returned status {response.status}"
        except urllib.error.URLError as e:
            return "error", f"Failed to connect to CoinGecko: {str(e.reason)}"
        except json.JSONDecodeError as e:
            return "error", f"Failed to parse CoinGecko response: {str(e)}"
        except Exception as e:
            return "error", f"Unexpected error: {str(e)}"
