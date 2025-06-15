import requests
from bs4 import BeautifulSoup
import openpyxl

def fetch_all_routes():
    """從網站抓取所有 route_id 和 route_name"""
    url = "https://ebus.gov.taipei/ebus"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        routes = []
        # 找到所有 <li><a href="javascript:go('0100000A00')">0東</a></li>
        for li in soup.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag and "javascript:go" in a_tag['href']:
                route_id = a_tag['href'].split("'")[1]  # 提取 route_id
                route_name = a_tag.get_text(strip=True)  # 提取 route_name
                routes.append((route_id, route_name))
        return routes
    else:
        print("無法連接到網站，請檢查網址或網路連線。")
        return []

def fetch_stops(route_id):
    """根據 route_id 抓取站名資料"""
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 去程站名
        go_direction_route = soup.find('div', id='GoDirectionRoute', class_='auto-list-pool-c stationlist-list-pool-c')
        go_stops = [station.get_text(strip=True) for station in go_direction_route.find_all('span', class_='auto-list-stationlist-place')] if go_direction_route else []
        # 返程站名
        back_direction_route = soup.find('div', id='BackDirectionRoute', class_='auto-list-pool-c stationlist-list-pool-c')
        back_stops = [station.get_text(strip=True) for station in back_direction_route.find_all('span', class_='auto-list-stationlist-place')] if back_direction_route else []
        return go_stops, back_stops
    else:
        print(f"無法讀取 route_id={route_id} 的資料。")
        return [], []

def save_to_excel(data, file_name="taipei_bus_stops.xlsx"):
    """將資料儲存到 Excel"""
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Bus Stops"
    # 寫入標題行
    sheet.append(["Route ID", "Route Name", "Direction", "Stops"])
    # 寫入資料
    for route_id, route_name, go_stops, back_stops in data:
        # 去程
        sheet.append([route_id, route_name, "Go", ", ".join(go_stops)])
        # 回程
        sheet.append([route_id, route_name, "Back", ", ".join(back_stops)])
    # 儲存檔案
    workbook.save(file_name)
    print(f"資料已成功儲存到 {file_name}")

def main():
    # 抓取所有路線
    routes = fetch_all_routes()
    if not routes:
        print("未找到任何路線資料，程式結束。")
        return

    # 抓取每條路線的站名
    all_data = []
    for route_id, route_name in routes:
        print(f"正在處理路線 {route_name} (ID: {route_id})...")
        go_stops, back_stops = fetch_stops(route_id)
        all_data.append((route_id, route_name, go_stops, back_stops))

    # 儲存到 Excel
    save_to_excel(all_data)

if __name__ == "__main__":
    main()
