import matplotlib.pyplot as plt
import numpy as np # Import numpy for better array handling if needed, though not strictly required here.

# --- Data Definition ---
# Data for Run 1: Population Size 350
# Generations 0 to 63
conflicts_run1 = [2, 3, 2, 2, 3, 2, 2, 2, 1, 3, 3, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 3, 2, 2, 2, 2, 1, 2, 2, 3, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 0]
generations_run1 = list(range(len(conflicts_run1)))
label_run1 = 'Population Size 350'

# Data for Run 2: Cultural Algorithm (Pop Size 500)
# Generations 0 to 16
conflicts_run2 = [2, 2, 3, 3, 1, 2, 2, 2, 2, 2, 3, 2, 2, 3, 2, 2, 0]
generations_run2 = list(range(len(conflicts_run2)))
label_run2 = 'Cultural Algorithm (Pop Size 500)'

# Define the consistent green color scheme
LINE_COLOR = '#38A169' # A nice shade of green
FILL_COLOR = LINE_COLOR # Use the same base color for the fill
FILL_ALPHA = 0.3        # Define the transparency level separately

# Determine the max conflict value across both datasets to set a uniform scale
max_conflict_value = max(max(conflicts_run1), max(conflicts_run2))

# --- Plotting Configuration ---
# Create a figure with two vertical subplots (2 rows, 1 column)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=False) 

# --- Subplot 1: Run 1 (Pop Size 350) ---
ax1.set_title(f'Fitness Evolution Over Generations ({label_run1})', fontsize=14, fontweight='bold')

# Plot the line
ax1.plot(generations_run1, conflicts_run1, 
         label='Fitness (Conflicts)', 
         color=LINE_COLOR, 
         marker='o', 
         linestyle='-', 
         linewidth=2, 
         markersize=5)

# Fill the area beneath the line, using the new alpha parameter
ax1.fill_between(generations_run1, conflicts_run1, 0, color=FILL_COLOR, alpha=FILL_ALPHA)

# Aesthetics and Labels
ax1.set_ylabel('Conflicts', fontsize=12)
ax1.set_xlabel('Generation', fontsize=12) # Added X-label for consistency
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend(loc='upper right')

# Explicitly set y-axis limits starting at 0 and define integer ticks
ax1.set_ylim(0, max_conflict_value + 1)
ax1.set_yticks(range(max_conflict_value + 1))

# Set x-axis limits to start at 0
ax1.set_xlim(0, max(generations_run1))


# --- Subplot 2: Run 2 (Cultural Algorithm) ---
ax2.set_title(f'Fitness Evolution Over Generations ({label_run2})', fontsize=14, fontweight='bold')

# Plot the line
ax2.plot(generations_run2, conflicts_run2, 
         label='Fitness (Conflicts)', 
         color=LINE_COLOR, 
         marker='o', 
         linestyle='-', 
         linewidth=2, 
         markersize=5)

# Fill the area beneath the line, using the new alpha parameter
ax2.fill_between(generations_run2, conflicts_run2, 0, color=FILL_COLOR, alpha=FILL_ALPHA)

# Aesthetics and Labels
ax2.set_ylabel('Conflicts', fontsize=12)
ax2.set_xlabel('Generation', fontsize=12)
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend(loc='upper right')

# Explicitly set y-axis limits starting at 0 and define integer ticks
ax2.set_ylim(0, max_conflict_value + 1)
ax2.set_yticks(range(max_conflict_value + 1))

# Set x-axis limits to start at 0
ax2.set_xlim(0, max(generations_run2))

# Remove the default spacing between subplots and adjust plot area
plt.subplots_adjust(hspace=0.4) 
plt.tight_layout()

# Display the plot
plt.show()

