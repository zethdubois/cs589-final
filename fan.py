import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Constants for the visualization
radius = 10  # Adjust as needed
min_year = 1800  # Adjust based on your data
max_year = 2023  # Adjust based on your data
year_range = max_year - min_year

element_files = {
    'Li': 'LI-query_filtered.csv',
    'Al': 'AL-query_filtered.csv',
    # Add more elements and their file paths
}

# List of elements to include in the visualization
elements = list(element_files.keys())

# Define the circle
num_elements = len(elements)
angle_increment = 2 * np.pi / num_elements

# Create the composite fan chart
plt.figure(figsize=(12, 12))

for i, element in enumerate(elements):
    element_data = pd.read_csv(element_files[element], encoding='ISO-8859-1')

    start_angle = i * angle_increment

    for index, row in element_data.iterrows():
        # Normalize the discoveryYear to a value between 0 and 1
        year_normalized = (row['discoveryYear'] - min_year) / year_range

        # Calculate the angle for this line within the segment
        line_angle = start_angle + year_normalized * angle_increment

        # Calculate coordinates for line start (element) and end (mineral)
        x_start = radius * np.cos(start_angle)
        y_start = radius * np.sin(start_angle)
        x_end = radius * np.cos(line_angle)
        y_end = radius * np.sin(line_angle)

        # Plot line
        plt.plot([x_start, x_end], [y_start, y_end], marker='o')

        # Add text label at the end point
        plt.text(x_end, y_end, row['mineralName'], ha='left', va='center', 
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7), fontsize='small')

plt.title('Composite Visualization of Mineral Discoveries')
plt.axis('equal')  # Ensure the plot is circular
plt.show()


# plt.title('Lithium (Li) Minerals Discovery Timeline')
# plt.ylabel('Minerals')
# plt.xlabel('discoveryYear')

# # Set the starting point of Y-axis to 1800
# plt.xlim(left=1780)
# plt.xlim(right=2030)
