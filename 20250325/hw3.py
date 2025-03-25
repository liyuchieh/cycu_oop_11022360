from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def fetch_bus_arrival_time():
    # 自動下載並配置 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # 開啟目標網址
        url = 'https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'
        driver.get(url)

        # 等待頁面加載完成，確保動態內容已載入
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ttegotitle'))
        )

        # 獲取頁面 HTML
        time.sleep(2)  # 等待額外的 JavaScript 加載
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 找到去程的站名表格
        outbound_table = soup.find('td', class_='ttegotitle').find_next('table')
        if not outbound_table:
            print("無法找到去程的站名表格，請檢查網頁結構。")
            return

        # 讀取去程站名與到站時間
        station_dict = {}
        rows = outbound_table.find_all('tr')
        for row in rows:
            stop_link = row.find('a')  # 找到站名的 <a> 標籤
            eta_cell = row.find('td', id=lambda x: x and x.startswith('tte'))  # 找到到站時間的 <td>

            if stop_link:
                station_name = stop_link.text.strip()  # 取得站名
                if eta_cell:
                    eta = eta_cell.text.strip()  # 取得到站時間
                    if not eta:  # 如果到站時間為空，記錄為「無資料」
                        eta = "無資料"
                else:
                    eta = "無資料"  # 如果無法找到到站時間，設為「無資料」

                # 儲存站名與到站時間
                station_dict[station_name] = eta

        # 列出所有站名與到站時間
        if station_dict:
            print("去程所有站名與到站時間如下：")
            for station_name, eta in station_dict.items():
                print(f"{station_name}: {eta}")
        else:
            print("無法解析任何去程車站資訊，請檢查網頁結構。")
            return

        # 使用者輸入站名
        station_name = input("\n請輸入站名：").strip()

        # 查詢站名並輸出到站時間
        if station_name in station_dict:
            print(f"{station_name} 公車到站時間：{station_dict[station_name]}")
        else:
            print("不好意思！沒有這個車站。")

    finally:
        # 關閉瀏覽器
        driver.quit()

if __name__ == '__main__':
    fetch_bus_arrival_time()