"""
SSI Financial module for retrieving financial reports and data.
"""

import pandas as pd
import requests
from typing import Optional, Dict, Any
from io import BytesIO

from vnstock.explorer.ssi.const import _FUNDAMENTAL_URL, DEFAULT_HEADERS, FINANCIAL_REPORT_TYPES, FINANCIAL_FREQUENCIES
from vnstock.core.utils.logger import get_logger
from vnstock.core.utils.user_agent import get_headers
from vnstock.core.utils.validation import validate_symbol
from vnai import optimize_execution

logger = get_logger(__name__)


class Finance:
    """
    SSI data source for financial reports and analysis.
    """
    
    def __init__(self, symbol: str, random_agent: Optional[bool] = False, show_log: bool = False):
        """
        Initialize Financial instance for SSI data source.
        
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
    def balance_sheet(
        self, 
        frequency: str = 'Quarterly', 
        **kwargs
    ) -> pd.DataFrame:
        """
        Get balance sheet report from SSI.
        
        Args:
            frequency: 'Quarterly' or 'Yearly'
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with balance sheet data
        """
        return self._get_financial_report('BalanceSheet', frequency)
    
    @optimize_execution("SSI")
    def income_statement(
        self, 
        frequency: str = 'Quarterly', 
        **kwargs
    ) -> pd.DataFrame:
        """
        Get income statement from SSI.
        
        Args:
            frequency: 'Quarterly' or 'Yearly'
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with income statement data
        """
        return self._get_financial_report('IncomeStatement', frequency)
    
    @optimize_execution("SSI")
    def cash_flow(
        self, 
        frequency: str = 'Quarterly', 
        **kwargs
    ) -> pd.DataFrame:
        """
        Get cash flow statement from SSI.
        
        Args:
            frequency: 'Quarterly' or 'Yearly'
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with cash flow data
        """
        return self._get_financial_report('CashFlow', frequency)
    
    @optimize_execution("SSI")
    def ratio(
        self, 
        symbol_list: Optional[list] = None,
        industry_comparison: bool = True,
        frequency: str = 'Yearly',
        start_year: int = 2010,
        **kwargs
    ) -> pd.DataFrame:
        """
        Get financial ratios comparison from SSI.
        
        Args:
            symbol_list: List of symbols to compare (defaults to [self.symbol])
            industry_comparison: Include industry comparison
            frequency: 'Yearly' or 'Quarterly'
            start_year: Starting year for data
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with financial ratios
        """
        if symbol_list is None:
            symbol_list = [self.symbol]
        
        main_symbol = symbol_list[0]
        
        # Build comparison symbols parameter
        company_join = ""
        if len(symbol_list) > 1:
            for symbol in symbol_list[1:]:
                company_join += f"&CompareToCompanies={symbol}"
        
        # Build ratios parameters - using common financial ratios
        ratios = [
            'ryd21', 'ryd25', 'ryd14', 'ryd7', 'rev', 'isa22', 'ryq44', 
            'ryq14', 'ryq12', 'rtq51', 'rtq50', 'ryq48', 'ryq47', 'ryq45', 
            'ryq46', 'ryq54', 'ryq55', 'ryq56', 'ryq57', 'nob151', 'casa'
        ]
        
        ratios_params = "&".join([f"Ratios={ratio}" for ratio in ratios])
        
        url = f"{_FUNDAMENTAL_URL}/FinancialAnalysis/DownloadFinancialRatio2"
        
        params = (
            f"language=vi&OrganCode={main_symbol}&CompareToIndustry={str(industry_comparison).lower()}"
            f"{company_join}&Frequency={frequency}&{ratios_params}"
        )
        
        headers = self._get_headers()
        
        try:
            response = requests.get(f"{url}?{params}", headers=headers, timeout=30)
            response.raise_for_status()
            
            # SSI returns Excel file
            df = pd.read_excel(BytesIO(response.content), skiprows=7)
            
            # Clean up the data
            df = df.dropna(how='all')
            
            # Remove SSI attribution rows
            if 'Chỉ số' in df.columns:
                df = df[~df['Chỉ số'].str.contains('Dữ liệu được cung cấp bởi FiinTrade', na=False)]
                df = df[~df['Chỉ số'].str.contains('https://fiintrade.vn/', na=False)]
            
            if self.show_log:
                logger.info(f"Retrieved financial ratios for {symbol_list}")
            
            return df
            
        except requests.RequestException as e:
            logger.error(f"Error fetching financial ratios from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI financial ratios: {e}")
            return pd.DataFrame()
    
    def _get_financial_report(self, report_type: str, frequency: str) -> pd.DataFrame:
        """
        Get financial report from SSI.
        
        Args:
            report_type: Type of report (BalanceSheet, IncomeStatement, CashFlow)
            frequency: Frequency (Quarterly, Yearly)
            
        Returns:
            DataFrame with financial report data
        """
        if report_type not in FINANCIAL_REPORT_TYPES:
            raise ValueError(f"Report type {report_type} not supported. Use: {list(FINANCIAL_REPORT_TYPES.keys())}")
        
        if frequency not in FINANCIAL_FREQUENCIES:
            raise ValueError(f"Frequency {frequency} not supported. Use: {list(FINANCIAL_FREQUENCIES.keys())}")
        
        url = f"{_FUNDAMENTAL_URL}/FinancialStatement/Download{report_type}"
        
        params = {
            'language': 'vi',
            'OrganCode': self.symbol,
            'Skip': 0,
            'Frequency': frequency
        }
        
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            # SSI returns Excel file
            df = pd.read_excel(BytesIO(response.content), skiprows=7)
            df = df.dropna(how='all')
            
            if self.show_log:
                logger.info(f"Retrieved {report_type} report for {self.symbol} ({frequency})")
            
            return df
            
        except requests.RequestException as e:
            logger.error(f"Error fetching {report_type} from SSI: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error processing SSI {report_type}: {e}")
            return pd.DataFrame()
