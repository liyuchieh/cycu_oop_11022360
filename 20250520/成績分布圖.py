import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv('20250520/老師資料/midterm_scores.csv')

# Define subjects and colors
subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'gray']

# Define bins: 0-10, 10-20, ..., 90-100
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
bin_centers = np.array(bins[:-1]) + 5  # Calculate the center of each bin

# Create a single plot
plt.figure(figsize=(12, 8))

# Bar width for each subject
bar_width = 8 / (len(subjects) + 1)

# Plot histograms for each subject with shifted positions
for i, (subject, color) in enumerate(zip(subjects, colors)):
    counts, _ = np.histogram(df[subject], bins=bins)
    plt.bar(bin_centers + i * bar_width, counts, width=bar_width, color=color, alpha=0.7, label=subject, edgecolor='black')

# Add labels, title, and legend
plt.xlabel('Score Range', fontsize=14)
plt.ylabel('Number of Students', fontsize=14)
plt.title('Score Distribution for All Subjects', fontsize=18)
plt.xticks(bin_centers + (len(subjects) - 1) * bar_width / 2, [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Subjects', fontsize=10)

# Show the plot
plt.tight_layout()
plt.show()