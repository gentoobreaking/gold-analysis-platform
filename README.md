# Gold Analysis Platform

黃金分析系統平台功能模組，提供對外 API、社區功能和移動端應用。

## 功能模塊

### 1. API 開發和文檔 (T001)

- RESTful API 端點
- OpenAPI 3.0 規格文檔
- API Key 認證
- 速率限制

### 2. 社區功能 (T002)

- 策略分享
- 用戶討論
- 內容審核

### 3. 移動端應用 (T003)

- React Native 應用
- iOS / Android 支持
- 推送通知

## API 端點

### 市場數據

- `GET /market/price` - 當前金價
- `GET /market/history` - 歷史價格

### 分析

- `GET /analysis/technical` - 技術分析
- `GET /decision/recommend` - 交易決策

### 用戶

- `GET /user/info` - 用戶信息

## 認證

所有 API 請求需要 Bearer Token：

```
Authorization: Bearer <your_api_key>
```

## 速率限制

| 方案 | 請求限制 |
|------|---------|
| 免費 | 100/小時 |
| 專業 | 1000/小時 |
| 企業 | 無限制 |

## SDK

### Python

```python
from app.utils.sdk import GoldAnalysisClient

client = GoldAnalysisClient(api_key="your_api_key")
price = client.get_price()
print(f"當前金價: {price['price']}")
```

## 技術棧

- FastAPI
- Python 3.9+
- React Native

## 快速開始

```bash
cd backend
pip install -r requirements.txt
python main.py
```

API 文檔: http://localhost:8002/docs

## 依賴

本專案依賴：

- gold-analysis-core: 核心分析功能
- gold-analysis-extend: 延伸功能（T003 多語言）

## 授權

MIT License
