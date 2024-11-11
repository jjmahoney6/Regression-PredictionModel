import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from svgpathtools import svg2paths, Path
import pandas as pd
import numpy as np

# Load SVG paths and attributes
svg_file = "/Users/nathanwillemsen/Downloads/sections_test.svg"
paths, attributes = svg2paths(svg_file)

# Define a gradient from gray to red
gradient = mcolors.LinearSegmentedColormap.from_list("custom_gradient", ["#808080", "#ab162b"])

# Sample data with percentages for each section (replace with actual data as needed)
data = {
    'section_id': ['section_1', 'section_2', 'section_3', 'section_4', 'section_5', 'section_6', 
                   'section_7', 'section_8', 'section_9', 'section_10', 'section_11', 'section_12', 
                    'section_13', 'section_14', 'section_15', 'section_16', 'section_17', 'section_18', ],  # Example section IDs
    'percentage': [10, 25, 55, 75, 90, 10, 25, 55, 75, 90, 10, 25, 55, 75, 90, 11, 11, 11]  # Example percentages for each section
}
df = pd.DataFrame(data)
# Normalize percentages for color mapping
norm = plt.Normalize(df['percentage'].min(), df['percentage'].max())

# Create a figure
fig, ax = plt.subplots(figsize=(10, 10))

# Define a function to sample points along the path
def sample_path(path, num_points=100):
    """Sample points along the SVG path."""
    points = []
    for seg in path:
        points += [seg.point(t) for t in np.linspace(0, 1, num_points)]
    return points

# Map each section with colors based on percentage
for path, attr in zip(paths, attributes):
    section_id = attr.get('id', None)
    if section_id and section_id in df['section_id'].values:
        # Get the corresponding percentage
        percentage = df.loc[df['section_id'] == section_id, 'percentage'].values[0]
        section_color = gradient(norm(percentage))

        # Sample points from path to approximate as polygon
        sampled_points = sample_path(path)
        x_vals = [p.real for p in sampled_points]  # Real part for x-coordinate
        y_vals = [p.imag for p in sampled_points]  # Imaginary part for y-coordinate

        # Plot the section as a filled polygon
        ax.fill(x_vals, y_vals, color=section_color, edgecolor='black', linewidth=0.5)

# Adjust plot
ax.set_aspect('equal')
ax.axis('off')  # Hide axes for a clean look
plt.title("Polar Park Sections Colored by Percentage")

plt.show()