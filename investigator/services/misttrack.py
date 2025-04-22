import aiohttp
import os
from typing import Optional, Dict, Any, Literal
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://openapi.misttrack.io/v1"
API_KEY = os.environ.get("MISTTRACK_API_KEY")

# 支持的區塊鏈幣種，按照 MistTrack API 文檔要求的正確大寫格式
CoinType = Literal["BTC", "ETH", "TRX", "BSC", "AVAX", "MATIC", "FTM", "HECO", "OPT", "ARB"]

async def get_api_status() -> Dict[str, Any]:
    """Check the status of the MistTrack API."""
    if not API_KEY:
        return {"error": "MISTTRACK_API_KEY environment variable not set."}
    url = f"{BASE_URL}/status"
    headers = {"Authorization": API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.json()

async def get_address_labels(coin: CoinType, address: str) -> Dict[str, Any]:
    """檢索與特定地址相關的標籤。"""
    if not API_KEY:
        return {"error": "MISTTRACK_API_KEY environment variable not set."}
    url = f"{BASE_URL}/address_labels"
    params = {"coin": coin, "address": address, "api_key": API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            print(f"Response from get_address_labels: {data}")  # Debugging line
            return data

async def get_address_overview(coin: CoinType, address: str) -> Dict[str, Any]:
    """獲取地址的餘額和交易統計信息。"""
    if not API_KEY:
        return {"error": "MISTTRACK_API_KEY environment variable not set."}
    url = f"{BASE_URL}/address_overview"
    params = {"coin": coin, "address": address, "api_key": API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

async def get_risk_score(
    coin: CoinType,
    address: Optional[str] = None,
    txid: Optional[str] = None
) -> Dict[str, Any]:
    """評估地址或交易的風險分數。"""
    if not API_KEY:
        return {"error": "MISTTRACK_API_KEY environment variable not set."}
    url = f"{BASE_URL}/risk_score"
    params = {"coin": coin, "api_key": API_KEY}
    if address:
        params["address"] = address
    if txid:
        params["txid"] = txid
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

async def get_transactions_investigation(
    coin: CoinType,
    address: str,
    start_timestamp: Optional[int] = None,
    end_timestamp: Optional[int] = None,
    tx_type: str = "all",
    page: int = 1
) -> Dict[str, Any]:
    """調查給定地址的交易。"""
    if not API_KEY:
        return {"error": "MISTTRACK_API_KEY environment variable not set."}
    url = f"{BASE_URL}/transactions_investigation"
    params = {
        "coin": coin,
        "address": address,
        "api_key": API_KEY,
        "type": tx_type,
        "page": page
    }
    if start_timestamp:
        params["start_timestamp"] = start_timestamp
    if end_timestamp:
        params["end_timestamp"] = end_timestamp
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

async def get_address_actions(coin: CoinType, address: str) -> Dict[str, Any]:
    """分析地址的交易行為。"""
    if not API_KEY:
        return {"error": "MISTTRACK_API_KEY environment variable not set."}
    url = f"{BASE_URL}/address_action"
    params = {"coin": coin, "address": address, "api_key": API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

async def get_address_profile(coin: CoinType, address: str) -> Dict[str, Any]:
    """檢索地址的配置信息。"""
    if not API_KEY:
        return {"error": "MISTTRACK_API_KEY environment variable not set."}
    url = f"{BASE_URL}/address_trace"
    params = {"coin": coin, "address": address, "api_key": API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()
