import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def plot_vix_indices():
    # 1. 設定 VIX 指數代號
    ticker_symbol = "^VIX"
    
    print("--- 市場恐慌指數 (VIX) 查詢系統 ---")
    start_date = input("請輸入開始日期 (YYYY-MM-DD): ")
    end_date = input("請輸入結束日期 (YYYY-MM-DD): ")

    try:
        # 2. 下載資料
        data = yf.download(ticker_symbol, start=start_date, end=end_date)

        if data.empty:
            print("❌ 找不到資料，請檢查日期格式或該區間是否為休市日。")
            return

        # 整理資料（處理 yfinance 可能產生的 MultiIndex）
        prices = data['Close'].values.flatten()
        dates = data.index.strftime('%m-%d')

        # 3. 設定動態顏色 (根據 VIX 數值判斷恐慌程度)
        # 綠色: 平穩(<20) | 橙色: 警戒(20-30) | 紅色: 恐慌(>30)
        colors = []
        for v in prices:
            if v < 20: colors.append('#2ecc71')   # 綠色
            elif v < 30: colors.append('#f39c12') # 橙色
            else: colors.append('#e74c3c')        # 紅色

        # 4. 繪圖
        plt.figure(figsize=(12, 6))
        bars = plt.bar(dates, prices, color=colors, edgecolor='grey', alpha=0.8)

        # 5. 圖表修飾
        plt.title(f"VIX Fear Index ({start_date} to {end_date})", fontsize=16)
        plt.ylabel("VIX Value", fontsize=12)
        plt.xlabel("Date (Month-Day)", fontsize=12)
        plt.xticks(rotation=45)
        
        # 加入一條 20 的警戒線
        plt.axhline(y=20, color='orange', linestyle='--', label='Warning Level (20)')
        plt.axhline(y=30, color='red', linestyle='--', label='Panic Level (30)')
        plt.legend()
        
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.tight_layout()
        
        print("✅ 恐慌指數長條圖已生成！")
        plt.show()

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    plot_vix_indices()
