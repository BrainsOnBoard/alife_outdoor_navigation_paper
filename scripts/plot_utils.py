import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys

presentation = "presentation" in sys.argv[1:]

def remove_axis_junk(axis, despine_right=True):
    # Turn off grid
    axis.xaxis.grid(False)
    axis.yaxis.grid(False)

    sns.despine(ax=axis, right=despine_right)


def plot_grouped_bars(data, group_size, fig, axis, num_legend_col=2, legend_pad=0.2):
    columns = list(zip(*data))
    device = np.asarray(columns[0],  dtype=str)
    group = np.asarray(columns[1],  dtype=str)
    times = np.asarray(columns[2], dtype=float)

    errors = None if len(columns) < 4 else columns[3]

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

    # Build colour vector - colouring bars based on group
    pal = sns.color_palette()
    legend_actors = []
    colour = None
    num_bars = len(device)
    colour = [pal[j] for j in range(group_size)] * num_bars

    # Plot bars
    bars = axis.bar(bar_x, times, bar_width, color=colour, yerr=errors)

    legend_actors.extend(b for b in bars[:group_size])

    # Remove vertical grid and despine
    axis.xaxis.grid(False)
    sns.despine(ax=axis)

    # Use group names as x tick labels
    axis.set_xticks(group_x)
    unique_device = np.hstack((device[0::group_size], device))
    axis.set_xticklabels(unique_device)

    # Add legend
    fig.legend(legend_actors[:group_size], group[:group_size],
                ncol=num_legend_col, loc="lower center")

    # Set tight layout and save
    fig.tight_layout(pad=0, rect=[0.0, legend_pad, 1.0, 1.0])


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
