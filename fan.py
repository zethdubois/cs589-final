import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('LI-query_filtered.csv')

# Create the fan chart
plt.figure(figsize=(12, 8))
li_point = (0, 0)  # Central point for 'Li'

for index, row in data.iterrows():
    mineral_point = (row['discoveryYear'], index)
    plt.plot([li_point[0], mineral_point[0]], [li_point[1], mineral_point[1]], marker='o')
    plt.text(mineral_point[0] + 2, mineral_point[1], row['mineralName'], va='center', ha='left',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, boxstyle='round,pad=0'),
        fontsize='small')



plt.title('Lithium (Li) Minerals Discovery Timeline')
plt.ylabel('Minerals')
plt.xlabel('Discovery Year')

# Set the starting point of Y-axis to 1800
plt.xlim(left=1780)
plt.xlim(right=2030)

plt.show()
