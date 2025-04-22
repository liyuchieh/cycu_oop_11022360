import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

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
    :return: 包含無條件捨去後的 latitude 和 longitude 的 DataFrame
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
        
        return df[['latitude', 'longitude']]
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None

def plot_bus_route(csv_data, geojson_path, output_image="Bus_Route_Map.jpg"):
    """
    根據 CSV 資料和 GeoJSON 檔案繪製公車路線圖。
    
    :param csv_data: 包含 latitude 和 longitude 的 DataFrame
    :param geojson_path: bus_stops.geojson 檔案的路徑
    :param output_image: 輸出的地圖圖片檔案名稱
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
        
        plt.title("Bus Route Map")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend()
        
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
    file2 = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250422\\練習一_data\\基隆路_go_bus_info.csv"
    geojson_path = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250422\\bus_stops.geojson"
    
    # 讀取並處理 CSV 檔案
    print("處理承德幹線_go_bus_info.csv：")
    df1 = read_and_truncate_coordinates(file1)
    if df1 is not None:
        plot_bus_route(df1, geojson_path, output_image="Chengde_Bus_Route_Map.jpg")
    
    print("\n處理基隆路_go_bus_info.csv：")
    df2 = read_and_truncate_coordinates(file2)
    if df2 is not None:
        plot_bus_route(df2, geojson_path, output_image="Keelung_Bus_Route_Map.jpg")