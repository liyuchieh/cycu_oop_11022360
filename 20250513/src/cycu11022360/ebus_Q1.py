import os
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_bus_info_go(bus_id):
    """
    Retrieve bus stop information based on the bus ID.
    """
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={bus_id}"
    content = None

    # 使用 Playwright 獲取網頁內容
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)  # 等待 3 秒以確保動態內容加載完成
        content = page.content()
        browser.close()

    # 將渲染後的 HTML 儲存到檔案
    os.makedirs("data", exist_ok=True)
    with open(f"data/ebus_{bus_id}.html", "w", encoding="utf-8") as file:
        file.write(content)

    # 使用 BeautifulSoup 解析 HTML
    try:
        soup = BeautifulSoup(content, "html.parser")
        direction_block = soup.find("div", id="GoDirectionRoute")

        if not direction_block:
            raise ValueError("無法找到站點資料。")

        # 提取站點資料
        rows = []
        for station in direction_block.find_all("span", class_="auto-list-stationlist"):
            uni_stop_id = station.find("input", {"name": "item.UniStopId"})
            uni_stop_id = uni_stop_id["value"] if uni_stop_id else "N/A"

            rows.append(uni_stop_id)

        return rows
    
    except Exception as e:
        print(f"解析失敗：{e}")
        return None


if __name__ == "__main__":
    bus = get_bus_info_go("0161000900")
    print(f"Bus ID: {bus}")
