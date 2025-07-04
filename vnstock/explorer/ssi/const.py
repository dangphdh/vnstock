"""
Constants and configuration for SSI data source.
"""

# SSI API endpoints
_BASE_URL = "https://fiin-market.ssi.com.vn"
_FUNDAMENTAL_URL = "https://fiin-fundamental.ssi.com.vn"
_CORE_URL = "https://fiin-core.ssi.com.vn"
_IBOARD_URL = "https://iboard-query.ssi.com.vn"

# Default headers for SSI API requests
DEFAULT_HEADERS = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'X-Fiin-Key': 'KEY',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Fiin-User-ID': 'ID',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'X-Fiin-Seed': 'SEED',
    'sec-ch-ua-platform': 'Windows',
    'Origin': 'https://iboard.ssi.com.vn',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://iboard.ssi.com.vn/',
    'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7'
}

# OHLC column mapping for SSI data
_OHLC_MAP = {
    'tradingDate': 'time',
    'priceOpen': 'open', 
    'priceHigh': 'high',
    'priceLow': 'low',
    'priceClose': 'close',
    'totalVolume': 'volume'
}

# Data type mapping for OHLC data
_OHLC_DTYPE = {
    'time': 'datetime64[ns]',
    'open': 'float64',
    'high': 'float64', 
    'low': 'float64',
    'close': 'float64',
    'volume': 'int64'
}

# Trading data column mapping
_TRADING_MAP = {
    'p': 'price',
    'v': 'volume', 
    't': 'time',
    's': 'side'  # Buy/Sell
}

# Supported frequencies for historical data
SUPPORTED_INTERVALS = ['1D']  # SSI primarily supports daily data

# Financial report types
FINANCIAL_REPORT_TYPES = {
    'BalanceSheet': 'Bảng cân đối kế toán',
    'IncomeStatement': 'Báo cáo kết quả kinh doanh', 
    'CashFlow': 'Báo cáo lưu chuyển tiền tệ'
}

# Financial report frequencies
FINANCIAL_FREQUENCIES = {
    'Quarterly': 'Theo quý',
    'Yearly': 'Theo năm'
}

# Supported languages
SUPPORTED_LANGUAGES = ['vi', 'en']

# Market exchanges
EXCHANGES = ['All', 'HOSE', 'HNX', 'UPCOM']

# Index codes
INDEX_CODES = [
    'VNINDEX', 'VN30', 'HNXIndex', 'HNX30', 'UpcomIndex', 'VNXALL',
    'VN100', 'VNALL', 'VNCOND', 'VNCONS', 'VNDIAMOND', 'VNENE', 'VNFIN',
    'VNFINLEAD', 'VNFINSELECT', 'VNHEAL', 'VNIND', 'VNIT', 'VNMAT', 'VNMID',
    'VNREAL', 'VNSI', 'VNSML', 'VNUTI', 'VNX50'
]
