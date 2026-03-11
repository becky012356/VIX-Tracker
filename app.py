import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd  # 引入 pandas

st.set_page_config(page_title="金融觀測站", layout="wide")
st.title("📊 市場數據視覺化")

# 側邊欄設定
with st.sidebar:
    st.header("參數設定")
    ticker = st.selectbox("選擇標的", ["^VIX", "GC=F"], 
                        format_func=lambda x: "恐慌指數 (VIX)" if x=="^VIX" else "黃金期貨")
    
    # 這裡修正了 yf.pd 的錯誤，改用 pd.to_datetime
    start = st.date_input("開始日期", value=pd.to_datetime("2024-01-01"))
    end = st.date_input("結束日期")

if st.button("更新圖表"):
    with st.spinner('資料讀取中...'):
        # 修正 yfinance 可能回傳 MultiIndex 的問題
        df = yf.download(ticker, start=start, end=end)
        
        if not df.empty:
            # 取得收盤價並轉為一維陣列
            prices = df['Close'].values.flatten()
            dates = df.index.strftime('%m-%d')
            
            # 繪圖
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(dates, prices, color='skyblue', edgecolor='black')
            ax.set_title(f"{ticker} Trend ({start} to {end})")
            plt.xticks(rotation=45)
            
            # 在網頁顯示圖表
            st.pyplot(fig)
            
            # 顯示數據表格
            st.write("### 數據明細 (最後五筆)")
            st.dataframe(df.tail()) 
        else:
            st.error("❌ 此區間抓不到資料，請檢查日期設定（注意週末休市）！")
