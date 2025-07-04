import requests
import pandas as pd
from pandas import json_normalize
from typing import Optional

class VND:
    """
    Data source for VNDIRECT (vndirect.com.vn) - provides stock data via public API.
    """
    BASE_URL = "https://finfo-api.vndirect.com.vn/v4"

    def get_stock_prices(self, symbol: str, start_date: str = None, end_date: str = None, limit: int = 100) -> Optional[pd.DataFrame]:
        """
        Get historical daily prices for a given stock symbol from VNDIRECT.

        Args:
            symbol (str): Stock symbol (e.g., 'VCB').
            start_date (str, optional): Start date in 'YYYY-MM-DD' format.
            end_date (str, optional): End date in 'YYYY-MM-DD' format.
            limit (int, optional): Number of records to fetch (default 100).

        Returns:
            Optional[pd.DataFrame]: DataFrame with price data, or None if failed.
        """
        url = f"{self.BASE_URL}/stock_prices"
        params = {
            "symbol": symbol,
            "sort": "date",
            "size": limit
        }
        if start_date:
            params["from"] = start_date.replace("-", "")
        if end_date:
            params["to"] = end_date.replace("-", "")
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            return pd.DataFrame(data)
        else:
            print(f"Error fetching prices: {response.text}")
            return None

    def get_company_info(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Get company information for a given stock symbol from VNDIRECT.

        Args:
            symbol (str): Stock symbol (e.g., 'VCB').

        Returns:
            Optional[pd.DataFrame]: DataFrame with company info, or None if failed.
        """
        url = f"{self.BASE_URL}/stocks"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            return pd.DataFrame(data)
        else:
            print(f"Error fetching company info: {response.text}")
            return None
