# SSI Data Source Integration

This document explains how to use the newly integrated SSI data source in vnstock.

## Overview

SSI (SSI Securities Corporation) is now available as a data source in vnstock, providing access to Vietnam stock market data through SSI's APIs. This integration is based on the implementation from the [tuanphongpham/vnstock](https://github.com/tuanphongpham/vnstock) repository.

## Features

The SSI data source provides the following functionality:

### 1. Quote Data
- Historical price data (OHLC)
- Intraday trading data
- Price depth/order book data

### 2. Listing Data
- All stock symbols
- Industry classifications
- Market listings

### 3. Financial Data
- Balance sheet reports
- Income statements
- Cash flow statements
- Financial ratios with industry comparison

### 4. Company Data
- Company overview and profile
- Shareholders information
- Company events and news
- Dividend information

### 5. Trading Data
- Price board for multiple symbols
- Market top movers
- Foreign trading heatmap
- Market indices

## Usage Examples

### Using the StockComponents wrapper

```python
from vnstock.common.data.data_explorer import StockComponents

# Initialize SSI stock component
stock = StockComponents(symbol='VCI', source='SSI')

# Get historical price data
hist_data = stock.quote.history(start='2024-01-01', end='2024-12-31')

# Get company information
company_info = stock.company.overview()

# Get financial reports
balance_sheet = stock.finance.balance_sheet(frequency='Quarterly')
income_statement = stock.finance.income_statement(frequency='Yearly')

# Get market listings
all_symbols = stock.listing.all_symbols()
```

### Using the API classes directly

```python
from vnstock.api.quote import Quote
from vnstock.api.company import Company
from vnstock.api.financial import Finance
from vnstock.api.listing import Listing
from vnstock.api.trading import Trading

# Quote data
quote = Quote(source='ssi', symbol='VCI')
price_data = quote.history(start='2024-01-01', end='2024-12-31')
intraday_data = quote.intraday(page_size=100)

# Company data
company = Company(source='ssi', symbol='VCI')
overview = company.overview()

# Financial data
finance = Finance(source='ssi', symbol='VCI')
balance_sheet = finance.balance_sheet(frequency='Quarterly')

# Listing data
listing = Listing(source='ssi')
symbols = listing.all_symbols()

# Trading data
trading = Trading(source='ssi', symbol='VCI')
price_board = trading.price_board(['VCI', 'VCB', 'TCB'])
```

## API Endpoints

The SSI integration uses the following API endpoints:

- **Base URL**: `https://fiin-market.ssi.com.vn`
- **Fundamental URL**: `https://fiin-fundamental.ssi.com.vn`
- **Core URL**: `https://fiin-core.ssi.com.vn`
- **iBoard URL**: `https://iboard-query.ssi.com.vn`

## Implementation Notes

### Data Frequency
- SSI primarily supports daily data (1D interval)
- Historical data is available with customizable date ranges
- Intraday data provides recent trading activity

### Financial Reports
- Supports both Quarterly and Yearly frequency
- Returns data in Vietnamese language by default
- Excel-based reports are automatically parsed into DataFrames

### Headers and Authentication
- Uses standard web browser headers
- No special authentication required for basic endpoints
- Rate limiting may apply based on SSI's policies

### Error Handling
- Comprehensive error handling for network issues
- Graceful fallback for missing data
- Informative logging for debugging

## Limitations

1. **Real-time Data**: SSI endpoints may have delays compared to real-time feeds
2. **Rate Limits**: SSI may impose rate limits on API usage
3. **Data Availability**: Some advanced features may not be fully implemented yet
4. **Language**: Most data is returned in Vietnamese

## Migration from Original Repository

This implementation is based on the SSI functionality from the [tuanphongpham/vnstock](https://github.com/tuanphongpham/vnstock) repository. Key improvements include:

1. **Modern Architecture**: Follows vnstock 3.x architecture patterns
2. **Better Error Handling**: More robust error handling and logging
3. **Consistent API**: Matches the interface of other vnstock data sources
4. **Type Hints**: Improved code documentation with type annotations
5. **Configurable Options**: More flexible configuration options

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
2. **Network Timeouts**: SSI servers may be slow; increase timeout values if needed
3. **Empty DataFrames**: Check if the requested symbol/date range has data available
4. **Authentication Errors**: SSI may require specific headers for some endpoints

### Debug Mode

Enable logging to see detailed API calls:

```python
import logging
logging.basicConfig(level=logging.INFO)

stock = StockComponents(symbol='VCI', source='SSI', show_log=True)
```

## Future Enhancements

Planned improvements for the SSI data source:

1. **Complete API Coverage**: Implement remaining SSI endpoints
2. **Real-time Data**: Add support for streaming data if available
3. **Caching**: Implement intelligent caching for frequently requested data
4. **Performance**: Optimize API calls and data processing
5. **Documentation**: Add more comprehensive examples and tutorials

## Contributing

To contribute improvements to the SSI data source:

1. Check the existing implementation in `vnstock/explorer/ssi/`
2. Follow the established patterns from other data sources
3. Add appropriate tests for new functionality
4. Update documentation as needed

## References

- [Original SSI Implementation](https://github.com/tuanphongpham/vnstock)
- [SSI Securities Corporation](https://www.ssi.com.vn/)
- [SSI iBoard Platform](https://iboard.ssi.com.vn/)
- [vnstock Documentation](https://vnstocks.com/docs/)
