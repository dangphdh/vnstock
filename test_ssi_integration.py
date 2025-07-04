#!/usr/bin/env python3
"""
Simple test script to verify SSI data source integration.
"""

import sys
import os

# Add the project root to path so we can import vnstock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_ssi_integration():
    """Test SSI data source integration."""
    print("Testing SSI data source integration...")
    
    try:
        # Test 1: Initialize SSI stock component
        try:
            from vnstock.common.data.data_explorer import StockComponents
            ssi_stock = StockComponents(symbol='VCI', source='SSI')
            print("✓ SSI StockComponents initialization successful")
            print(f"  - Symbol: {ssi_stock.symbol}")
            print(f"  - Source: {ssi_stock.source}")
            print(f"  - Quote available: {ssi_stock.quote is not None}")
            print(f"  - Listing available: {ssi_stock.listing is not None}")
            print(f"  - Trading available: {ssi_stock.trading is not None}")
            print(f"  - Company available: {ssi_stock.company is not None}")
            print(f"  - Finance available: {ssi_stock.finance is not None}")
            print(f"  - Screener available: {ssi_stock.screener is not None}")
        except Exception as e:
            print(f"✗ SSI StockComponents initialization failed: {e}")
            return False
        
        # Test 2: Test Quote API imports
        try:
            from vnstock.api.quote import Quote as APIQuote
            api_quote = APIQuote(source='ssi', symbol='VCI')
            print("✓ SSI Quote API initialization successful")
        except Exception as e:
            print(f"✗ SSI Quote API initialization failed: {e}")
            return False
        
        # Test 3: Test other API imports
        try:
            from vnstock.api.company import Company as APICompany
            api_company = APICompany(source='ssi', symbol='VCI')
            print("✓ SSI Company API initialization successful")
        except Exception as e:
            print(f"✗ SSI Company API initialization failed: {e}")
            return False
        
        try:
            from vnstock.api.financial import Finance as APIFinance
            api_finance = APIFinance(source='ssi', symbol='VCI')
            print("✓ SSI Financial API initialization successful")
        except Exception as e:
            print(f"✗ SSI Financial API initialization failed: {e}")
            return False
        
        try:
            from vnstock.api.listing import Listing as APIListing
            api_listing = APIListing(source='ssi')
            print("✓ SSI Listing API initialization successful")
        except Exception as e:
            print(f"✗ SSI Listing API initialization failed: {e}")
            return False
        
        try:
            from vnstock.api.trading import Trading as APITrading
            api_trading = APITrading(source='ssi', symbol='VCI')
            print("✓ SSI Trading API initialization successful")
        except Exception as e:
            print(f"✗ SSI Trading API initialization failed: {e}")
            return False
        
        print("\n🎉 All SSI data source integration tests passed!")
        print("\nSSI data source has been successfully added to vnstock.")
        print("You can now use SSI as a data source in vnstock APIs:")
        print("  - Quote(source='ssi', symbol='VCI')")
        print("  - Company(source='ssi', symbol='VCI')")
        print("  - Finance(source='ssi', symbol='VCI')")
        print("  - Listing(source='ssi')")
        print("  - Trading(source='ssi', symbol='VCI')")
        print("  - StockComponents(symbol='VCI', source='SSI')")
        
        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure vnstock dependencies are installed: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = test_ssi_integration()
    sys.exit(0 if success else 1)
