import numpy as np
import matplotlib.pyplot as plt

def create_stream_plot(x_min, x_max, x_points, y_min, y_max, y_points, numerator, denominator=(lambda x, y: 1)):
    """
    Create a stream plot for the differential equation dy/dx = numerator/denominator.
    Numerator and denominator are functions that take two inputs (x, y) and return a value.
    Denominator defaults to returning 1 regardless of input.
    The grid should have the specified number of points in the x-direction and y-direction within the specified ranges.
    Return the figure and axes created.
    """
    x_values = np.linspace(x_min, x_max, x_points)
    y_values = np.linspace(y_min, y_max, y_points)
    x, y = np.meshgrid(x_values, y_values, sparse=True)

    top = numerator(x, y)
    bottom = denominator(x, y)
    magnitude = np.sqrt(top**2 + bottom**2)
    x_arrows = bottom / magnitude
    y_arrows = top / magnitude

    fig, ax = plt.subplots()
    ax.streamplot(x_values, y_values, x_arrows, y_arrows)

    return fig, ax
