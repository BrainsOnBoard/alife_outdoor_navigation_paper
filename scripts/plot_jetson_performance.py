import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import plot_utils

# neuron simulation, synapse simulation, Total simulation time,

jetson_test_data= [("10", "P.M. raw", 6.2),
                   ("10", "P.M. watershed", 5.8),
                   #("10", "P.M. horizon", 1.16),
                   ("10", "InfoMax raw", 463,2447),
                   ("10", "InfoMax watershed", 387,1825),
                   #("10", "InfoMax horizon", 1.1),
                   ("100", "P.M. raw", 59.7),
                   ("100", "P.M. watershed", 57.3),
                   #("100", "P.M. horizon", 7.1),
                   ("100", "InfoMax raw", 463,2447),
                   ("100", "InfoMax watershed", 387,1825),
                   #("100", "InfoMax horizon", 1.1),
                   ("1000", "P.M. raw", 627),
                   ("1000", "P.M. watershed", 573),
                   #("1000", "P.M. horizon", 63.5),
                   ("1000", "InfoMax raw", 463,2447),
                   ("1000", "InfoMax watershed", 387,1825),
                   #("1000", "InfoMax horizon", 1.1),
                   ("10000", "P.M. raw", 6180),
                   ("10000", "P.M. watershed", 5700),
                   #("10000", "P.M. horizon", 794),
                   ("10000", "InfoMax raw", 463,2447),
                   ("10000", "InfoMax watershed", 387,1825)]
                   #("10000", "InfoMax horizon", 1.1)]

fig, axis = plt.subplots(figsize=(plot_utils.column_width, 2.0),
                         frameon=False)
axis.set_xlabel("Number of stored snapshots")
axis.set_ylabel("Time [ms]")
axis.set_yscale("log", nonposy="clip")

plot_utils.plot_grouped_bars(jetson_test_data, 4, fig, axis, legend_pad=0.25)

if not plot_utils.presentation:
    fig.savefig("../figures/jetson_test_performance.eps")
plt.show()
