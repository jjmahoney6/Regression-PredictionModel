import matplotlib.pyplot as plt

# Define the style dictionary
plot_style = {
    'font.family': 'Arial',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'text.color': '#FFFFFF',
    'axes.edgecolor': '#000000',
    'axes.facecolor': '#FFFFFF',
    'xtick.color': '#000000',
    'ytick.color': '#000000',
    'grid.color': '#000000',
    'lines.color': '#ab162b',
    'lines.linewidth': 2,
    'legend.frameon': False,
    'legend.loc': 'upper right'
}

# Apply the style
plt.rcParams.update(plot_style)

# Example plot
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y1, label="Sine Wave", color='#ab162b')  # Red color from the style
plt.plot(x, y2, label="Cosine Wave", color='#000000')  # Black color for contrast
plt.title("Example Plot with Custom Style")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.grid(True)
plt.show()


# Define colors for gradient from gray to red (#ab162b)
start_color = "#808080"  # Gray
end_color = "#ab162b"    # Red

# Create a color gradient function
gradient = mcolors.LinearSegmentedColormap.from_list("custom_gradient", [start_color, end_color])

# Generate a color palette of 6 colors evenly spaced along the gradient
num_colors = 6
color_palette = [gradient(i / (num_colors - 1)) for i in range(num_colors)]

# Display the color palette for reference
fig, ax = plt.subplots(figsize=(6, 1), subplot_kw=dict(xticks=[], yticks=[], frame_on=False))
ax.imshow([color_palette], aspect='auto')
plt.title("Custom Color Palette")
plt.show()

# Example plot using the color palette
x = np.linspace(0, 10, 100)
y_values = [np.sin(x + i) for i in range(num_colors)]

plt.figure(figsize=(8, 6))
for i, y in enumerate(y_values):
    plt.plot(x, y, label=f"Line {i + 1}", color=color_palette[i])  # Use colors from the palette

plt.title("Example Plot with Custom Gradient Palette")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.grid(True)
plt.show()