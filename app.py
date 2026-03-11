import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# 網頁標題
st.title("📈 金融數據觀測站")

# 側邊欄：讓使用者輸入
with st.sidebar:
    st.header("設定參數")
    target = st.selectbox("選擇標的", ["黃金期貨 (GC=F)", "恐慌指數 (^VIX)"])
    start_date = st.date_input("開始日期")
    end_date = st.date_input("結束日期")

if st.button("開始繪圖"):
    ticker = "GC=F" if "黃金" in target else "^VIX"
    data = yf.download(ticker, start=start_date, end=end_date)
    
    if not data.empty:
        # 繪圖
        fig, ax = plt.subplots(figsize=(10, 5))
        color = 'gold' if ticker == "GC=F" else 'red'
        ax.bar(data.index.strftime('%m-%d'), data['Close'].values.flatten(), color=color)
        plt.xticks(rotation=45)
        
        # 在 Streamlit 顯示圖表
        st.pyplot(fig)
        st.write("### 數據明細", data.tail())
    else:
        st.error("此區間無資料，請重新選擇！")
