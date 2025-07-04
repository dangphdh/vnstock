# VND Data Source

This module provides access to Vietnamese stock market data from VNDIRECT (vndirect.com.vn) using their public API.

## Features
- Fetch historical daily prices for a given stock symbol
- Retrieve company information

## Example Usage
```python
from vnstock.connector.vnd.vnd import VND
vnd = VND()
# Get historical prices for VCB
prices = vnd.get_stock_prices('VCB', start_date='2024-01-01', end_date='2024-06-30')
# Get company info for VCB
info = vnd.get_company_info('VCB')
```

## API Reference
- [VNDIRECT API Docs](https://api.vndirect.com.vn/docs/)
