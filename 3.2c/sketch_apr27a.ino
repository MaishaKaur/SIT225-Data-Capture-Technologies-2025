import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd

# Define the correct file path
file_path = "task31.csv"
try:
    # Read CSV file 
    data = pd.read_csv(file_path, header=None)
    # Ensure the CSV has exactly 3 columns (X, Y, Z values)
    if data.shape[1] != 3:
        raise ValueError("CSV file must have exactly 3 columns for X, Y, and Z values.")

    # Extract X, Y, and Z values
    time = list(range(len(data)))  # Generate a time index (0, 1, 2, ...)
    x_values = data.iloc[:, 0]  # First column (X-axis)
    y_values = data.iloc[:, 1]  # Second column (Y-axis)
    z_values = data.iloc[:, 2]  # Third column (Z-axis)

    # Plot data
    plt.figure(figsize=(10, 5))
    plt.plot(time, x_values, label="X-axis", marker="o", linestyle="-")
    plt.plot(time, y_values, label="Y-axis", marker="s", linestyle="--")
    plt.plot(time, z_values, label="Z-axis", marker="^", linestyle=":")

    # Formatting
    plt.xlabel("Time Index")
    plt.ylabel("Acceleration")
    plt.title("Accelerometer Readings Over Time")
    plt.legend()
    plt.grid(True)

    # Save the plot as an image instead of displaying it (to avoid Tkinter issues)
    plt.savefig("accelerometer_plot.png")
    print("Plot saved as 'accelerometer_plot.png'")

except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
except pd.errors.ParserError:
    print("Error: CSV file format is incorrect. Check for missing values or wrong delimiter.")
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
except ValueError as e:
    print(f"Error reading file: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")