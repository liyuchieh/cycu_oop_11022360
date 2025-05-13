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
            position = station.find("span", class_="auto-list-stationlist-position")
            position = position.text.strip() if position else "N/A"

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
        output_csv = f"data/ebus_{bus_id}.csv"
        with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["公車到達時間", "車站序號", "車站名稱", "車站編號", "latitude", "longitude"])
            writer.writerows(rows)

        print(f"資料已成功解析並儲存到：{output_csv}")
        return rows
    except Exception as e:
        print(f"解析失敗：{e}")
        return None


class BusInfo:
    def __init__(self, bus_id):
        self.bus_id = bus_id

    def get_route_info_go(self): # 還要再分去程和回程
        """
        Retrieve route information for the bus.
        """
        route_info = ['stop_id1', 'stop_id2', 'stop_id3']  # Example route info
        return route_info
        # return bus_stop(self.bus_id)

    def get_route_info_come(self): # 還要再分去程和回程
        """
        Retrieve route information for the bus.
        """
        route_info = ['stop_id1', 'stop_id2', 'stop_id3']  # Example route info
        return route_info
        # return bus_stop(self.bus_id)
    
    def get_stop_info(self):
        """
        Retrieve stop information for the bus.
        """
        return bus_stop(self.bus_id)

    def get_arrival_time_info(self):
        """
        Retrieve arrival time information for the bus.
        """
        # 此方法可以根據需求進一步實作
        print("到站時間資訊功能尚未實作。")
        return None


if __name__ == "__main__":
    bus = BusInfo("0161000900")
    print(f"Bus ID: {bus.bus_id}")
    print(f"Route Info Go: {bus.get_route_info_go()}")
    print(f"Route Info Come: {bus.get_route_info_come()}")

    
    # Example usage of the methods
    route_info = bus.get_route_info()
    print("Route Info:", route_info)

    stop_info = bus.get_stop_info()
    print("Stop Info:", stop_info)

    arrival_time_info = bus.get_arrival_time_info()
    print("Arrival Time Info:", arrival_time_info)

    # Example usage of the methods (to be implemented)
    # bus.get_route_info()
    # bus.get_stop_info()
    # bus.get_arrival_time_info()