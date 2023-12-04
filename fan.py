import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk, StringVar, OptionMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to plot the selected element
def plot_element(element):
    plt.clf()  # Clear the current figure
    data = pd.read_csv(element_files[element], encoding='ISO-8859-1')

    # Find min and max discovery years for the selected element
    min_year = data['discoveryYear'].min()
    max_year = data['discoveryYear'].max()


    element_point = (0, 0)  # Central point for the element
    for index, row in data.iterrows():
        mineral_point = (row['discoveryYear'], index)
        plt.plot([element_point[0], mineral_point[0]], [element_point[1], mineral_point[1]], marker='o')
        plt.text(mineral_point[0]+2, mineral_point[1], row['mineralName'], ha='left', va='center')

    plt.title(f'{element} Minerals Discovery Timeline')
    plt.xlabel('Discovery Year')
    plt.ylabel('Mineral Count')

    # Set the limits for X based on the discovered min and max years
    plt.xlim(left=min_year, right=max_year)

    plt.draw()

# Initialize Tkinter window
root = Tk()
root.title("Element Fan Chart")

# Define your element_files dictionary
element_files = {
    'Li': 'LI-query_filtered.csv',
    'Al': 'AL-query_filtered.csv',
    # ... other elements
}

# Create a matplotlib figure
fig = plt.figure(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)  
widget = canvas.get_tk_widget()
widget.grid(row=0, column=1, sticky="nsew")

# Configure grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Dropdown menu for element selection
selected_element = StringVar(root)
selected_element.set(list(element_files.keys())[0])  # Set default value

dropdown = OptionMenu(root, selected_element, *element_files.keys(), command=plot_element)
dropdown.grid(row=0, column=0, sticky="ew")

root.mainloop()
