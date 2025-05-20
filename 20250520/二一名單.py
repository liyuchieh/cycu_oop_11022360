import pandas as pd

# Load CSV data
df = pd.read_csv('20250520/老師資料/midterm_scores.csv')

# Define the subjects to calculate the average
subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']


# Check for students with four or more scores below 60
students_below_60 = []
for index, row in df.iterrows():
    scores_below_60 = sum(score < 60 for score in row[subjects])
    if scores_below_60 >= 4:
        students_below_60.append(row['Name'])

# Output the list of names and the total count
print("\n二一名單:")
print(students_below_60)
print(f"\n總人數: {len(students_below_60)}")

# Save the list to a CSV file
output_df = pd.DataFrame({'Name': students_below_60})
output_df.to_csv('20250520/二一名單.csv', index=False, encoding='utf-8-sig')
print("\n名單已儲存為 '20250520/二一名單.csv'")