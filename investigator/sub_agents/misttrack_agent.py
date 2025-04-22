from google.adk.agents import Agent
from investigator.services.misttrack import *
from investigator.services.state import session_state
from typing import Dict, Any, List, Optional

# 增強版的帶緩存 API 調用

async def get_address_labels_cached(coin: CoinType, address: str) -> Dict[str, Any]:
    """
    獲取指定地址的標籤並緩存結果。
    
    參數:
        coin: 加密貨幣類型（BTC, ETH, TRX等）
        address: 區塊鏈地址
        
    返回:
        地址標籤信息
    """
    # 檢查緩存
    cached_data = session_state.get_cached_address_data(coin, address, 'labels')
    if cached_data:
        cached_data['from_cache'] = True
        return cached_data
    
    # 調用 API
    result = await get_address_labels(coin, address)
    
    # 緩存結果
    if result and 'error' not in result:
        session_state.cache_address_data(coin, address, 'labels', result)
    
    return result

async def get_address_overview_cached(coin: CoinType, address: str) -> Dict[str, Any]:
    """
    獲取地址概述並緩存結果。
    
    參數:
        coin: 加密貨幣類型（BTC, ETH, TRX等）
        address: 區塊鏈地址
        
    返回:
        地址概述信息
    """
    # 檢查緩存
    cached_data = session_state.get_cached_address_data(coin, address, 'overview')
    if cached_data:
        cached_data['from_cache'] = True
        return cached_data
    
    # 調用 API
    result = await get_address_overview(coin, address)
    
    # 緩存結果
    if result and 'error' not in result:
        session_state.cache_address_data(coin, address, 'overview', result)
    
    return result

async def get_risk_score_cached(
    coin: CoinType,
    address: Optional[str] = None,
    txid: Optional[str] = None
) -> Dict[str, Any]:
    """
    獲取風險評分並緩存結果。
    
    參數:
        coin: 加密貨幣類型（BTC, ETH, TRX等）
        address: 區塊鏈地址（與 txid 二選一）
        txid: 交易 ID（與 address 二選一）
        
    返回:
        風險評分信息
    """
    if address:
        # 檢查地址緩存
        cached_data = session_state.get_cached_address_data(coin, address, 'risk_score')
        if cached_data:
            cached_data['from_cache'] = True
            return cached_data
    
    elif txid:
        # 檢查交易緩存
        cached_data = session_state.get_cached_transaction_data(coin, txid)
        if cached_data:
            cached_data['from_cache'] = True
            return cached_data
    
    # 調用 API
    result = await get_risk_score(coin, address, txid)
    
    # 緩存結果
    if result and 'error' not in result:
        if address:
            session_state.cache_address_data(coin, address, 'risk_score', result)
        elif txid:
            session_state.cache_transaction_data(coin, txid, result)
    
    return result

async def get_transactions_and_store(
    coin: CoinType,
    address: str,
    start_timestamp: Optional[int] = None,
    end_timestamp: Optional[int] = None,
    tx_type: str = "all",
    page: int = 1
) -> Dict[str, Any]:
    """
    調查指定地址的交易並將其存儲在會話狀態中。
    
    參數:
        coin: 加密貨幣類型（BTC, ETH, TRX等）
        address: 要調查的區塊鏈地址
        start_timestamp: 可選的開始時間過濾器
        end_timestamp: 可選的結束時間過濾器
        tx_type: 交易類型過濾器（all, in, out）
        page: 結果頁碼
        
    返回:
        交易數據和狀態
    """
    # 檢查緩存
    cache_key = f"tx_investigation_{tx_type}_{page}"
    cached_data = session_state.get_cached_address_data(coin, address, cache_key)
    if cached_data and not start_timestamp and not end_timestamp:
        # 時間過濾器會影響結果，沒有時間過濾器時才使用緩存
        cached_data['from_cache'] = True
        
        # 確保圖形數據也存在
        tx_graph_data = session_state.transform_misttrack_data(cached_data)
        session_state.set_tx_data(tx_graph_data)
        
        cached_data["data_stored_for_graph"] = True
        cached_data["graph_edge_count"] = len(tx_graph_data)
        
        return cached_data
    
    # 調用原始函數
    result = await get_transactions_investigation(
        coin=coin,
        address=address,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tx_type=tx_type,
        page=page
    )
    
    # 如果成功，轉換並存儲數據
    if result and "data" in result:
        # 緩存交易調查結果
        if not start_timestamp and not end_timestamp:
            # 沒有時間過濾器的結果才緩存
            session_state.cache_address_data(coin, address, cache_key, result)
        
        # 轉換為圖形代理所需的格式
        tx_graph_data = session_state.transform_misttrack_data(result)
        
        # 存儲在會話狀態中
        session_state.set_tx_data(tx_graph_data)
        
        # 添加標志表示數據已存儲
        result["data_stored_for_graph"] = True
        result["graph_edge_count"] = len(tx_graph_data)
    
    return result

async def get_address_actions_cached(coin: CoinType, address: str) -> Dict[str, Any]:
    """
    獲取地址操作並緩存結果。
    
    參數:
        coin: 加密貨幣類型（BTC, ETH, TRX等）
        address: 區塊鏈地址
        
    返回:
        地址操作信息
    """
    # 檢查緩存
    cached_data = session_state.get_cached_address_data(coin, address, 'actions')
    if cached_data:
        cached_data['from_cache'] = True
        return cached_data
    
    # 調用 API
    result = await get_address_actions(coin, address)
    
    # 緩存結果
    if result and 'error' not in result:
        session_state.cache_address_data(coin, address, 'actions', result)
    
    return result

async def get_address_profile_cached(coin: CoinType, address: str) -> Dict[str, Any]:
    """
    獲取地址資料並緩存結果。
    
    參數:
        coin: 加密貨幣類型（BTC, ETH, TRX等）
        address: 區塊鏈地址
        
    返回:
        地址資料信息
    """
    # 檢查緩存
    cached_data = session_state.get_cached_address_data(coin, address, 'profile')
    if cached_data:
        cached_data['from_cache'] = True
        return cached_data
    
    # 調用 API
    result = await get_address_profile(coin, address)
    
    # 緩存結果
    if result and 'error' not in result:
        session_state.cache_address_data(coin, address, 'profile', result)
    
    return result

async def get_investigation_summary() -> Dict[str, Any]:
    """
    獲取當前調查的摘要信息。
    
    返回:
        包含調查摘要信息的字典
    """
    return session_state.get_investigation_summary()

misttrack_agent = Agent(
    name="misttrack_crypto_agent",
    model="gemini-2.0-flash",
    description=(
        "提供使用 MistTrack 服務的區塊鏈和加密貨幣數據的代理，帶有數據緩存功能。"
    ),
    instruction=(
        "此代理使用 MistTrack 服務提供區塊鏈和加密貨幣數據，並自動緩存所有調查結果。\n"
        "API 密鑰自動從 MISTTRACK_API_KEY 環境變量中檢索。\n"
        "你可以使用以下工具：\n"
        "- get_api_status: 檢查 MistTrack API 狀態。\n"
        "- get_address_labels_cached: 獲取並緩存特定地址的標籤。需要 'coin'、'address'。\n"
        "- get_address_overview_cached: 獲取並緩存地址的餘額和交易統計信息。需要 'coin'、'address'。\n"
        "- get_risk_score_cached: 評估並緩存地址或交易的風險評分。需要 'coin' 和 'address' 或 'txid'。\n"
        "- get_transactions_investigation: 調查地址的交易（無緩存）。需要 'coin'、'address'。可選：'start_timestamp'、'end_timestamp'、'tx_type'、'page'。\n"
        "- get_transactions_and_store: 調查並緩存地址的交易，同時為圖形渲染準備數據。需要 'coin'、'address'。\n"
        "- get_address_actions_cached: 分析並緩存地址的交易行為。需要 'coin'、'address'。\n"
        "- get_address_profile_cached: 獲取並緩存地址的資料信息。需要 'coin'、'address'。\n"
        "- get_investigation_summary: 獲取當前調查的摘要信息，包括已調查的地址和交易。\n\n"
        "優先使用帶有 _cached 後綴的函數來獲取數據，這將自動緩存結果並提高性能。\n"
        "當需要視覺化交易數據時，使用 get_transactions_and_store 函數，這將自動為圖形代理準備數據。\n\n"
        "緩存的數據在會話期間保持有效，你可以通過 get_investigation_summary 查看當前緩存的內容。"
    ),
    tools=[
        get_api_status,
        get_address_labels, 
        get_address_labels_cached,
        get_address_overview, 
        get_address_overview_cached,
        get_risk_score, 
        get_risk_score_cached,
        get_transactions_investigation,
        get_transactions_and_store,
        get_address_actions, 
        get_address_actions_cached,
        get_address_profile, 
        get_address_profile_cached,
        get_investigation_summary
    ],
)