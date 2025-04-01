from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def fetch_bus_stations():
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

        # 讀取去程站名及超連結
        outbound_stations = []
        rows = outbound_table.find_all('tr')
        for row in rows:
            stop_link = row.find('a')  # 找到站名的 <a> 標籤
            if stop_link:
                station_name = stop_link.text.strip()  # 取得站名
                station_url = stop_link['href']  # 取得超連結
                outbound_stations.append((station_name, station_url))

        # 找到返程的站名表格
        inbound_table = outbound_table.find_next('table')
        if not inbound_table:
            print("無法找到返程的站名表格，請檢查網頁結構。")
            return

        # 讀取返程站名及超連結
        inbound_stations = []
        rows = inbound_table.find_all('tr')
        for row in rows:
            stop_link = row.find('a')  # 找到站名的 <a> 標籤
            if stop_link:
                station_name = stop_link.text.strip()  # 取得站名
                station_url = stop_link['href']  # 取得超連結
                inbound_stations.append((station_name, station_url))

        # 列出所有站名及超連結
        if outbound_stations:
            print("去程所有站名及超連結如下：")
            for station_name, station_url in outbound_stations:
                print(f"{station_name}: {station_url}")
        else:
            print("無法解析任何去程車站資訊，請檢查網頁結構。")

        if inbound_stations:
            print("\n返程所有站名及超連結如下：")
            for station_name, station_url in inbound_stations:
                print(f"{station_name}: {station_url}")
        else:
            print("無法解析任何返程車站資訊，請檢查網頁結構。")

    finally:
        # 關閉瀏覽器
        driver.quit()

if __name__ == '__main__':
    fetch_bus_stations()