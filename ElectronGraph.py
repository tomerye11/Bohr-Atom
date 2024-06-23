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
def polar_to_cartesian(resultsArr):
    # Extract 'phi' and 'roh' values
    phi_arr = resultsArr[0]
    roh_arr = resultsArr[1]
    
    # Convert polar to Cartesian coordinates
    x_arr = roh_arr * np.cos(phi_arr)
    y_arr = roh_arr * np.sin(phi_arr)
    
    # Combine 'x' and 'y' values into a numpy array
    cartesian_points = np.vstack((x_arr, y_arr))
    
    return cartesian_points

# Function to fit an ellipse to the given Cartesian points
def fit_ellipse(cartesian_points):
    x = cartesian_points[0]
    y = cartesian_points[1]

    # Calculate the center of the ellipse
    x_m = np.mean(x)
    y_m = np.mean(y)
    
    def calc_R(x, y, xc, yc):
        return np.sqrt((x - xc)**2 + (y - yc)**2)
    
    def f_2(c):
        Ri = calc_R(x, y, *c)
        return Ri - Ri.mean()
    
    # Optimize the center estimate
    center_estimate = x_m, y_m
    center_optimized = least_squares(f_2, center_estimate)
    xc, yc = center_optimized.x

    # Calculate the main and minor axes of the ellipse
    D1 = np.vstack([x**2, x * y, y**2, x, y, np.ones_like(x)]).T
    S1 = np.dot(D1.T, D1)
    C1 = np.zeros([6, 6])
    C1[0, 2] = 2
    C1[2, 0] = 2
    C1[1, 1] = -1
    E, V = np.linalg.eig(np.dot(np.linalg.inv(S1), C1))
    n = np.argmax(np.abs(E))
    a = V[:, n]

    # Function to calculate the center of the ellipse
    def ellipse_center(a):
        b, c, d, f, g, a = a[1] / 2, a[2], a[3] / 2, a[4] / 2, a[5], a[0]
        num = b * b - a * c
        x0 = (c * d - b * f) / num
        y0 = (a * f - b * d) / num
        return np.array([x0, y0])

    # Function to calculate the lengths of the ellipse's axes
    def ellipse_axis_length(a):
        b, c, d, f, g, a = a[1] / 2, a[2], a[3] / 2, a[4] / 2, a[5], a[0]
        up = 2 * (a * f * f + c * d * d + g * b * b - 2 * b * d * f - a * c * g)
        down1 = (b * b - a * c) * ((c - a) * np.sqrt(1 + 4 * b * b / ((a - c) * (a - c))) - (c + a))
        down2 = (b * b - a * c) * ((a - c) * np.sqrt(1 + 4 * b * b / ((a - c) * (a - c))) - (c + a))
        res1 = np.sqrt(up / down1)
        res2 = np.sqrt(up / down2)
        return np.array([res1, res2])

    # Function to calculate the rotation angle of the ellipse
    def ellipse_angle_of_rotation(a):
        b, c, d, f, g, a = a[1] / 2, a[2], a[3] / 2, a[4] / 2, a[5], a[0]
        return 0.5 * np.arctan(2 * b / (a - c))

    # Get the ellipse parameters
    center = ellipse_center(a)
    axis_length = ellipse_axis_length(a)
    angle = ellipse_angle_of_rotation(a)
    
    xc, yc = center
    major_axis, minor_axis = axis_length
    rotation_angle = angle
    
    return np.array([xc, yc, major_axis, minor_axis, rotation_angle])

# Function to plot multiple ellipses on a single plot
def plot_multiple_ellipses(ellipses):
    fig, ax = plt.subplots(figsize=(7, 7))  # Increase the plot size

    colors = ['r', 'g', 'b', 'm', 'c', 'y', 'k']  # List of colors
    line_styles = ['-', '--', '-.', ':']  # List of line styles
    
    # Add each ellipse to the plot
    for i, ellipse_params in enumerate(ellipses):
        xc, yc, major_axis, minor_axis, rotation_angle = ellipse_params
        color = colors[i % len(colors)]
        line_style = line_styles[i % len(line_styles)]
        ellipse = Ellipse((xc, yc), 2 * major_axis, 2 * minor_axis, angle=np.degrees(rotation_angle), 
                          edgecolor=color, facecolor='none', linestyle=line_style, linewidth=2)
        ax.add_patch(ellipse)

    ax.set_aspect('equal', 'box')
    
    max_major_axis = max(ellipse[2] for ellipse in ellipses)
    max_minor_axis = max(ellipse[3] for ellipse in ellipses)
    xc_values = [ellipse[0] for ellipse in ellipses]
    yc_values = [ellipse[1] for ellipse in ellipses]

    x_min, x_max = min(xc_values) - 1.5 * max_major_axis, max(xc_values) + 1.5 * max_major_axis
    y_min, y_max = min(yc_values) - 1.5 * max_minor_axis, max(yc_values) + 1.5 * max_minor_axis
    
    # Set the axis range to be equal
    max_range = max(x_max - x_min, y_max - y_min)
    mid_x = (x_max + x_min) / 2
    mid_y = (y_max + y_min) / 2

    ax.set_xlim(mid_x - max_range / 2, mid_x + max_range / 2)
    ax.set_ylim(mid_y - max_range / 2, mid_y + max_range / 2)
    
    # Change the tick labels on the axes
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    formatter = FuncFormatter(lambda x, _: f'{x * 1e8:.0f}')
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_title('(d)')
    
    plt.grid(True)
    plt.show()

# Main function to run the program
def main():
    # Get paths to the result files from the user
    file_paths = [
        input("Please enter the path to the first results file: "),
        input("Please enter the path to the second results file: "),
        input("Please enter the path to the third results file: "),
        input("Please enter the path to the fourth results file: ")
    ]

    # Process each result file and plot the ellipses
    results = [getResults(file_path) for file_path in file_paths]
    cartesian_points = [polar_to_cartesian(result) for result in results]
    ellipses = [fit_ellipse(points) for points in cartesian_points]

    plot_multiple_ellipses(ellipses)

# Run the main function
if __name__ == "__main__":
    main()
