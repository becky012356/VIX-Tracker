import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="金融觀測站", layout="wide")
st.title("📊 市場數據視覺化")

# 側邊欄設定
with st.sidebar:
    st.header("參數設定")
    ticker = st.selectbox("選擇標的", ["^VIX", "GC=F"], 
                        format_func=lambda x: "恐慌指數 (VIX)" if x=="^VIX" else "黃金期貨")
    
    # 預設開始日期為 2024-01-01，結束日期為今天
    start = st.date_input("開始日期", value=pd.to_datetime("2024-01-01"))
    end = st.date_input("結束日期", value=pd.to_datetime("today"))

if st.button("更新圖表"):
    with st.spinner('資料讀取中...'):
        df = yf.download(ticker, start=start, end=end)
        
        if not df.empty:
            prices = df['Close'].values.flatten()
            dates = df.index  # 直接使用 Pandas 的 datetime 索引，Matplotlib 處理得更好
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 動態設定顏色：黃金用金色系，VIX用紅色系
            line_color = 'darkgoldenrod' if ticker == "GC=F" else 'crimson'
            fill_color = 'gold' if ticker == "GC=F" else 'lightcoral'
            
            # 1. 繪製折線圖
            ax.plot(dates, prices, color=line_color, linewidth=2)
            
            # 2. 加上底部填色 (讓圖表看起來更專業)
            ax.fill_between(dates, prices, color=fill_color, alpha=0.3)
            
            # 圖表美化
            ax.set_title(f"{'Gold Futures' if ticker == 'GC=F' else 'VIX Index'} Trend", fontsize=16, fontweight='bold')
            ax.set_ylabel("Price / Value", fontsize=12)
            ax.grid(axis='y', linestyle='--', alpha=0.7) # 加入水平參考線
            
            # 3. 自動格式化 X 軸日期，避免文字重疊
            fig.autofmt_xdate()
            
            # 在網頁顯示圖表
            st.pyplot(fig)
            
            # 顯示數據表格
            st.write("### 數據明細 (最後五筆)")
            st.dataframe(df.tail()) 
        else:
            st.error("❌ 此區間抓不到資料，請檢查日期設定（注意週末與國定假日休市）！")
