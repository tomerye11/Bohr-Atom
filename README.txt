**Overview**

ElectronGraph.py is a Python script designed to read data from a results file, process the data into a usable format, and visualize it through a graph.

Steps Followed by the Program

1. Reading the Data:
    - The script reads a results file and extracts relevant data points.
    - It parses the file to retrieve `r` (distance) and `phi` (angle) values.

2. Converting Coordinates:
    - The extracted polar coordinates (`r`, `phi`) are converted into Cartesian coordinates (`x`, `y`).

3. Plotting the Data:
    - The plot is customized with labels, a title, and a grid for better visualization.

How to Use and Run the Program
-Prerequisites:
- Python 3.x installed on your machine.
- Required Python libraries: `numpy`, `matplotlib`, and `scipy`, you can install the necessary libraries using pip: pip install numpy matplotlib scipy

How to Run the Program:

- Prepare Your result files:
Ensure you have four result files containing the data in the expected format (r= value and phi= value).

-Run the script:
You can run the script from your command line or terminal. Navigate to the directory where the script is located and run:
python ElectronGraph.py

-Provide file paths when prompted:
The script will prompt you to enter the paths to the four result files. Enter the paths one by one.
Example Command Line Interaction:
$ python ElectronGraph.py
Please enter the path to the first results file: path/to/first_results.txt
Please enter the path to the second results file: path/to/second_results.txt
Please enter the path to the third results file: path/to/third_results.txt
Please enter the path to the fourth results file: path/to/fourth_results.txt

-View the plot:
After processing the files, the script will plot the ellipses based on the data from the result files.

