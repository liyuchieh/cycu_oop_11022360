import geopandas as gpd
import matplotlib.pyplot as plt
from folium import Map, CircleMarker
from folium.plugins import MarkerCluster

def visualize_bus_stops(file_path):
    """
    讀取 bus_stops.geojson 檔案並視覺化所有公車站點。
    :param file_path: bus_stops.geojson 檔案的路徑
    """
    try:
        # 讀取 GeoJSON 檔案為 GeoDataFrame
        gdf = gpd.read_file(file_path)
        
        # 確認 GeoDataFrame 是否包含資料
        if gdf.empty:
            print("GeoDataFrame 為空，請檢查檔案內容。")
            return
        
        # 使用 Matplotlib 繪製地圖並儲存為圖片
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(marker='o', color='blue', markersize=5, ax=ax)
        plt.title("Bus Stops Visualization (Matplotlib)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        output_image = "Bus Stops Visualization.jpg"
        plt.savefig(output_image, dpi=300)  # 儲存為 JPG 圖片
        plt.close(fig)  # 關閉圖表以釋放記憶體
        print(f"靜態地圖已儲存為 {output_image}")
        
        # 使用 Folium 繪製互動地圖
        center_lat = gdf.geometry.y.mean()
        center_lon = gdf.geometry.x.mean()
        folium_map = Map(location=[center_lat, center_lon], zoom_start=13)
        
        # 使用 MarkerCluster 群集顯示站點
        marker_cluster = MarkerCluster().add_to(folium_map)
        for _, row in gdf.iterrows():
            if row.geometry.is_empty:
                continue
            lat, lon = row.geometry.y, row.geometry.x
            CircleMarker(location=(lat, lon), radius=5, color='blue', fill=True, fill_opacity=0.7).add_to(marker_cluster)
        
        # 儲存互動地圖為 HTML
        output_html = "bus_stops_map.html"
        folium_map.save(output_html)
        print(f"互動地圖已儲存為 {output_html}")
    
    except Exception as e:
        print(f"發生錯誤：{e}")

# 範例使用
if __name__ == "__main__":
    geojson_path = "C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250422\\練習二.data\\bus_stops.geojson"  # 請將此路徑替換為實際檔案路徑
    visualize_bus_stops(geojson_path)