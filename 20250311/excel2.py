import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 檔案
df = pd.read_excel('20250311.xlsx')

# 假設欄位名稱為 'A' 和 'B'
x = df['A']
y = df['B']

# 繪製散佈圖
plt.scatter(x, y)
plt.xlabel('A')
plt.ylabel('B')
plt.title('Scatter Plot of A vs B')
plt.show()