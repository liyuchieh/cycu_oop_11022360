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

            # 提取站點資料
            rows = []
            for station in soup.find_all("span", class_="auto-list-stationlist"):
                # 提取 auto-list-stationlist-position-time
                position_time = station.find("span", class_="auto-list-stationlist-position auto-list-stationlist-position-time")
                position_time = position_time.text.strip() if position_time else "N/A"

                # 提取 auto-list-stationlist-position-now
                position_now = station.find("span", class_="auto-list-stationlist-position auto-list-stationlist-position-now")
                position_now = position_now.text.strip() if position_now else "N/A"

                # 如果 position_time 是 N/A，使用 position_now
                position = position_time if position_time != "N/A" else position_now

                # 提取其他資料
                number = station.find("span", class_="auto-list-stationlist-number")
                number = number.text.strip() if number else "N/A"

                place = station.find("span", class_="auto-list-stationlist-place")
                place = place.text.strip() if place else "N/A"

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
                writer.writerow(["Position", "Station Number", "Station Name", "UniStopId", "Latitude", "Longitude"])
                writer.writerows(rows)

            print(f"資料已成功解析並儲存到：{output_csv}")
        except Exception as e:
            print(f"解析失敗：{e}")


# 主程式
if __name__ == "__main__":
    # 去程
    go_route = BusRouteInfo(routeid="0100000A00", direction="go")
    go_route._fetch_content()  # 先渲染去程
    go_route.parse_to_csv("data/ebus_taipei_0100000A00_go.csv")  # 輸出去程資料

    # 返程
    back_route = BusRouteInfo(routeid="0100000A00", direction="come")
    back_route._fetch_content()  # 再渲染返程
    back_route.parse_to_csv("data/ebus_taipei_0100000A00_come.csv")  # 輸出返程資料