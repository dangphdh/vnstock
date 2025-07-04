"""
DNSE Trading module for retrieving trading and account data.
"""

import pandas as pd
from typing import Optional
from vnstock.connector.dnse.trade import Trade as DnseTrade

class Trading:
    """
    DNSE data source for trading and account data.
    """
    def __init__(self, user_name: str, password: str):
        """
        Initialize Trading instance for DNSE data source.
        Args:
            user_name: DNSE username (account/email/phone)
            password: DNSE password
        """
        self.data_source = "DNSE"
        self._trade = DnseTrade()
        self.token = self._trade.login(user_name, password)
        if not self.token:
            raise ValueError("DNSE login failed. Check credentials.")

    def account(self) -> Optional[pd.DataFrame]:
        """Get the full user profile from DNSE."""
        return self._trade.account()

    def sub_accounts(self) -> Optional[pd.DataFrame]:
        """Get sub-accounts information."""
        return self._trade.sub_accounts()

    def account_balance(self, sub_account: str) -> Optional[pd.DataFrame]:
        """Get account balance for a specific sub-account."""
        return self._trade.account_balance(sub_account)

    def order_list(self, sub_account: str, asset_type: str = 'stock') -> Optional[pd.DataFrame]:
        """Get the list of orders for a specific account."""
        return self._trade.order_list(sub_account, asset_type)

    def order_detail(self, order_id: str, sub_account: str, asset_type: str = 'stock') -> Optional[pd.DataFrame]:
        """Get the details of a specific order for a specific sub account."""
        return self._trade.order_detail(order_id, sub_account, asset_type)

    def deals_list(self, sub_account: str, asset_type: str = 'stock') -> Optional[pd.DataFrame]:
        """Get the list of deals for a specific sub account."""
        return self._trade.deals_list(sub_account, asset_type)

    # Add more wrappers as needed for other DNSE Trade methods
