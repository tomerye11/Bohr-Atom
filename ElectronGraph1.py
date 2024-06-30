import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.optimize import least_squares
from matplotlib.ticker import FuncFormatter, MaxNLocator

# Function to read the results from a file and extract relevant data
def getResults(resultFilePath: str):
    # Open the result file for reading
    with open(resultFilePath, "r") as resultFile:
        resultLines = resultFile.readlines()

    resultsArr = []
    phi_arr = []
    roh_arr = []

    # Parse each line to extract 'r' and 'phi' values
    for i in range(len(resultLines)):
        currLine = resultLines[i]

        # Extract 'r' value
        r_index = currLine.find("r= ") + 3
        r_val = currLine[r_index:]
        r = float(r_val[:r_val.find("\t")])
        roh_arr.append(r)

        # Extract 'phi' value
        phi_index = currLine.find("phi= ") + 5
        phi_val = currLine[phi_index:]
        phi = float(phi_val[:phi_val.find("\t")])
        phi_arr.append(phi)

    # Combine 'phi' and 'r' values into a numpy array
    resultsArr = np.vstack((phi_arr, roh_arr))

    return resultsArr

# Function to convert polar coordinates to Cartesian coordinates
def polarToCartesian(phi_arr, roh_arr):
    x = roh_arr * np.cos(phi_arr)
    y = roh_arr * np.sin(phi_arr)
    return x, y

# Function to plot points and connect them from multiple result files with different dashed lines
def plotMultiplePoints(resultFilePaths):
    fig, ax = plt.subplots()
    line_styles = ['-', '--', '-.', ':']

    for idx, resultFilePath in enumerate(resultFilePaths):
        resultsArr = getResults(resultFilePath)
        phi_arr, roh_arr = resultsArr

        # Convert polar coordinates to Cartesian coordinates for plotting
        x, y = polarToCartesian(phi_arr, roh_arr)

        # Plot and connect the points with different dashed lines
        ax.plot(np.append(x, x[0]), np.append(y, y[0]), linestyle=line_styles[idx % len(line_styles)],)

    # Change the tick labels on the axes
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    formatter = FuncFormatter(lambda x, _: f'{x * 1e8:.0f}')
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_title('(d)')

    ax.legend()
    plt.grid(True)
    plt.show()

# Example usage
resultFilePaths = ['results1.txt', 'results2.txt','results3.txt' , 'results4.txt']
plotMultiplePoints(resultFilePaths)

