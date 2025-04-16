from datetime import datetime

def calculate_days_since(input_time_str):
    """
    計算輸入時間的星期幾，該日期是當年的第幾天，並計算該時刻到現在經過的太陽日數。

    :param input_time_str: str，輸入的時間，格式為 "YYYY-MM-DD HH:MM"
    :return: tuple，包含該天是星期幾 (str)、當年的第幾天 (int) 和該時刻到現在經過的太陽日數 (float)
    """
    try:
        # 將輸入的時間字串轉換為 datetime 物件
        input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")
        
        # 計算該天是星期幾
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday = weekdays[input_time.weekday()]
        
        # 計算該日期是當年的第幾天
        day_of_year = input_time.timetuple().tm_yday
        
        # 計算該時刻到現在經過的太陽日數
        now = datetime.now()
        delta = now - input_time
        days_since = delta.total_seconds() / 86400  # 將秒數轉換為天數
        
        return weekday, day_of_year, days_since
    except ValueError:
        raise ValueError("輸入的時間格式無效，請使用 'YYYY-MM-DD HH:MM' 格式。")

# 測試函數
if __name__ == "__main__":
    try:
        input_time_str = input("請輸入時間 (格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30): ")
        weekday, day_of_year, days_since = calculate_days_since(input_time_str)
        print(f"該天是：{weekday}")
        print(f"該日期是當年的第 {day_of_year} 天")
        print(f"該時刻到現在經過的太陽日數為：{days_since:.6f}")
    except ValueError as e:
        print(e)