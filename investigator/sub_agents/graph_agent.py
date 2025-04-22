from google.adk.agents import Agent
from investigator.services.graph import render_tx_graph
from investigator.services.state import session_state
from typing import List, Dict, Optional

async def render_stored_tx_graph(custom_edges: Optional[List[Dict[str, str]]] = None) -> str:
    """
    使用提供的邊緣或存儲在會話狀態中的邊緣渲染交易圖。
    
    參數:
        custom_edges: 可選的自定義邊緣列表，用於代替存儲的數據進行渲染
        
    返回:
        包含Base64編碼PNG圖像的Markdown圖片字符串。
    """
    # 使用提供的邊緣或從會話狀態獲取
    edges = custom_edges if custom_edges else session_state.get_tx_data()
    
    # 確保我們有邊緣可以渲染
    if not edges:
        # 創建一個簡單的「無數據」圖
        no_data_edge = [
            {
                "from": "無交易",
                "to": "數據可用",
                "value": "0",
                "ts": ""
            }
        ]
        return render_tx_graph(no_data_edge)
    
    # 使用會話狀態中的邊緣渲染圖
    return render_tx_graph(edges)

graph_agent = Agent(
    model="gemini-2.0-flash",
    name="graph_agent",
    instruction=(
        "你是一個圖形渲染助手。你可以：\n"
        "1. 使用 `render_tx_graph` 從直接提供的邊緣數據渲染圖\n"
        "2. 使用 `render_stored_tx_graph` 從先前存儲的交易數據渲染圖\n\n"
        "當交易數據已由 misttrack_agent 存儲時，你可以通過調用 "
        "`render_stored_tx_graph` 而不提供任何參數來將其可視化。這將使用已存儲的交易數據。\n\n"
        "如果給定自定義邊緣數據，請使用 `render_tx_graph` 工具或將自定義邊緣提供給 `render_stored_tx_graph`。"
    ),
    description="從 JSON 邊緣數據或存儲的會話狀態渲染交易流圖。",
    tools=[render_tx_graph, render_stored_tx_graph],
)
