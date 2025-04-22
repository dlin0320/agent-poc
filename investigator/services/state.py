from typing import Dict, Any, List, Optional, Set
import time
import os
import tempfile
import uuid

class SessionState:
    """
    管理代理之間的會話狀態。
    允許跨代理邊界存儲和檢索數據，並緩存所有調查相關數據。
    """
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._investigation_cache: Dict[str, Dict[str, Any]] = {}
        self._addresses_investigated: Set[str] = set()
        self._transactions_analyzed: Set[str] = set()
        self._last_updated: Dict[str, float] = {}
        
        # 建立臨時文件目錄用於存儲圖像
        self._temp_dir = tempfile.mkdtemp(prefix="tx_graphs_")
        self._graph_files: Dict[str, str] = {}
    
    def set(self, key: str, value: Any) -> None:
        """在會話狀態中設置值。"""
        self._state[key] = value
        self._last_updated[key] = time.time()
    
    def get(self, key: str, default: Any = None) -> Any:
        """從會話狀態中獲取值。"""
        return self._state.get(key, default)
    
    def clear(self) -> None:
        """清除所有會話狀態。"""
        self._state = {}
        self._investigation_cache = {}
        self._addresses_investigated = set()
        self._transactions_analyzed = set()
        self._last_updated = {}
        
        # 清除圖像文件
        for filepath in self._graph_files.values():
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
        self._graph_files = {}
    
    def get_tx_data(self) -> List[Dict[str, str]]:
        """
        獲取用於圖形渲染的交易數據格式。
        如果沒有可用數據，則返回空列表。
        """
        return self.get('tx_data', [])
    
    def set_tx_data(self, tx_data: List[Dict[str, str]]) -> None:
        """
        以圖形渲染所需的格式存儲交易數據。
        """
        self.set('tx_data', tx_data)
    
    # 緩存相關方法
    
    def cache_address_data(self, coin: str, address: str, data_type: str, data: Dict[str, Any]) -> None:
        """
        緩存與特定地址相關的數據。
        
        參數:
            coin: 幣種類型（eth、btc等）
            address: 區塊鏈地址
            data_type: 數據類型（標籤、概述、風險評分等）
            data: 要緩存的數據
        """
        cache_key = f"{coin}_{address}"
        if cache_key not in self._investigation_cache:
            self._investigation_cache[cache_key] = {}
        
        self._investigation_cache[cache_key][data_type] = {
            'data': data,
            'timestamp': time.time()
        }
        
        self._addresses_investigated.add(address)
    
    def get_cached_address_data(self, coin: str, address: str, data_type: str) -> Optional[Dict[str, Any]]:
        """
        獲取緩存的地址數據。
        
        參數:
            coin: 幣種類型
            address: 區塊鏈地址
            data_type: 數據類型
            
        返回:
            緩存的數據，如果不存在則返回 None
        """
        cache_key = f"{coin}_{address}"
        if cache_key in self._investigation_cache and data_type in self._investigation_cache[cache_key]:
            return self._investigation_cache[cache_key][data_type]['data']
        return None
    
    def cache_transaction_data(self, coin: str, txid: str, data: Dict[str, Any]) -> None:
        """
        緩存特定交易的數據。
        
        參數:
            coin: 幣種類型
            txid: 交易 ID
            data: 要緩存的數據
        """
        cache_key = f"{coin}_tx_{txid}"
        self._investigation_cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        self._transactions_analyzed.add(txid)
    
    def get_cached_transaction_data(self, coin: str, txid: str) -> Optional[Dict[str, Any]]:
        """
        獲取緩存的交易數據。
        
        參數:
            coin: 幣種類型
            txid: 交易 ID
            
        返回:
            緩存的數據，如果不存在則返回 None
        """
        cache_key = f"{coin}_tx_{txid}"
        if cache_key in self._investigation_cache:
            return self._investigation_cache[cache_key]['data']
        return None
    
    def get_investigation_summary(self) -> Dict[str, Any]:
        """
        獲取當前調查的摘要信息。
        
        返回:
            包含調查摘要信息的字典
        """
        return {
            'addresses_investigated': list(self._addresses_investigated),
            'transactions_analyzed': list(self._transactions_analyzed),
            'cache_size': len(self._investigation_cache),
            'state_keys': list(self._state.keys()),
            'graph_files': list(self._graph_files.keys())
        }
        
    def save_graph_to_file(self, png_bytes: bytes, description: str = "") -> str:
        """
        將圖像保存到臨時文件，並返回訪問URL
        
        參數:
            png_bytes: 圖像的二進制數據
            description: 圖像描述
            
        返回:
            文件路徑
        """
        file_id = str(uuid.uuid4())
        file_name = f"graph_{file_id}.png"
        file_path = os.path.join(self._temp_dir, file_name)
        
        with open(file_path, 'wb') as f:
            f.write(png_bytes)
        
        # 保存映射關係
        self._graph_files[file_id] = file_path
        
        # 返回文件標識符
        return file_id
        
    def get_graph_file_path(self, file_id: str) -> Optional[str]:
        """
        根據文件ID獲取文件路徑
        
        參數:
            file_id: 文件標識符
            
        返回:
            文件路徑，如不存在則返回None
        """
        return self._graph_files.get(file_id)
    
    def transform_misttrack_data(self, misttrack_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        將 MistTrack 交易數據轉換為圖形代理所需的格式。
        
        圖形代理所需格式：
        [
            {
                "from": "0x123...",  # 發送地址
                "to": "0x456...",    # 接收地址
                "value": "1.23",     # 交易價值
                "ts": "2023-04-01 12:34:56"  # 時間戳
            },
            ...
        ]
        """
        edges = []
        if not misttrack_data or "data" not in misttrack_data:
            return edges
            
        # 從 MistTrack 響應中提取交易
        try:
            transactions = misttrack_data.get("data", {}).get("transactions", [])
            for tx in transactions:
                # 檢查交易是否包含所需字段
                if all(k in tx for k in ["from_address", "to_address", "value", "timestamp"]):
                    edge = {
                        "from": tx["from_address"],
                        "to": tx["to_address"],
                        "value": str(tx.get("value", "0")),
                        "ts": tx.get("timestamp", "")
                    }
                    edges.append(edge)
                    
                    # 將此交易添加到已分析交易列表中
                    if "hash" in tx:
                        self._transactions_analyzed.add(tx["hash"])
        except Exception as e:
            print(f"轉換交易數據時出錯: {e}")
            
        return edges

# 全局會話狀態實例
session_state = SessionState()