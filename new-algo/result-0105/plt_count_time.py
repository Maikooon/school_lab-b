import pandas as pd
import matplotlib.pyplot as plt

# Data points
total_check_count = [0, 11734, 22582, 33819, 45463, 55815, 56426, 57145]
execution_time_ns = [
    763198166,
    1261354959,
    1906780541,
    2751929750,
    4519731875,
    5203566000,
    4562002709,
    4626312625,
]

total_check_count = sorted(total_check_count)


# Convert execution time from nanoseconds to seconds for better readability
execution_time_sec = [t / 1e9 for t in execution_time_ns]

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.scatter(total_check_count, execution_time_sec, color="blue", label="Data Points")
plt.plot(
    total_check_count,
    execution_time_sec,
    linestyle="--",
    color="blue",
    label="Trend Line",
)
plt.title("Program Execution Time vs Total Check Count")
plt.xlabel("Total Check Count")
plt.ylabel("Program Execution Time (seconds)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.savefig("*execution_time_vs_total_check_count.png")
plt.show()
