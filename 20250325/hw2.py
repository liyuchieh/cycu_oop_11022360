import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 讀取 CSV 檔案
file_path = "hw2.csv"  # 請替換成你的檔案名稱
df = pd.read_csv(file_path)

# 讀取日期並轉換格式 (確保最舊的日期在最左邊)
date_column = df.columns[0]  # 假設日期在第一欄
df[date_column] = pd.to_datetime(df[date_column].astype(str), format='%Y%m%d')
df["Formatted_Date"] = df[date_column].dt.strftime('%m/%d')

# 取得數據並倒序排列（讓最舊的時間在最左邊）
dates = df["Formatted_Date"][::-1].values  # 倒序排列日期
buy_values = df.iloc[:, 3][::-1].values   # 倒序排列買入數據
sell_values = df.iloc[:, 5][::-1].values  # 倒序排列賣出數據

# 畫圖
plt.figure(figsize=(10, 5))
plt.plot(dates, buy_values, label='Buy', linestyle='-', color='blue')
plt.plot(dates, sell_values, label='Sell', linestyle='-', color='red')

# 新增 y 軸網格線
plt.grid(axis='y', linestyle='--', alpha=0.7)  

# 設定 X 軸刻度（每 7 天取一個）
tick_indices = np.arange(0, len(dates), 7)  # 每 7 天取一個索引
plt.xticks(tick_indices, dates[tick_indices], rotation=45)  # 避免 IndexError

# 設定標題與標籤
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.title('cash exchange rate')
plt.legend()

# 顯示圖表
plt.show()
