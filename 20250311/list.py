import datetime
import lunarcalendar

#每個星期的英文
week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#每個月份的英文
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novermber', 'December']
#每個農曆年的十二生肖
zodiac = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']

#使用者輸入公曆日期
month_input = int(input('Enter month: '))
day = int(input('Enter day: '))
year = int(input('Enter year: '))
date = datetime.date(year, month_input, day)

#轉換成農曆
lunar_date = lunarcalendar.Converter.Solar2Lunar(date)

#輸出結果
print("Day of the week:", week[date.weekday()])
print("Month name:", month[date.month - 1])
print("Lunar Date:", f"{lunar_date.year}年{lunar_date.month}月{lunar_date.day}日")
print("Chinese zodiac:", zodiac[(lunar_date.year - 4) % 12])

