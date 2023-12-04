import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk, StringVar, OptionMenu, Scale, HORIZONTAL, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to plot the selected element
def plot_element(element, start_year, num_results):
    plt.clf()  # Clear the current figure
    data = pd.read_csv(element_files[element], encoding='ISO-8859-1')

    # Filter data based on start_year and num_results
    filtered_data = data[data['discoveryYear'] >= start_year].head(num_results)

    element_point = (0, 0)  # Central point for the element

    for index, row in filtered_data.iterrows():
        mineral_point = (row['discoveryYear'], index)
        plt.plot([element_point[0], mineral_point[0]], [element_point[1], mineral_point[1]], marker='o')
        plt.text(mineral_point[0]+2, mineral_point[1], row['mineralName'], ha='left', va='center')

    plt.title(f'{element} Minerals Discovery Timeline')
    plt.xlabel('Discovery Year')
    plt.ylabel('Mineral Count')
    plt.xlim(left=start_year)

    plt.draw()

def dropdown_changed(*args):
    update_sliders(selected_element.get())
    plot_element(selected_element.get(), start_year_slider.get(), num_results_slider.get())


# Initialize Tkinter window
root = Tk()
root.title("RDF Mineral Chart")

# Define your element_files dictionary
element_files = {
    'Lithium': 'LI-query_filtered.csv',
    'Aluminum': 'AL-query_filtered.csv',
    # ... other elements
}

# Dropdown menu for element selection
selected_element = StringVar(root)
selected_element.set(list(element_files.keys())[0])  # Set default value

# Load initial data to set slider range
initial_data = pd.read_csv(element_files[selected_element.get()])
initial_min_year = initial_data['discoveryYear'].min()
initial_max_year = initial_data['discoveryYear'].max()

# Create a matplotlib figure
fig = plt.figure(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.grid(row=1, column=0, columnspan=3, sticky="nsew")

# Load initial data to set slider range
initial_data = pd.read_csv(element_files[selected_element.get()])
initial_min_year = initial_data['discoveryYear'].min()
initial_max_year = initial_data['discoveryYear'].max()

# Starting Year Slider
start_year_slider = Scale(root, from_=initial_min_year, to=initial_max_year, orient=HORIZONTAL, label="Start Year")
start_year_slider.grid(row=2, column=0, columnspan=1, sticky="ew")

# Number of Results Slider
initial_num_results = min(100, len(initial_data))  # Adjust this as needed
num_results_slider = Scale(root, from_=1, to=initial_num_results, orient=HORIZONTAL, label="Number of Results")
num_results_slider.grid(row=2, column=1, columnspan=1, sticky="ew")

# Configure grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Dropdown menu for element selection
selected_element = StringVar(root)
selected_element.set(list(element_files.keys())[0])  # Set default value

# When element is changed via dropdown
dropdown = OptionMenu(root, selected_element, *element_files.keys(), command=dropdown_changed)
dropdown.grid(row=0, column=0, sticky="ew")


# Function to update the plot based on sliders
def update_plot(*args):
    plot_element(selected_element.get(), start_year_slider.get(), num_results_slider.get())

def update_sliders(element):
    # Load data
    data = pd.read_csv(element_files[element], encoding='ISO-8859-1')

    # Update start_year_slider range and value
    new_min_year = data['discoveryYear'].min()
    new_max_year = data['discoveryYear'].max()
    start_year_slider.config(from_=new_min_year, to=new_max_year,label=f"Start Year ({new_min_year} - {new_max_year})")
    start_year_slider.set(new_min_year)

    # Update num_results_slider
    new_max_results = len(data)
    num_results_slider.config(to=new_max_results, label=f"Number of Results (max {new_max_results})")
    num_results_slider.set(new_max_results // 2)

    # Redraw the plot with updated values
    plot_element(element, start_year_slider.get(), num_results_slider.get())



# Bind sliders and dropdown to update_plot function
start_year_slider.bind("<ButtonRelease-1>", update_plot)
num_results_slider.bind("<ButtonRelease-1>", update_plot)
selected_element.trace("w", update_plot)

# Configure grid
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


root.mainloop()