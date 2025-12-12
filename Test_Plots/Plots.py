import matplotlib.pyplot as plt
import numpy as np

# Define the board sizes (N) for the x-axis
N_values = np.array([4, 8, 16, 32])

# Define the execution times (Seconds) for each algorithm.
# Note: For N=32, "Did not finish" or "Got Stuck" are assigned large time estimates
# to represent the practical failure on the logarithmic scale.

# 1. Backtracking (BT) - Blue Line
# Data: [0.001, 0.010, 60.0, 'Did not finish']
time_bt = np.array([0.001, 0.010, 60.0, 100000.0]) # 10^5 s is a high estimate for DNF

# 2. Hill Climbing (HC) - Red Line
# Data: [0.001, 0.017, 8.0, 120.0 (2 min)]
time_hc = np.array([0.001, 0.017, 8.0, 120.0])

# 3. Cultural Algorithm (CA) - Yellow Line
# Data: [0.001, 0.040, 15.0, 60.0 (1 min)]
# We use 'gold' for the color to match the visual feel of the original yellow line.
time_ca = np.array([0.001, 0.040, 15.0, 60.0])

# 4. Best-First Search (BFS) - Green Line
# Data: [0.001, 0.025, 9.0, 'Got Stuck']
time_bfs = np.array([0.001, 0.025, 9.0, 10000.0]) # 10^4 s is a high estimate for stuck

# --- Plotting Configuration ---

plt.figure(figsize=(10, 6))

# Plot the data points using lines and markers ('o-')
# Colors are matched to the provided image's legend
plt.plot(N_values, time_bt, 'o-', color='blue', label='Backtracking (Blue Line)')
plt.plot(N_values, time_hc, 'o-', color='red', label='Hill Climbing (Red Line)')
plt.plot(N_values, time_bfs, 'o-', color='green', label='Best-First Search (Green Line)')
plt.plot(N_values, time_ca, 'o-', color='gold', label='Cultural Algorithm (Yellow Line)')

# Set the y-axis to a logarithmic scale, as execution time scales rapidly
plt.yscale('log')

# Set the x-axis ticks to only show the N values we have data for
plt.xticks(N_values)
plt.xlim(3, 33) # Set limits to space out the N=4 and N=32 points

# Add titles and labels
plt.title('Algorithm Execution Time Scaling for N-Queens Problem')
plt.xlabel('Board Size (N)')
plt.ylabel('Average Execution Time (Seconds) - Logarithmic Scale')

# Add a legend to identify the lines
plt.legend(loc='upper left')

# Add grid lines for better readability on the logarithmic scale
plt.grid(True, which="both", ls="--", alpha=0.6)

# Display the plot
plt.show()