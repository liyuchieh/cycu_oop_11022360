import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import geopandas as gpd 
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib
matplotlib.rc('font', family='Microsoft JhengHei')  # 設定字型為微軟正黑體


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


def truncate_to_three_decimals(value):
    """
    無條件捨去到小數點後第三位
    :param value: 浮點數值
    :return: 無條件捨去後的浮點數值
    """
    return np.floor(value * 1000) / 1000

def read_and_truncate_coordinates(file_path):
    """
    讀取 CSV 檔案中的 latitude 和 longitude，並將其無條件捨去到小數點後第三位。
    
    :param file_path: CSV 檔案的路徑
    :return: 包含無條件捨去後的所有欄位的 DataFrame
    """
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(file_path)
        
        # 檢查是否包含 latitude 和 longitude 欄位
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            raise ValueError("CSV 檔案中缺少 latitude 或 longitude 欄位")
        
        # 無條件捨去到小數點後第三位
        df['latitude'] = df['latitude'].apply(truncate_to_three_decimals)
        df['longitude'] = df['longitude'].apply(truncate_to_three_decimals)
        
        return df  # 返回完整的 DataFrame，而不僅僅是 latitude 和 longitude
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None

def plot_bus_route_with_marker(csv_data, geojson_path, output_image="Bus_Route_Map.jpg", marker_image_path=None):
    """
    根據 CSV 資料繪製公車路線圖，並在「進站中」的點右邊標記公車圖片，其餘點左邊標記文字。
    
    :param csv_data: 包含 latitude 和 longitude 的 DataFrame
    :param geojson_path: GeoJSON 檔案路徑
    :param output_image: 輸出的地圖圖片檔案名稱
    :param marker_image_path: 標記圖片的路徑
    """
    try:
        # 讀取 GeoJSON 檔案
        gdf = gpd.read_file(geojson_path)
        
        # 無條件捨去 GeoJSON 中的座標到小數點後第三位
        gdf['latitude'] = gdf.geometry.y.apply(truncate_to_three_decimals)
        gdf['longitude'] = gdf.geometry.x.apply(truncate_to_three_decimals)
        
        # 合併 CSV 資料與 GeoJSON 資料
        merged_data = pd.merge(csv_data, gdf, on=['latitude', 'longitude'], how='inner')
        
        # 繪製路線圖
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='lightgrey', label='All Bus Stops')  # 所有公車站點
        ax.plot(merged_data['longitude'], merged_data['latitude'], color='blue', linewidth=2, label='Bus Route')  # 公車路線
        ax.scatter(merged_data['longitude'], merged_data['latitude'], color='red', label='Bus Stops', zorder=5)  # 公車站點
        
        # 遍歷所有站點
        for _, row in csv_data.iterrows():
            station_lat = float(row['latitude'])
            station_lon = float(row['longitude'])
            station_name = row['車站名稱']
            arrival_time = row['公車到達時間']
            
            if arrival_time == '進站中' and marker_image_path is not None:
                # 在右邊標記公車圖片
                img = plt.imread(marker_image_path)
                imagebox = OffsetImage(img, zoom=0.03)  # 調整圖片大小
                ab = AnnotationBbox(imagebox, (station_lon + 0.007, station_lat), frameon=False, zorder=10)
                ax.add_artist(ab)
            else:
                # 在左邊標記文字
                ax.text(station_lon - 0.003, station_lat, arrival_time, fontsize=4, ha='right', color='black')
        
        plt.title("Bus Route Map")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend()
        
        # 儲存地圖為圖片
        plt.savefig(output_image, dpi=300)
        plt.close()
        print(f"路線圖已儲存為 {output_image}")
    except Exception as e:
        print(f"發生錯誤：{e}")

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

        # 讀取並處理 CSV 檔案
        csv_data = read_and_truncate_coordinates(output_csv)
        if csv_data is not None:
            # 指定 GeoJSON 檔案路徑
            geojson_path = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250422\\bus_stops.geojson"
            
            # 指定標記圖片的路徑
            marker_image_path = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250429\\練習二\\bus.png"
            
            # 繪製公車路線圖並添加標記
            output_image = f"data/ebus_taipei_{routeid}_{direction}_map.jpg"
            plot_bus_route_with_marker(csv_data, geojson_path, output_image, marker_image_path)
    except Exception as e:
        print(f"發生錯誤：{e}")