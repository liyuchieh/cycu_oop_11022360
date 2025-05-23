import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.rc('font', family='Microsoft JhengHei')

def truncate_to_three_decimals(value):
    """
    無條件捨去到小數點後第三位
    """
    return np.floor(value * 1000) / 1000

def read_and_truncate_coordinates(file_path):
    """
    讀取 CSV 檔案中的 latitude 和 longitude，並將其無條件捨去到小數點後第三位。
    """
    try:
        df = pd.read_csv(file_path)
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            raise ValueError("CSV 檔案中缺少 latitude 或 longitude 欄位")
        df['latitude'] = df['latitude'].apply(truncate_to_three_decimals)
        df['longitude'] = df['longitude'].apply(truncate_to_three_decimals)
        return df[['latitude', 'longitude']]
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None

def plot_bus_route(csv_data, geojson_path, shp_path, output_image="Bus_Route_Map.jpg"):
    """
    根據 CSV 資料、GeoJSON 檔案和背景 SHP 檔案繪製公車路線圖。
    """
    try:
        # 讀取 GeoJSON 檔案
        gdf_geojson = gpd.read_file(geojson_path)
        gdf_geojson['latitude'] = gdf_geojson.geometry.y.apply(truncate_to_three_decimals)
        gdf_geojson['longitude'] = gdf_geojson.geometry.x.apply(truncate_to_three_decimals)

        # 合併 CSV 資料與 GeoJSON 資料
        merged_data = pd.merge(csv_data, gdf_geojson, on=['latitude', 'longitude'], how='inner')

        # 讀取背景 SHP 檔案
        gdf_shp = gpd.read_file(shp_path)

        # 繪製地圖
        fig, ax = plt.subplots(figsize=(20, 20))
        gdf_shp.plot(ax=ax, color='white', edgecolor='black', label='Background Map')  # 背景地圖
        ax.plot(merged_data['longitude'], merged_data['latitude'], color='blue', linewidth=1, label='Bus Route')  # 公車路線
        ax.scatter(merged_data['longitude'], merged_data['latitude'], color='red', label='Bus Stops', zorder=1)  # 公車站點

        plt.title("承德幹線地圖(北北基桃)", fontsize=24)
        plt.xlabel("經度", fontsize=20)
        plt.ylabel("緯度", fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=20)  # 增大刻度字體大小
        plt.legend(loc='lower right', fontsize=20)

        # 儲存地圖為圖片
        plt.savefig(output_image, dpi=300)
        plt.close(fig)
        print(f"路線圖已儲存為 {output_image}")
    except Exception as e:
        print(f"發生錯誤：{e}")

# 範例使用
if __name__ == "__main__":
    # 檔案路徑
    file1 = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250422\\練習一_data\\承德幹線_go_bus_info.csv"
    geojson_path = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250422\\bus_stops.geojson"
    shp_path = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250520\\老師資料\\篩選後\\filtered_cities.shp"

    # 讀取並處理 CSV 檔案
    print("處理承德幹線_go_bus_info.csv：")
    df1 = read_and_truncate_coordinates(file1)
    if df1 is not None:
        plot_bus_route(df1, geojson_path, shp_path, output_image="Chengde_Bus_Route_Map.jpg")