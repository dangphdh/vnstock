"""
SSI Company module for retrieving company information.
"""

import pandas as pd
import requests
from typing import Optional, Dict, Any

from vnstock.explorer.ssi.const import _CORE_URL, _FUNDAMENTAL_URL, DEFAULT_HEADERS
from vnstock.core.utils.logger import get_logger
from vnstock.core.utils.user_agent import get_headers
from vnstock.core.utils.validation import validate_symbol
from vnai import optimize_execution

logger = get_logger(__name__)


class Company:
    """
    SSI data source for company information.
    """
    
    def __init__(self, symbol: str, random_agent: Optional[bool] = False, show_log: bool = False):
        """
        Initialize Company instance for SSI data source.
        
        Args:
            symbol: Stock symbol
            random_agent: Whether to use random user agent
            show_log: Whether to show logs
        """
        self.symbol = validate_symbol(symbol)
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
    def overview(self, **kwargs) -> Dict[str, Any]:
        """
        Get company overview information from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with company overview data
        """
        # This would use SSI's company overview endpoint
        # Implementation depends on specific SSI API structure
        logger.warning(f"overview not yet implemented for SSI source for symbol {self.symbol}")
        return {}
    
    @optimize_execution("SSI")
    def profile(self, **kwargs) -> Dict[str, Any]:
        """
        Get company profile information from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with company profile data
        """
        # This would use SSI's company profile endpoint
        logger.warning(f"profile not yet implemented for SSI source for symbol {self.symbol}")
        return {}
    
    @optimize_execution("SSI")
    def shareholders(self, **kwargs) -> pd.DataFrame:
        """
        Get shareholders information from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with shareholders data
        """
        # This would use SSI's shareholders endpoint
        logger.warning(f"shareholders not yet implemented for SSI source for symbol {self.symbol}")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def insider_deals(self, **kwargs) -> pd.DataFrame:
        """
        Get insider trading information from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with insider deals data
        """
        logger.warning(f"insider_deals not yet implemented for SSI source for symbol {self.symbol}")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def subsidiaries(self, **kwargs) -> pd.DataFrame:
        """
        Get subsidiaries information from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with subsidiaries data
        """
        logger.warning(f"subsidiaries not yet implemented for SSI source for symbol {self.symbol}")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def officers(self, **kwargs) -> pd.DataFrame:
        """
        Get company officers information from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with officers data
        """
        logger.warning(f"officers not yet implemented for SSI source for symbol {self.symbol}")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def events(self, **kwargs) -> pd.DataFrame:
        """
        Get company events from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with events data
        """
        logger.warning(f"events not yet implemented for SSI source for symbol {self.symbol}")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def news(self, **kwargs) -> pd.DataFrame:
        """
        Get company news from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with news data
        """
        logger.warning(f"news not yet implemented for SSI source for symbol {self.symbol}")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def dividends(self, **kwargs) -> pd.DataFrame:
        """
        Get dividend information from SSI.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with dividend data
        """
        logger.warning(f"dividends not yet implemented for SSI source for symbol {self.symbol}")
        return pd.DataFrame()
