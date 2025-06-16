import os
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class BusRouteInfo:
    def __init__(self, routeid: str, direction: str = 'go'):
        """
        初始化 BusRouteInfo 類別，設定路線 ID 和方向。

        :param routeid: str，公車路線 ID
        :param direction: str，方向 ('go' 或 'come')
        """
        self.rid = routeid
        self.content = None
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={routeid}'

        if direction not in ['go', 'come']:
            raise ValueError("Direction must be 'go' or 'come'")

        self.direction = direction

    def _fetch_content(self):
        """
        使用 Playwright 獲取網頁內容，根據方向切換到去程或返程。
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)

            # 如果是返程，點擊切換按鈕
            if self.direction == 'come':
                page.click('a.stationlist-come-go-gray.stationlist-come')

            page.wait_for_timeout(3000)  # 等待 3 秒以確保動態內容加載完成
            self.content = page.content()
            browser.close()

        # 將渲染後的 HTML 儲存到檔案
        os.makedirs("data", exist_ok=True)
        with open(f"data/ebus_taipei_{self.rid}_{self.direction}.html", "w", encoding="utf-8") as file:
            file.write(self.content)

    def parse_to_csv(self, output_csv: str):
        """
        解析 HTML，提取站點資料並輸出為 CSV 格式。

        :param output_csv: str，輸出的 CSV 檔案路徑
        """
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(self.content, "html.parser")

            # 根據方向選擇對應的區塊
            if self.direction == 'go':
                direction_block = soup.find("div", id="GoDirectionRoute")
            else:
                direction_block = soup.find("div", id="BackDirectionRoute")

            if not direction_block:
                raise ValueError(f"無法找到方向為 {self.direction} 的站點資料。")

            # 提取站點資料
            rows = []
            for station in direction_block.find_all("span", class_="auto-list-stationlist"):
                # 公車到達時間
                position = station.find("span", class_="auto-list-stationlist-position")
                position = position.text.strip() if position else "N/A"

                # 車站序號
                number = station.find("span", class_="auto-list-stationlist-number")
                number = number.text.strip() if number else "N/A"

                # 車站名稱
                place = station.find("span", class_="auto-list-stationlist-place")
                place = place.text.strip() if place else "N/A"

                # 車站編號
                uni_stop_id = station.find("input", {"name": "item.UniStopId"})
                uni_stop_id = uni_stop_id["value"] if uni_stop_id else "N/A"

                latitude = station.find("input", {"name": "item.Latitude"})
                latitude = latitude["value"] if latitude else "N/A"

                longitude = station.find("input", {"name": "item.Longitude"})
                longitude = longitude["value"] if longitude else "N/A"

                rows.append([position, number, place, uni_stop_id, latitude, longitude])

            # 輸出為 CSV 檔案
            with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["公車到達時間", "車站序號", "車站名稱", "車站編號", "latitude", "longitude"])
                writer.writerows(rows)

            print(f"資料已成功解析並儲存到：{output_csv}")
        except Exception as e:
            print(f"解析失敗：{e}")


# 主程式
if __name__ == "__main__":
    try:
        # 使用者輸入 routeid 和方向
        routeid = input("請輸入公車路線 ID (例如：0100000A00): ")
        direction = input("請輸入方向 ('go' 表示去程, 'come' 表示回程): ").strip().lower()

        if direction not in ['go', 'come']:
            raise ValueError("方向必須是 'go' 或 'come'")

        # 建立 BusRouteInfo 物件並執行
        route = BusRouteInfo(routeid=routeid, direction=direction)
        route._fetch_content()  # 獲取網頁內容
        output_csv = f"data/ebus_taipei_{routeid}_{direction}.csv"
        route.parse_to_csv(output_csv)  # 解析並輸出為 CSV
    except Exception as e:
        print(f"發生錯誤：{e}")