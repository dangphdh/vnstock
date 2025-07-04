"""
SSI Trading module for retrieving trading data and market information.
"""

import pandas as pd
import requests
from typing import Optional, Dict, Any, List

from vnstock.explorer.ssi.const import _BASE_URL, _IBOARD_URL, DEFAULT_HEADERS, EXCHANGES
from vnstock.core.utils.logger import get_logger
from vnstock.core.utils.user_agent import get_headers
from vnai import optimize_execution

logger = get_logger(__name__)


class Trading:
    """
    SSI data source for trading and market data.
    """
    
    def __init__(self, symbol: Optional[str] = None, random_agent: Optional[bool] = False, show_log: bool = False):
        """
        Initialize Trading instance for SSI data source.
        
        Args:
            symbol: Optional stock symbol
            random_agent: Whether to use random user agent
            show_log: Whether to show logs
        """
        self.symbol = symbol.upper() if symbol else None
        self.data_source = "SSI"
        self.random_agent = random_agent
        self.show_log = show_log
        
        if not show_log:
            logger.setLevel(40)  # ERROR level
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        if self.random_agent:
            return get_headers(self.random_agent)
        return DEFAULT_HEADERS.copy()
    
    @optimize_execution("SSI")
    def price_board(self, symbols_list: List[str], **kwargs) -> pd.DataFrame:
        """
        Get price board data for multiple symbols from SSI.
        
        Args:
            symbols_list: List of stock symbols
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with price board data
        """
        if not symbols_list:
            logger.warning("No symbols provided for price board")
            return pd.DataFrame()
        
        # Convert symbols to lowercase for SSI API
        symbols_str = ",".join([symbol.lower() for symbol in symbols_list])
        
        url = f"{_IBOARD_URL}/stock/price-board"
        params = {'symbols': symbols_str}
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                df = pd.DataFrame(data['data'])
                
                if self.show_log:
                    logger.info(f"Retrieved price board data for {len(symbols_list)} symbols")
                
                return df
            else:
                logger.warning("No price board data available")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching price board from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI price board data: {e}")
            return pd.DataFrame()
    
    @optimize_execution("SSI")
    def market_top_mover(
        self, 
        exchange: str = 'All',
        mover_type: str = 'TopGain',
        **kwargs
    ) -> pd.DataFrame:
        """
        Get top movers from SSI market data.
        
        Args:
            exchange: Exchange name ('All', 'HOSE', 'HNX', 'UPCOM')
            mover_type: Type of mover ('TopGain', 'TopLoss', 'TopValue', etc.)
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with top movers data
        """
        if exchange not in EXCHANGES:
            raise ValueError(f"Exchange {exchange} not supported. Use: {EXCHANGES}")
        
        url = f"{_BASE_URL}/TopMover/Get{mover_type}"
        params = {
            'language': 'vi',
            'ComGroupCode': exchange,
            'TimeRange': 'OneDay'  # Can be OneDay, OneWeek, OneMonth, etc.
        }
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' in data and data['items']:
                df = pd.DataFrame(data['items'])
                
                if self.show_log:
                    logger.info(f"Retrieved {mover_type} data for {exchange}")
                
                return df
            else:
                logger.warning(f"No {mover_type} data available for {exchange}")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching {mover_type} from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI {mover_type} data: {e}")
            return pd.DataFrame()
    
    @optimize_execution("SSI")
    def foreign_trade_heatmap(
        self, 
        exchange: str = 'HOSE',
        report_type: str = 'FrBuyVal',
        **kwargs
    ) -> pd.DataFrame:
        """
        Get foreign trading heatmap data from SSI.
        
        Args:
            exchange: Exchange or index name
            report_type: Type of report (FrBuyVal, FrSellVal, FrBuyVol, etc.)
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with foreign trading data
        """
        # Determine if it's an exchange or index group
        if exchange in ['All', 'HOSE', 'HNX', 'UPCOM']:
            url = f"{_IBOARD_URL}/stock/exchange/{exchange.lower()}"
        else:
            url = f"{_IBOARD_URL}/stock/group/{exchange.lower()}"
        
        params = {
            'language': 'vi',
            'Exchange': exchange,
            'Criteria': report_type
        }
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                df = pd.DataFrame(data['data'])
                
                if self.show_log:
                    logger.info(f"Retrieved foreign trade heatmap for {exchange} - {report_type}")
                
                return df
            else:
                logger.warning(f"No foreign trade heatmap data available")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching foreign trade heatmap from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI foreign trade data: {e}")
            return pd.DataFrame()
    
    @optimize_execution("SSI")
    def market_indices(self, **kwargs) -> pd.DataFrame:
        """
        Get latest market indices from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with market indices data
        """
        url = f"{_BASE_URL}/MarketInDepth/GetLatestIndices"
        params = {
            'language': 'vi',
            'pageSize': 999999,
            'status': 1
        }
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' in data and data['items']:
                df = pd.DataFrame(data['items'])
                
                if self.show_log:
                    logger.info(f"Retrieved market indices data")
                
                return df
            else:
                logger.warning("No market indices data available")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching market indices from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI market indices data: {e}")
            return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    trading = Trading(symbol="VCI")
    df = trading.foreign_trade_heatmap()
    print(df)
