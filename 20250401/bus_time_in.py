import os
import re
from playwright.sync_api import sync_playwright

def sanitize_filename(name):
    """ 過濾非法字元，確保檔名可用 """
    return re.sub(r'[\/:*?"<>|]', '_', name)

def download_and_extract_eta_with_playwright(stop_link: str, folder_path: str, station_name: str, target_line="忠孝幹線"):
    """ 使用 Playwright 下載站牌的 HTML 頁面並提取指定路線的預估到站時間 """
    stop_id = stop_link.split("=")[1]
    url = f'https://pda5284.gov.taipei/MQS/{stop_link}'
    file_path = os.path.join(folder_path, f"bus_stop_{stop_id}.html")

    os.makedirs(folder_path, exist_ok=True)  # 確保資料夾存在

    try:
        with sync_playwright() as p:
            # 啟動瀏覽器
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 打開目標網址
            page.goto(url)

            # 等待網頁加載完成
            page.wait_for_timeout(10000)  # 額外等待 10 秒
            print("🔍 正在檢查網頁內容...")
            print(page.content())  # 輸出網頁的 HTML 結構以調試

            # 確保表格行元素存在
            page.wait_for_selector("table tbody tr")  # 更精確的選取器

            # 儲存 HTML 到本地檔案
            content = page.content()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
                print(f"網頁已成功下載並儲存為 {file_path}")

            # 提取所有行資料
            rows = page.query_selector_all("table tbody tr")
            for row in rows:
                # 找到包含目標路線名稱的行
                route_name = row.query_selector("td")
                if route_name and target_line in route_name.inner_text():
                    # 提取 `data-deptimen1` 屬性值
                    eta_cell = row.query_selector("td[data-deptimen1]")
                    if eta_cell:
                        eta_text = eta_cell.get_attribute("data-deptimen1")
                        print(f"{station_name} - {target_line} 預估到站時間: {eta_text}")
                        browser.close()
                        return eta_text

            print(f"⚠️ 在 {station_name} 的 HTML 中找不到 {target_line} 的預估時間")
            browser.close()
            return None

    except Exception as e:
        print(f"❌ 使用 Playwright 解析 {station_name} 的 HTML 時發生錯誤: {e}")
        return None

if __name__ == '__main__':
    folder_path = "./bus_stations_html"
    stop_link = "route.jsp?rid=10417"  # 替換成實際的站牌連結
    station_name = "忠孝幹線"  # 替換成你要查的站名

    # 使用 Playwright 下載站牌頁面並提取預估到站時間
    download_and_extract_eta_with_playwright(stop_link, folder_path, station_name)