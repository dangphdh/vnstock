"""
SSI Quote module for retrieving stock price data.
"""

import pandas as pd
import requests
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from io import BytesIO

from vnstock.explorer.ssi.const import (
    _BASE_URL, _IBOARD_URL, DEFAULT_HEADERS, _OHLC_MAP, _OHLC_DTYPE, 
    SUPPORTED_INTERVALS
)
from vnstock.core.utils.logger import get_logger
from vnstock.core.utils.user_agent import get_headers
from vnstock.core.utils.validation import validate_symbol
from vnstock.core.utils.parser import get_asset_type
from vnstock.core.utils import transform
from vnai import optimize_execution

logger = get_logger(__name__)


class Quote:
    """
    SSI data source for fetching stock market data.
    """
    
    def __init__(self, symbol: str, random_agent: Optional[bool] = False, show_log: bool = False):
        """
        Initialize Quote instance for SSI data source.
        
        Args:
            symbol: Stock symbol to query
            random_agent: Whether to use random user agent
            show_log: Whether to show logs
        """
        self.symbol = validate_symbol(symbol)
        self.data_source = "SSI"
        self.asset_type = get_asset_type(symbol)
        self.random_agent = random_agent
        self.show_log = show_log
        
        if not show_log:
            logger.setLevel(40)  # ERROR level
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        if self.random_agent:
            return get_headers(self.random_agent)
        return DEFAULT_HEADERS.copy()
    
    @optimize_execution('SSI')
    def history(
        self, 
        start: str, 
        end: Optional[str] = None,
        interval: str = "1D",
        to_df: bool = True,
        show_log: bool = False,
        count_back: Optional[int] = 365,
        asset_type: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Retrieve historical stock price data from SSI.
        
        Args:
            start: Start date in YYYY-MM-DD format
            end: End date in YYYY-MM-DD format  
            interval: Time interval (only '1D' supported)
            to_df: Return as DataFrame
            show_log: Show logs
            count_back: Number of records to return
            asset_type: Asset type override
            
        Returns:
            DataFrame with OHLC data
        """
        if interval not in SUPPORTED_INTERVALS:
            raise ValueError(f"Interval {interval} not supported. Use: {SUPPORTED_INTERVALS}")
        
        if not end:
            end = datetime.now().strftime('%Y-%m-%d')
        
        # Convert dates
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        
        # SSI uses timestamps in milliseconds
        start_ts = int(start_date.timestamp() * 1000)
        end_ts = int(end_date.timestamp() * 1000)
        
        url = f"{_IBOARD_URL}/stock/{self.symbol.lower()}/historical-quotes"
        
        params = {
            'startDate': start_ts,
            'endDate': end_ts,
            'pageIndex': 1,
            'pageSize': 1000
        }
        
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                df = self._process_history_data(data['data'])
                
                if count_back:
                    df = df.tail(count_back)
                
                df.source = self.data_source
                df.category = self.asset_type
                df.name = self.symbol
                
                if show_log:
                    logger.info(f"Retrieved {len(df)} records for {self.symbol} from {start} to {end}")
                
                return df if to_df else data
            else:
                logger.warning(f"No data available for {self.symbol}")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching data from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI data: {e}")
            return pd.DataFrame()
    
    def _process_history_data(self, data: list) -> pd.DataFrame:
        """Process historical data from SSI API."""
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Map columns
        df = df.rename(columns=_OHLC_MAP)
        
        # Ensure required columns exist
        required_cols = ['time', 'open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0
        
        # Convert time from timestamp to datetime
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'], unit='ms', utc=True)
            df['time'] = df['time'].dt.tz_convert('Asia/Ho_Chi_Minh')
            df['time'] = df['time'].dt.tz_localize(None)
            df['time'] = df['time'].dt.date
        
        # Convert data types
        for col, dtype in _OHLC_DTYPE.items():
            if col in df.columns and col != 'time':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sort by time
        df = df.sort_values('time').reset_index(drop=True)
        
        # Select only required columns
        df = df[required_cols]
        
        return df
    
    @optimize_execution('SSI') 
    def intraday(
        self,
        page_size: int = 100,
        page: int = 0,
        to_df: bool = True,
        show_log: bool = False
    ) -> pd.DataFrame:
        """
        Get intraday trading data from SSI.
        
        Args:
            page_size: Number of records per page
            page: Page number
            to_df: Return as DataFrame
            show_log: Show logs
            
        Returns:
            DataFrame with intraday trading data
        """
        url = f"{_IBOARD_URL}/stock/{self.symbol.lower()}/intraday-trades"
        
        params = {
            'pageIndex': page,
            'pageSize': page_size
        }
        
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                if to_df:
                    df = pd.DataFrame(data['data'])
                    
                    # Process intraday data
                    if 'time' in df.columns:
                        df['time'] = pd.to_datetime(df['time'], unit='ms')
                    
                    df.source = self.data_source
                    df.category = self.asset_type
                    
                    if show_log:
                        logger.info(f"Retrieved {len(df)} intraday records for {self.symbol}")
                    
                    return df
                else:
                    return data
            else:
                logger.warning(f"No intraday data available for {self.symbol}")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching intraday data from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI intraday data: {e}")
            return pd.DataFrame()
    
    @optimize_execution('SSI')
    def price_depth(
        self,
        to_df: bool = True,
        show_log: bool = False
    ) -> pd.DataFrame:
        """
        Get order book/price depth data from SSI.
        
        Args:
            to_df: Return as DataFrame
            show_log: Show logs
            
        Returns:
            DataFrame with order book data
        """
        url = f"{_IBOARD_URL}/stock/{self.symbol.lower()}/price-depth"
        
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if to_df and data:
                # Convert to DataFrame - structure depends on SSI API response
                if 'data' in data:
                    df = pd.DataFrame(data['data'])
                else:
                    df = pd.DataFrame([data])
                
                df.source = self.data_source
                df.category = self.asset_type
                
                if show_log:
                    logger.info(f"Retrieved price depth data for {self.symbol}")
                
                return df
            else:
                return data
                
        except requests.RequestException as e:
            logger.error(f"Error fetching price depth from SSI: {e}")
            return pd.DataFrame() if to_df else {}
        except Exception as e:
            logger.error(f"Error processing SSI price depth data: {e}")
            return pd.DataFrame() if to_df else {}

# example usage
if __name__ == "__main__":
    quote = Quote(symbol="VCI")
    df = quote.intraday_trades()
    print(df)