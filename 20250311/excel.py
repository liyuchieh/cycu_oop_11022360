import pandas as pd

# 讀取 Excel 檔案
df = pd.read_excel('20250311.xlsx')

# 假設欄位名稱為 'A' 和 'B'
df['Sum'] = df['A'] + df['B']

# 印出相加結果
print(df['Sum'])