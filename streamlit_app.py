import datetime
import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# ========== 导入翻译配置 ==========
try:
    from translations import TRANSLATIONS, PERIOD_MAP
    TRANSLATIONS_AVAILABLE = True
except ImportError:
    TRANSLATIONS_AVAILABLE = False
    # 创建默认英文翻译
    TRANSLATIONS = {"en": {}}
    PERIOD_MAP = {"en": {}}

# ========== 语言设置 ==========
if 'language' not in st.session_state:
    st.session_state.language = 'zh'  # 默认中文

# 翻译辅助函数
def t(key):
    """获取当前语言的翻译文本"""
    lang = st.session_state.language
    if TRANSLATIONS_AVAILABLE and lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    # 回退到英文
    if 'en' in TRANSLATIONS and key in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][key]
    return key

# ========== 原有函数（稍作修改支持双语） ==========
def format_value(value):
    """格式化市值和企业价值，支持双语后缀"""
    if st.session_state.language == 'zh':
        suffixes = ["", "千", "百万", "十亿", "万亿"]
    else:
        suffixes = ["", "K", "M", "B", "T"]
    
    suffix_index = 0
    while value >= 1000 and suffix_index < len(suffixes) - 1:
        value /= 1000
        suffix_index += 1
    return f"${value:.1f}{suffixes[suffix_index]}"

def safe_format(value, fmt="{:.2f}", fallback=None):
    """安全格式化函数，支持双语N/A"""
    if fallback is None:
        fallback = t('na')
    try:
        return fmt.format(value) if value is not None else fallback
    except (ValueError, TypeError):
        return fallback

def get_next_trading_day(df, date):
    after = df[df.index > date]
    return after.index[0] if not after.empty else None

def get_same_or_next_trading_day(df, date):
    if date in df.index:
        return date
    return get_next_trading_day(df, date)

# ========== Streamlit 应用界面 ==========
st.set_page_config(page_title=t('page_title'), layout="wide")

with st.sidebar:
    # ========== 语言切换按钮 ==========
    st.markdown("### 🌐 语言 / Language")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"🇨🇳 {t('zh_button')}", use_container_width=True, 
                    type="primary" if st.session_state.language == 'zh' else "secondary"):
            st.session_state.language = 'zh'
            st.rerun()
    
    with col2:
        if st.button(f"🇬🇧 {t('en_button')}", use_container_width=True,
                    type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    
    st.markdown("---")
    
    # ========== 股票查询表单 ==========
    st.title(t('sidebar_title'))
    ticker = st.text_input(t('ticker_label'), "AAPL")
    period = st.selectbox(t('period_label'), t('period_options'), index=2)
    submit = st.button(t('submit_button'), type="primary")

# ========== 数据处理和显示 ==========
if submit:
    if not ticker.strip():
        st.error(t('error_ticker'))
    else:
        try:
            with st.spinner(t('fetching'), show_time=True):
                # 获取股票数据
                stock = yf.Ticker(ticker.upper())
                info = stock.info

                st.subheader(f"{ticker} - {info.get('longName', t('na'))}")

                # 获取周期映射
                current_lang = st.session_state.language
                period_mapping = PERIOD_MAP.get(current_lang, PERIOD_MAP.get('en', {}))
                selected_period, interval = period_mapping.get(period, ("1mo", "1d"))
                
                # 获取历史数据
                history = stock.history(period=selected_period, interval=interval)
                chart_data = pd.DataFrame(history["Close"])
                
                # 显示历史价格图表
                st.markdown(f"**{t('historical_chart')}**")
                st.line_chart(chart_data)

                # 显示三个信息表格
                col1, col2, col3 = st.columns(3)

                # 1. 股票信息表格
                stock_info = [
                    (t('stock_info'), t('value')),
                    (t('country'), info.get('country', t('na'))),
                    (t('sector'), info.get('sector', t('na'))),
                    (t('industry'), info.get('industry', t('na'))),
                    (t('market_cap'), format_value(info.get('marketCap', 0))),
                    (t('enterprise_value'), format_value(info.get('enterpriseValue', 0))),
                    (t('employees'), info.get('fullTimeEmployees', t('na')))
                ]
                
                df_stock = pd.DataFrame(stock_info[1:], columns=stock_info[0](@ref)
                col1.dataframe(df_stock, width=400, hide_index=True)

                # 2. 价格信息表格
                price_info = [
                    (t('price_info'), t('value')),
                    (t('current_price'), safe_format(info.get('currentPrice'), fmt="${:.2f}")),
                    (t('previous_close'), safe_format(info.get('previousClose'), fmt="${:.2f}")),
                    (t('day_high'), safe_format(info.get('dayHigh'), fmt="${:.2f}")),
                    (t('day_low'), safe_format(info.get('dayLow'), fmt="${:.2f}")),
                    (t('week52_high'), safe_format(info.get('fiftyTwoWeekHigh'), fmt="${:.2f}")),
                    (t('week52_low'), safe_format(info.get('fiftyTwoWeekLow'), fmt="${:.2f}"))
                ]
                
                df_price = pd.DataFrame(price_info[1:], columns=price_info[0](@ref)
                col2.dataframe(df_price, width=400, hide_index=True)

                # 3. 商业指标表格
                biz_metrics = [
                    (t('business_metrics'), t('value')),
                    (t('eps_fwd'), safe_format(info.get('forwardEps'))),
                    (t('pe_fwd'), safe_format(info.get('forwardPE'))),
                    (t('peg_ratio'), safe_format(info.get('pegRatio'))),
                    (t('div_rate'), safe_format(info.get('dividendRate'), fmt="${:.2f}")),
                    (t('div_yield'), safe_format(info.get('dividendYield'), fmt="{:.2f}%") if info.get('dividendYield') else t('na')),
                    (t('recommendation'), info.get('recommendationKey', t('na')).capitalize())
                ]
                
                df_metrics = pd.DataFrame(biz_metrics[1:], columns=biz_metrics[0](@ref)
                col3.dataframe(df_metrics, width=400, hide_index=True)

                # ========== 盈利数据部分 ==========
                st.subheader(t('earnings_title'))
                
                earnings = stock.get_earnings_dates(limit=12)
                history_3y = stock.history(period="3y")
                
                results = []
                for idx, row in earnings.iterrows():
                    earnings_date = pd.to_datetime(idx).date()
                    raw_time = row.get("Time", "")
                    time_of_day = raw_time.lower() if isinstance(raw_time, str) else "pm"

                    try:
                        if time_of_day == "am":
                            trading_day = get_same_or_next_trading_day(history_3y, idx)
                            prev_day = history_3y.index[history_3y.index < trading_day][-1]
                        else:
                            trading_day = get_next_trading_day(history_3y, idx)
                            prev_day = history_3y.index[history_3y.index < idx][-1]

                        prev_close = history_3y.loc[prev_day]["Close"]
                        next_close = history_3y.loc[trading_day]["Close"]
                        pct_change = ((next_close - prev_close) / prev_close) * 100

                        results.append({
                            t('earnings_date'): earnings_date,
                            t('price_date'): trading_day.date(),
                            t('close_change'): f"{pct_change:.2f}%"
                        })

                    except Exception:
                        results.append({
                            t('earnings_date'): earnings_date,
                            t('price_date'): None,
                            t('close_change'): None
                        })

                df_earnings = pd.DataFrame(results)
                df_earnings = df_earnings.dropna()

                # 显示盈利数据表格和图表
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    df_display = df_earnings.copy()
                    df_display[t('close_change')] = df_display[t('close_change')].apply(
                        lambda x: f"{float(str(x).replace('%', '')):.2f}%" if pd.notnull(x) else t('na')
                    )
                    st.dataframe(df_display, width=400, height=450, hide_index=True)

                with col2:
                    chart_data = df_earnings.copy()
                    chart_data[t('earnings_date')] = chart_data[t('earnings_date')].astype(str)
                    chart_data = chart_data[chart_data[t('close_change')] != t('na')].copy()
                    chart_data[t('close_change')] = (
                        chart_data[t('close_change')].str.replace("%","").astype(float)
                    )

                    chart = alt.Chart(chart_data).mark_bar().encode(
                        x=alt.X(f"{t('earnings_date')}:N", sort="ascending"),
                        y=alt.Y(f"{t('close_change')}:Q"),
                        color=alt.condition(
                            alt.datum[t('close_change')] > 0,
                            alt.value("green"),
                            alt.value("red")
                        ),
                        tooltip=[
                            t('earnings_date'), 
                            t('price_date'), 
                            alt.Tooltip(t('close_change'), format=".2f")
                        ]
                    ).properties(width="container", height=450)

                    st.altair_chart(chart, use_container_width=True)

        except Exception as e:
            st.exception(f"{t('error_general')}: {e}")

# ========== 初始状态显示 ==========
else:
    st.info("👈 请在侧边栏输入股票代码并点击提交按钮开始分析。")
    if st.session_state.language == 'zh':
        st.info("💡 您可以通过侧边栏的按钮切换中英文界面。")
