import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys

presentation = "presentation" in sys.argv[1:]

def remove_axis_junk(axis):
    # Turn off grid
    axis.xaxis.grid(False)
    axis.yaxis.grid(False)

    sns.despine(ax=axis)


def plot_grouped_bars(data, group_size, fig, axis, num_legend_col=2):
    columns = list(zip(*data))
    device = np.asarray(columns[0],  dtype=str)
    group = np.asarray(columns[1],  dtype=str)
    time_col_start = 1 if group_size is None else 2

    # Read times into numpy arrays
    num_time_columns = len(columns) - time_col_start
    times = np.empty((num_time_columns, len(device)), dtype=float)
    for i, col in enumerate(columns[time_col_start:]):
        times[i,:] = col

    # Correctly place bars
    bar_width = 0.8

    # If there are no groups space bars evenly
    group_x = []
    bar_pad = 0.1
    group_pad = 1.0
    start = 0.0
    bar_x = np.empty(len(device))

    # Calculate bar positions of grouped GPU bars
    for d in range(0, len(device), group_size):
        end = start + ((bar_width + bar_pad) * group_size)
        bar_x[d:d + group_size] = np.arange(start, end, bar_width + bar_pad)[:group_size]

        group_x.append(start + ((end - bar_width - start) * 0.5))

        # Update start for next group
        start = end + group_pad

    assert len(bar_x) == len(device)
    offset = np.zeros(len(bar_x))


    pal = sns.color_palette()
    legend_actors = []
    for i in range(times.shape[0]):
        # Build colour vector - colouring bars based on group and stack height
        colour = None
        num_bars = len(device)
        colour = [pal[(i * group_size) + j] for j in range(group_size)] * num_bars

        bars = axis.bar(bar_x, times[i,:], bar_width, offset, color=colour)

        if group_size is None:
            legend_actors.append(bars[0])
        else:
            legend_actors.extend(b for b in bars[:group_size])
        offset += times[i,:]




    # Remove vertical grid
    axis.xaxis.grid(False)

    # Use group names as x tick labels
    axis.set_xticks(group_x)
    unique_device = np.hstack((device[0::group_size], device))
    axis.set_xticklabels(unique_device)

    # Add legend
    fig.legend(legend_actors[:group_size], group[:group_size],
                ncol=num_legend_col, loc="lower center")

    # Set tight layout and save
    fig.tight_layout(pad=0, rect=[0.0, 0.2, 1.0, 1.0])


# Set the plotting style
if presentation:
    sns.set(context="talk")
    sns.set_style("whitegrid", {"font.family":"sans-serif", "font.sans-serif":"Verdana"})
else:
    sns.set(context="paper")
    sns.set_style("whitegrid", {"font.family":"serif", "font.serif":"Times New Roman"})

# **HACK** fix bug with markers
sns.set_context(rc={"lines.markeredgewidth": 1.0})

gutter_width = 0.38
column_width = 3.31
double_column_width = (column_width * 2.0) + gutter_width
