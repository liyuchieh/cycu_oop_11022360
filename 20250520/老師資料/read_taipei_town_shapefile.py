import geopandas as gpd
import matplotlib.pyplot as plt
import os

# 找出 taipei_town 目錄下的第一個 .shp 檔案
shp_dir = "20250520/taipei_town"
shp_file = None
for fname in os.listdir(shp_dir):
    if fname.endswith(".shp"):
        shp_file = os.path.join(shp_dir, fname)
        break

if shp_file is None:
    print("No shapefile found in", shp_dir)
else:
    gdf = gpd.read_file(shp_file)
    gdf.plot(edgecolor='black', figsize=(8, 8))
    plt.title("Taipei Town Shapefile")
    plt.axis('equal')
    plt.show()
