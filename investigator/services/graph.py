from typing import List, Dict, Union
import base64
from graphviz import Digraph

def render_tx_graph(
    edges: List[Dict[str, str]]
) -> str:
    """
    渲染鏈上交易流圖。

    參數:
      edges: 字典列表，每個字典包含以下鍵:
        - from   (str): 發送方地址
        - to     (str): 接收方地址
        - value  (str): ETH 金額
        - ts     (str): 時間戳字符串

    返回:
      Base64編碼的PNG圖像，可在Markdown中顯示。
    """
    dot = Digraph(format="png")
    dot.attr(rankdir="LR", fontsize="12")

    # 添加帶標籤的邊
    for e in edges:
        dot.node(e["from"], shape="oval")
        dot.node(e["to"],   shape="oval")
        label = f'{e["value"]} ETH\n{e["ts"]}'
        dot.edge(e["from"], e["to"], label=label, fontsize="10")

    # 獲取PNG字節數據
    png_bytes = dot.pipe()
    
    # 將字節轉換為Base64編碼的字符串
    base64_str = base64.b64encode(png_bytes).decode('utf-8')
    
    # 返回可在Markdown中顯示的格式
    return f"![交易圖](data:image/png;base64,{base64_str})"