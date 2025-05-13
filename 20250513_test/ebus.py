import requests
from bs4 import BeautifulSoup

def get_bus_info_go(bus_id):
    # URL: https://ebus.gov.taipei/Route/StopsOfRoute?routeid={station_id}
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={bus_id}"
        # 發送請求
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    # 找到 <div id="GoDirectionRoute">
    go_direction_route = soup.find('div', id='GoDirectionRoute')
    if not go_direction_route:
        return []
    inputs = go_direction_route.find_all('input', id='item_UniStopId')
    bus_stops = [input_tag['value'].strip() for input_tag in inputs]
    
    return bus_stops
   

class BusInfo:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        
    def get_go_route_info(self):
       # URL: https://ebus.gov.taipei/Route/StopsOfRoute?routeid={station_id}
        url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={self.bus_id}"
        # 發送請求
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到 <div id="GoDirectionRoute">
        go_direction_route = soup.find('div', id='GoDirectionRoute')
        if not go_direction_route:
            return []

        # 提取站牌資訊
        stops = []
        for item in go_direction_route.find_all('a', class_='auto-list-link auto-list-stationlist-link'):
            number = item.find('span', class_='auto-list-stationlist-number').text.strip()
            place = item.find('span', class_='auto-list-stationlist-place').text.strip()
            latitude = item.find('input', id='item_Latitude')['value']
            longitude = item.find('input', id='item_Longitude')['value']
            stops.append({
                'number': number,
                'place': place,
                'latitude': latitude,
                'longitude': longitude
            })
        
        return stops


    def get_back_route_info(self):
        # URL: https://ebus.gov.taipei/Route/StopsOfRoute?routeid={station_id}
        url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={self.bus_id}"
        # 發送請求
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到 <div id="GoDirectionRoute">
        go_direction_route = soup.find('div', id='BackDirectionRoute')
        if not go_direction_route:
            return []

        # 提取 <span class="auto-list-stationlist-place"> 的文字
        spans = go_direction_route.find_all('span', class_='auto-list-stationlist-place')
        bus_stops = [span.text.strip() for span in spans]
        
        return bus_stops

    def get_stop_info(self):
        """
        Retrieve stop information for the bus.
        To be implemented.
        """
        pass

    def get_arrival_time_info(self):
        """
        Retrieve arrival time information for the bus.
        To be implemented.
        """
        pass

#執行get_bus_info_go函數
bus_id = "0161000900"
bus_stops = get_bus_info_go(bus_id)
print (bus_stops)

if __name__ == "__main__":
    bus = BusInfo("0161000900")
    print(f"Bus ID: {bus.bus_id}")
    print("Go Bus Stops:")
    for stop in bus.get_go_route_info():
        print(f"{stop}")
