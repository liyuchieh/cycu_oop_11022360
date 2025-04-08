import math
import matplotlib.pyplot as plt

def lognormal_cdf(x, mean, std_dev):
    """
    計算對數常態分布的累積分布函數 (CDF)。

    :param x: float，輸入值
    :param mean: float，對數常態分布的均值
    :param std_dev: float，對數常態分布的標準差
    :return: float，累積分布函數值
    """
    if x <= 0:
        return 0.0
    z = (math.log(x) - mean) / std_dev
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

def plot_lognormal_cdf(data, output_file):
    """
    繪製對數常態累積分布函數圖並儲存為 JPG 檔案。

    :param data: tuple，包含對數常態分布的參數 (mean, std_dev)
    :param output_file: str，輸出的 JPG 檔案名稱
    """
    mean, std_dev = data
    x_values = [i * 0.01 for i in range(1, 501)]  # 定義 x 軸範圍 (0.01 到 5)
    cdf_values = [lognormal_cdf(x, mean, std_dev) for x in x_values]

    # 繪製圖形
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, cdf_values, label=f'Log-normal CDF (mean={mean}, std_dev={std_dev})', color='blue')
    plt.title('Log-normal Cumulative Distribution Function')
    plt.xlabel('x')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid()

    # 儲存為 JPG 檔案
    plt.savefig(output_file, format='jpg')
    plt.close()
    print(f"圖形已儲存為 {output_file}")

# 從使用者輸入獲取數據
try:
    mean = float(input("請輸入對數常態分布的均值 (mean): "))
    std_dev = float(input("請輸入對數常態分布的標準差 (std_dev): "))
    output_file = input("請輸入輸出的 JPG 檔案名稱 (例如: lognormal_cdf.jpg): ")

    # 繪製圖形
    plot_lognormal_cdf((mean, std_dev), output_file)
except ValueError:
    print("輸入的數值無效，請輸入有效的數字。")