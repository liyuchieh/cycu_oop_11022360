import geopandas as gpd
import os

# 找出 taipei_town 目錄下的第一個 .shp 檔案
shp_dir = "20250520/老師資料/鄉鎮市"
shp_file = None
for fname in os.listdir(shp_dir):
    if fname.endswith(".shp"):
        shp_file = os.path.join(shp_dir, fname)
        break

if shp_file is None:
    print("No shapefile found in", shp_dir)
else:
    # 讀取 shapefile
    gdf = gpd.read_file(shp_file)
    
    # 篩選台北市、新北市、基隆市和桃園市
    target_cities = ["臺北市", "新北市", "基隆市", "桃園市"]
    filtered_gdf = gdf[gdf['COUNTYNAME'].isin(target_cities)]  # 假設 CITYNAME 欄位包含城市名稱

    # 儲存篩選後的資料為新的 shapefile
    output_file = os.path.join(shp_dir, "filtered_cities.shp")
    filtered_gdf.to_file(output_file, encoding='utf-8')
    print(f"Filtered shapefile saved to {output_file}")