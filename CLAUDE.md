# CLAUDE.md - 代理指南

## 開發命令
```bash
# 安裝依賴
pip install -r requirements.txt

# 使用 ADK web 服務器運行代理（推薦）
adk web

# 直接運行代理模塊（不推薦）
python -m investigator.agent

# 代碼檢查
python -m ruff check .

# 類型檢查
mypy investigator
```

## 代碼風格指南
- **導入**: 標準庫優先，第三方庫其次，項目導入最後
- **類型提示**: 全面使用，特別是函數參數和返回值
- **命名**: 函數/變量使用 snake_case，常量使用 UPPER_CASE
- **文檔**: 使用三引號的文檔字符串，包括描述和參數/返回部分
- **錯誤處理**: 在適當情況下返回帶有錯誤消息的字典
- **縮進**: 4個空格，運算符周圍保持一致的空格
- **行長**: 保持合理，避免過長的行

## 項目結構
- **服務**: `investigator/services` 中的 API 接口，包括會話狀態管理
- **子代理**: `investigator/sub_agents` 中的代理定義
- **根代理**: 在 `investigator/agent.py` 中定義

## 會話狀態和緩存系統
- 使用 `session_state` 從 `investigator.services.state` 在代理之間共享數據和緩存結果
- 通用數據緩存:
  - 使用 `cache_address_data` 和 `get_cached_address_data` 緩存和檢索地址數據
  - 使用 `cache_transaction_data` 和 `get_cached_transaction_data` 緩存和檢索交易數據
  - 使用 `get_investigation_summary` 獲取當前調查概覽
- 增強版 API 函數:
  - 所有帶 `_cached` 後綴的函數會自動緩存結果
  - 例如 `get_address_labels_cached`, `get_risk_score_cached` 等
- 交易可視化工作流:
  1. 使用 misttrack_agent 中的 `get_transactions_and_store` 緩存交易數據
  2. 使用 graph_agent 中的 `render_stored_tx_graph` 可視化緩存的數據

## 性能優化
- 首次查詢地址時使用帶 `_cached` 後綴的函數
- 重複查詢相同地址時會自動使用緩存數據
- 所有緩存的數據在會話期間保持有效
- 可以使用 `get_investigation_summary` 查看已緩存的數據範圍

## 語言
- 所有用戶界面和輸出使用繁體中文
- 代碼注釋和文檔字符串也使用繁體中文