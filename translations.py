# translations.py
# 独立翻译配置文件

TRANSLATIONS = {
    "en": {
        # 页面配置
        "page_title": "Financial Analysis",
        
        # 侧边栏
        "sidebar_title": "Financial Analysis",
        "ticker_label": "Enter a stock ticker (e.g. AAPL)",
        "period_label": "Select time frame",
        "period_options": ["1D", "5D", "1M", "6M", "YTD", "1Y", "5Y"],
        "submit_button": "Submit",
        
        # 表格标题
        "stock_info": "Stock Info",
        "price_info": "Price Info",
        "business_metrics": "Business Metrics",
        
        # 表格列名
        "country": "Country",
        "sector": "Sector",
        "industry": "Industry",
        "market_cap": "Market Cap",
        "enterprise_value": "Enterprise Value",
        "employees": "Employees",
        "current_price": "Current Price",
        "previous_close": "Previous Close",
        "day_high": "Day High",
        "day_low": "Day Low",
        "week52_high": "52 Week High",
        "week52_low": "52 Week Low",
        "eps_fwd": "EPS (FWD)",
        "pe_fwd": "P/E (FWD)",
        "peg_ratio": "PEG Ratio",
        "div_rate": "Div Rate (FWD)",
        "div_yield": "Div Yield (FWD)",
        "recommendation": "Recommendation",
        
        # 盈利数据部分
        "earnings_title": "Earnings Performance",
        "earnings_date": "Earnings Date",
        "price_date": "Price Date",
        "close_change": "Close % Change",
        
        # 其他文本
        "fetching": "Fetching data...",
        "error_ticker": "Please provide a valid stock ticker.",
        "error_general": "An error occurred",
        "na": "N/A",
        "value": "Value",
        
        # 图表标签
        "historical_chart": "Historical Price Chart",
        
        # 按钮文本
        "zh_button": "中文",
        "en_button": "English",
    },
    
    "zh": {
        # 页面配置
        "page_title": "股票财务分析",
        
        # 侧边栏
        "sidebar_title": "财务分析",
        "ticker_label": "输入股票代码 (例如：AAPL)",
        "period_label": "选择时间周期",
        "period_options": ["1天", "5天", "1个月", "6个月", "年初至今", "1年", "5年"],
        "submit_button": "提交",
        
        # 表格标题
        "stock_info": "股票信息",
        "price_info": "价格信息",
        "business_metrics": "商业指标",
        
        # 表格列名
        "country": "国家",
        "sector": "行业板块",
        "industry": "细分行业",
        "market_cap": "市值",
        "enterprise_value": "企业价值",
        "employees": "员工人数",
        "current_price": "当前价格",
        "previous_close": "前收盘价",
        "day_high": "当日最高价",
        "day_low": "当日最低价",
        "week52_high": "52周最高价",
        "week52_low": "52周最低价",
        "eps_fwd": "每股收益（预测）",
        "pe_fwd": "市盈率（预测）",
        "peg_ratio": "市盈增长比率",
        "div_rate": "股息率（预测）",
        "div_yield": "股息收益率（预测）",
        "recommendation": "推荐评级",
        
        # 盈利数据部分
        "earnings_title": "盈利表现",
        "earnings_date": "财报公布日期",
        "price_date": "交易日期",
        "close_change": "收盘价涨跌幅",
        
        # 其他文本
        "fetching": "正在获取数据...",
        "error_ticker": "请输入有效的股票代码",
        "error_general": "发生错误",
        "na": "不适用",
        "value": "数值",
        
        # 图表标签
        "historical_chart": "历史价格图表",
        
        # 按钮文本
        "zh_button": "中文",
        "en_button": "English",
    }
}

# 周期映射
PERIOD_MAP = {
    "en": {
        "1D": ("1d", "1h"),
        "5D": ("5d", "1d"),
        "1M": ("1mo", "1d"),
        "6M": ("6mo", "1wk"),
        "YTD": ("ytd", "1mo"),
        "1Y": ("1y", "1mo"),
        "5Y": ("5y", "3mo"),
    },
    "zh": {
        "1天": ("1d", "1h"),
        "5天": ("5d", "1d"),
        "1个月": ("1mo", "1d"),
        "6个月": ("6mo", "1wk"),
        "年初至今": ("ytd", "1mo"),
        "1年": ("1y", "1mo"),
        "5年": ("5y", "3mo"),
    }
}
