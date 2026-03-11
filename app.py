import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="金融觀測站", layout="wide")
st.title("📊 市場數據視覺化")

# 側邊欄設定
with st.sidebar:
    ticker = st.selectbox("選擇標的", ["^VIX", "GC=F"], format_func=lambda x: "恐慌指數 (VIX)" if x=="^VIX" else "黃金期貨")
    start = st.date_input("開始日期", value=yf.pd.to_datetime("2024-01-01"))
    end = st.date_input("結束日期")

if st.button("更新圖表"):
    with st.spinner('資料讀取中...'):
        df = yf.download(ticker, start=start, end=end)
        
        if len(df) > 0:
            # 確保資料格式正確
            prices = df['Close'].values.flatten()
            dates = df.index.strftime('%m-%d')
            
            # 繪圖
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(dates, prices, color='skyblue', edgecolor='black')
            ax.set_title(f"{ticker} Trend")
            plt.xticks(rotation=45)
            
            # 顯示
            st.pyplot(fig)
            st.dataframe(df.tail()) # 順便顯示最後幾筆數字
        else:
            st.error("此區間抓不到資料，請檢查日期設定！")
