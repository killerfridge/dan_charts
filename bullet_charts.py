import matplotlib.pyplot as plt
import pandas as pd
import philips_colors as pc


def bullet_chart(
        data:pd.DataFrame,
        x: str,
        y: list,
        target: str,
        bar: str,
        aggfunc: str='sum',
        size: tuple=(10,7),
        title: str=None,
        x_label: str=None,
        colors: dict=None,
        ):
    """
    param data: pd.DataFrame - dataframe containing the data to be plotted
    param x: str - column name that contains the x values
    param y: list - list of columns to group for the y axis
    param target: str - column name that contains the target data
    param bar: str - column name that contains the sub_target data
    param aggfunc: str - how to aggregate the values (e.g. sum, mean etc.)
    param size: tuple - figure size
    param title: str - figure title
    param x_label: str - x_axis label
    returns tuple: matplotlib figure and axis
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(f'data parameter should be of type pd.DataFrame, not {type(data)}')
    if not isinstance(x, str):
        raise TypeError(f'x parameter should be of type str, not {type(x)}')
    if not isinstance(target, str):
        raise TypeError(f'target parameter should be of type str, not {type(target)}')
    if not isinstance(bar, str):
        raise TypeError(f'bar parameter should be of type str, not {type(bar)}')
    if not isinstance(size, tuple):
        raise TypeError(f'size parameter should be of type tuple, not {type(size)}')
    if not isinstance(title, str):
        raise TypeError(f'title parameter should be of type str, not {type(title)}')
    if not isinstance(x_label, str):
        raise TypeError(f'x_label parameter should be of type str, not {type(x_label)}')
    
    # Create the grouped dataframe using the passed arguments

    grouped = data.groupby(y).agg({x: aggfunc, bar: aggfunc, target: aggfunc}).reset_index().copy

    number_of_axes = len(grouped[y])

    # If the number of axes is greater than 1, then create an array of axes, else just create one

    if number_of_axes > 1:
        fig, axarr = plt.subplots(number_of_axes, figsize=size)
    else:
        fig, ax = plt.subplots(figsize=size)


    if not isinstance(colors: dict):
        raise TypeError(f'colors parameter should be a dictionary, not {type(colors)}')

    if not colors:
        colors = {
                'target': pc.tableau_hex[0],
                'bar': pc.tableau_hex[15],
                'x_values': pc.tableau_hex[6]
                }

    try:
        bar_color = colors['bar']
    except:
        bar_color = pc.tableau_hex[15]

    try:
        target_color = colors['target']
    except:
        target_color = pc.tableau_hex[0]

    try:
        x_color = colors['x_values']
    except:
        x_color = pc.tableau_hex[6]

    # take the the raw data from the dataframe

    y_labels = grouped[y].values
    x_values = grouped[x].values
    bar_values = grouped[bar].values
    target_values = grouped[target].values

    # Get the height of the bar based on the maximum values

    height = max(max(x_values), max(bar_values), max(target_values))

    height = height / 10

    # Loop through the Y labels, and plot the charts

    for i, y_label in enumerate(y_labels):

        # If the number of axis is greater than one, assign the current one to ax
        if number_of_axis > 1:
            ax = axarr[i]
        # plot the background bar 
        ax.barh([1], bar_values[i], color=bar_color) 

        # If the x value is less than the target value, plot it red, else green

        if x_values[i] > target_values[i]:
            x_color = pc.tableau_hex[4]
            
        # plot the x value bar

        ax.barh([1], x_values[i], height=height/3, color=x_color)


        # plot the target line

        ax.vlines(target_values[i], linewidth=3, color=target_color)

        fig.subplots_adjust(hspace=0)

    # set the final axes label
    ax.set_xlabel(x_label)

    if number_of_axis == 1:
        axarr = ax

    return fig, axarr


