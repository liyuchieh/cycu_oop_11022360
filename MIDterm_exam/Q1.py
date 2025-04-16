import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_pdf(mu, sigma, filename="normal_pdf.jpg"):
    """
    繪製常態分布的機率密度函數 (PDF) 並儲存為圖檔。

    :param mu: 平均數
    :param sigma: 標準差
    :param filename: 儲存的圖檔名稱
    """
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)  # 定義 x 軸範圍
    y = norm.pdf(x, mu, sigma)  # 計算 PDF 值

    # 繪製圖形
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, label=f'N(μ={mu}, σ={sigma})', color='blue')
    plt.title(f'Normal Distribution PDF\nμ={mu}, σ={sigma}')
    plt.xlabel('x')
    plt.ylabel('Density')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # 儲存圖檔
    plt.savefig(filename)
    plt.close()
    print(f"PDF 圖檔已儲存為 {filename}")

def main():
    """
    主函式，負責接收使用者輸入並繪製常態分布的 PDF。
    """
    try:
        mu = float(input("請輸入常態分布的平均數(mean): "))
        sigma = float(input("請輸入常態分布的標準差(standard deviation): "))
        if sigma <= 0:
            raise ValueError("標準差 (σ) 必須為正數。")
        filename = "normal_pdf.jpg"
        plot_normal_pdf(mu, sigma, filename)
    except ValueError as e:
        print(f"輸入錯誤: {e}")

if __name__ == "__main__":
    main()