from datetime import datetime

def calculate_julian_date(input_time_str):
    """
    計算輸入時間的星期幾，並計算該時刻的 Julian Date。

    :param input_time_str: str，輸入的時間，格式為 "YYYY-MM-DD HH:MM"
    :return: tuple，包含該天是星期幾 (str) 和該時刻的 Julian Date (float)
    """
    try:
        # 將輸入的時間字串轉換為 datetime 物件
        input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")
        
        # 計算該天是星期幾
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday = weekdays[input_time.weekday()]
        
        # 計算輸入時間的 Julian Date
        julian_date_input = calculate_julian_date_from_datetime(input_time)
        
        return weekday, julian_date_input
    except ValueError:
        raise ValueError("輸入的時間格式無效，請使用 'YYYY-MM-DD HH:MM' 格式。")

def calculate_julian_date_from_datetime(dt):
    """
    根據 datetime 物件計算 Julian Date。

    :param dt: datetime，輸入的日期時間
    :return: float，對應的 Julian Date
    """
    year = dt.year
    month = dt.month
    day = dt.day + dt.hour / 24 + dt.minute / 1440  # 將時間轉換為小數部分的天數

    # 如果月份是 1 月或 2 月，將年份減 1，月份加 12
    if month <= 2:
        year -= 1
        month += 12

    # 計算 Julian Date
    A = year // 100
    B = 2 - A + (A // 4)
    julian_date = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return julian_date

# 測試函數
if __name__ == "__main__":
    try:
        input_time_str = input("請輸入時間 (格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30): ")
        weekday, julian_date_input = calculate_julian_date(input_time_str)
        print(f"該天是：{weekday}")
        print(f"該時刻的 Julian Date 為：{julian_date_input:.6f}")
    except ValueError as e:
        print(e)