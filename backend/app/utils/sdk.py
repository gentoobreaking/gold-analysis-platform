"""
Gold Analysis Platform SDK
提供給第三方應用的 Python SDK
"""
import httpx
from datetime import date
from typing import Optional, List, Dict, Any


class GoldAnalysisClient:
    """Gold Analysis Platform API Client"""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.gold-analysis.example.com/v1"
    ):
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
    
    def get_price(self) -> Dict[str, Any]:
        """獲取當前金價"""
        resp = self._client.get("/market/price")
        resp.raise_for_status()
        return resp.json()
    
    def get_history(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """獲取歷史價格"""
        resp = self._client.get(
            "/market/history",
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )
        resp.raise_for_status()
        return resp.json()
    
    def get_technical_analysis(self) -> Dict[str, Any]:
        """獲取技術分析"""
        resp = self._client.get("/analysis/technical")
        resp.raise_for_status()
        return resp.json()
    
    def get_decision(self) -> Dict[str, Any]:
        """獲取交易決策"""
        resp = self._client.get("/decision/recommend")
        resp.raise_for_status()
        return resp.json()
    
    def list_portfolios(self) -> List[Dict[str, Any]]:
        """列出投資組合"""
        resp = self._client.get("/portfolio")
        resp.raise_for_status()
        return resp.json()
    
    def create_portfolio(
        self,
        name: str,
        initial_capital: float
    ) -> Dict[str, Any]:
        """創建投資組合"""
        resp = self._client.post(
            "/portfolio",
            json={
                "name": name,
                "initial_capital": initial_capital
            }
        )
        resp.raise_for_status()
        return resp.json()
    
    def create_alert(
        self,
        alert_type: str,
        target_price: float,
        channels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """創建價格告警"""
        resp = self._client.post(
            "/alert",
            json={
                "type": alert_type,
                "target_price": target_price,
                "channels": channels or ["push"]
            }
        )
        resp.raise_for_status()
        return resp.json()
    
    def close(self):
        """關閉客戶端"""
        self._client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# 使用範例
if __name__ == "__main__":
    # 初始化客戶端
    client = GoldAnalysisClient(api_key="your_api_key_here")
    
    try:
        # 獲取當前金價
        price = client.get_price()
        print(f"當前金價: {price['price']} {price['currency']}")
        
        # 獲取技術分析
        analysis = client.get_technical_analysis()
        print(f"RSI: {analysis['indicators']['rsi']}")
        
        # 獲取交易決策
        decision = client.get_decision()
        print(f"推薦: {decision['action']} (信心度: {decision['confidence']}%)")
        
    finally:
        client.close()
