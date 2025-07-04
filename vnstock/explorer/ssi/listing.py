"""
SSI Listing module for retrieving market listing data.
"""

import pandas as pd
import requests
from typing import Optional, Dict, Any
from pandas import json_normalize

from vnstock.explorer.ssi.const import _CORE_URL, DEFAULT_HEADERS, SUPPORTED_LANGUAGES, EXCHANGES
from vnstock.core.utils.logger import get_logger
from vnstock.core.utils.user_agent import get_headers
from vnai import optimize_execution

logger = get_logger(__name__)


class Listing:
    """
    SSI data source for market listing information.
    """
    
    def __init__(self, random_agent: Optional[bool] = False, show_log: bool = False):
        """
        Initialize Listing instance for SSI data source.
        
        Args:
            random_agent: Whether to use random user agent
            show_log: Whether to show logs
        """
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
    def all_symbols(self, lang: str = 'vi', **kwargs) -> pd.DataFrame:
        """
        Return a DataFrame of all available stock symbols from SSI.
        
        Args:
            lang: Language for the data ('vi' or 'en')
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with all stock symbols
        """
        if lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language {lang} not supported. Use: {SUPPORTED_LANGUAGES}")
        
        url = f"{_CORE_URL}/Master/GetListOrganization"
        params = {'language': lang}
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' in data:
                df = pd.DataFrame(data['items'])
                
                if self.show_log:
                    logger.info(f"Retrieved {len(df)} stock symbols from SSI")
                    logger.info(f"Total companies: {data.get('totalCount', len(df))}")
                
                return df
            else:
                logger.warning("No stock symbols data available from SSI")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching stock symbols from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI stock symbols data: {e}")
            return pd.DataFrame()
    
    @optimize_execution("SSI")
    def symbols_by_industries(self, **kwargs) -> pd.DataFrame:
        """
        Get stocks organized by industry classification.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with stocks by industry
        """
        # This would use SSI's industry classification endpoint
        # Implementation depends on specific SSI API structure
        logger.warning("symbols_by_industries not yet implemented for SSI source")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def symbols_by_exchange(self, **kwargs) -> pd.DataFrame:
        """
        Get stocks organized by exchange.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with stocks by exchange
        """
        # Get all symbols first, then group by exchange
        df = self.all_symbols(**kwargs)
        
        if not df.empty and 'comGroupCode' in df.columns:
            # Group by exchange
            return df.groupby('comGroupCode').apply(lambda x: x).reset_index(drop=True)
        
        return df
    
    @optimize_execution("SSI")
    def symbols_by_group(self, group: str = 'VN30', **kwargs) -> pd.DataFrame:
        """
        Get stocks by index group (VN30, HNX30, etc.).
        
        Args:
            group: Index group name
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with stocks in the specified group
        """
        # This would use SSI's group/index endpoint
        logger.warning(f"symbols_by_group for {group} not yet implemented for SSI source")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def industries_icb(self, lang: str = 'vi', **kwargs) -> pd.DataFrame:
        """
        Return industry classification data.
        
        Args:
            lang: Language for the data
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with industry classifications
        """
        url = f"{_CORE_URL}/Master/GetAllCompanyGroup"
        params = {'language': lang}
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' in data:
                df = pd.DataFrame(data['items'])
                
                if not df.empty:
                    # Sort by order if available
                    if 'comGroupOrder' in df.columns:
                        df = df.sort_values(by='comGroupOrder').reset_index(drop=True)
                    
                    # Select relevant columns
                    relevant_cols = ['comGroupCode', 'parentComGroupCode', 'comGroupOrder']
                    df = df[[col for col in relevant_cols if col in df.columns]]
                
                if self.show_log:
                    logger.info(f"Retrieved {len(df)} industry classifications from SSI")
                
                return df
            else:
                logger.warning("No industry classification data available from SSI")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            logger.error(f"Error fetching industry classifications from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI industry data: {e}")
            return pd.DataFrame()
    
    @optimize_execution("SSI")
    def all_future_indices(self, **kwargs) -> pd.DataFrame:
        """
        Get all future indices.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with future indices
        """
        logger.warning("all_future_indices not yet implemented for SSI source")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def all_covered_warrant(self, **kwargs) -> pd.DataFrame:
        """
        Get all covered warrants.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with covered warrants
        """
        logger.warning("all_covered_warrant not yet implemented for SSI source")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def all_bonds(self, **kwargs) -> pd.DataFrame:
        """
        Get all bonds.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with bonds
        """
        logger.warning("all_bonds not yet implemented for SSI source")
        return pd.DataFrame()
    
    @optimize_execution("SSI")
    def all_government_bonds(self, **kwargs) -> pd.DataFrame:
        """
        Get all government bonds.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with government bonds
        """
        logger.warning("all_government_bonds not yet implemented for SSI source")
        return pd.DataFrame()
