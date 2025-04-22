import os
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import def_bus_11022329
output_dir = 'C:\\Users\\User\\Desktop\\cycu_oop_11022360\\20250422'#輸入自己的路徑


if __name__ == "__main__":
    station_id = input("請輸入車站代號：")
    file_path = os.path.join(output_dir, f"{station_id}.html")
    go_output_csv_path = os.path.join(output_dir, 'go_bus_info.csv')
    file_path = os.path.join(output_dir, f"{station_id}.html")
    os.makedirs(output_dir, exist_ok=True)
    def_bus_11022329.bus_call(station_id, output_dir)
    


    # 提取去程與回程的公車資訊
    go_bus_info_list = def_bus_11022329.extract_bus_info_by_direction(file_path)

    def save_to_csv(data_list, file_path):
    # 確保資料不為空
        if not data_list:
            print(f"資料為空，無法儲存至 {file_path}")
            return

        # 取得資料的欄位名稱
        fieldnames = data_list[0].keys()

        # 將資料寫入 CSV 檔案
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_list)

    # 儲存去程與回程的公車資訊到不同的 CSV 檔案
    save_to_csv(go_bus_info_list, go_output_csv_path)
    

    print(f"去程公車資訊已儲存至 {go_output_csv_path}")

#0161001500(基隆路幹線)
#0161000900(承德幹線)
#https://ebus.gov.taipei/thb/StopsOfRoute?nameZh=1818%E8%87%BA%E5%8C%97%E2%86%92%E4%B8%AD%E5%A3%A2 (1818)