import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# 設定 Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # 不開啟瀏覽器視窗
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 啟動 WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

BASE_URL = "https://pda5284.gov.taipei"

def fetch_station_urls(route_url):
    """使用 Selenium 抓取站名與對應的超連結"""
    try:
        driver.get(route_url)
        time.sleep(3)  # 等待 JavaScript 加載

        station_urls = {}

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            station_name = link.text.strip()
            station_url = link.get_attribute("href")

            if not station_name or not station_url or "javascript" in station_url:
                continue

            if not station_url.startswith("http"):
                station_url = BASE_URL + station_url

            station_urls[station_name] = station_url

        if not station_urls:
            print("⚠️ 無法找到任何站名，請檢查網頁結構")
        
        return station_urls

    except Exception as e:
        print(f"❌ 取得站名時發生錯誤: {e}")
        return {}

def sanitize_filename(name):
    """ 過濾非法字元，確保檔名可用 """
    return re.sub(r'[\/:*?"<>|]', '_', name)

def download_station_html(station_name, station_url, folder_path):
    """ 使用 Selenium 下載並儲存站點 HTML 內容 """
    try:
        print(f"⬇️ 正在下載 {station_name} 的 HTML，URL: {station_url}")

        driver.get(station_url)
        time.sleep(3)  # 等待頁面加載

        # 獲取完整 HTML 內容
        content = driver.page_source

        os.makedirs(folder_path, exist_ok=True)
        safe_station_name = sanitize_filename(station_name)
        file_path = os.path.join(folder_path, f"{safe_station_name}.html")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"✅ {station_name} 的 HTML 已成功下載至 {file_path}")

    except Exception as e:
        print(f"❌ 下載 {station_name} 的 HTML 時發生錯誤: {e}")

if __name__ == '__main__':
    route_url = 'https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'
    folder_path = "./bus_stations_html"

    station_urls = fetch_station_urls(route_url)
    
    if not station_urls:
        print("❌ 無法取得站名與對應的 URL，請檢查網頁結構。")
    else:
        for station_name, station_url in station_urls.items():
            download_station_html(station_name, station_url, folder_path)

        print("\n🎉 所有站名的 HTML 檔案已下載完成！")

    driver.quit()  # 關閉瀏覽器
