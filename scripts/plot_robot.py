import numpy as np
import matplotlib.pyplot as plt
from rdp import rdp
from scipy.interpolate import interp1d
from scipy.spatial import KDTree
import plot_utils

def load_training(filename):
    return np.loadtxt(filename, skiprows=1, delimiter=",",
                      dtype={"names": ("t", "filename"),
                             "formats": (np.float, "|S64")})

def load_perfect_memory_testing(filename):
    return np.loadtxt(filename, skiprows=1, delimiter=",",
                      converters={1: lambda s: float(s[:-4])},
                      dtype={"names": ("t", "best_heading", "lowest_diff", "best_snapshot", "filename"),
                             "formats": (np.float, np.float, np.float, np.int, "|S64")})

def load_infomax_testing(filename):
    return np.loadtxt(filename, skiprows=1, delimiter=",",
                      converters={1: lambda s: float(s[:-4])},
                      dtype={"names": ("t", "best_heading", "lowest_diff", "filename"),
                             "formats": (np.float, np.float, np.float, "|S64")})

def load_tracking(filename):
    data = np.loadtxt(filename, delimiter=",",
                      dtype={"names": ("t", "x", "y"),
                             "formats": (np.float, np.float, np.float)})
    # Convert time stamps to seconds
    data["t"] /= 1000.0
    return data

def get_snapshot_positions(tracking, snapshots):
    interpolator = interp1d(tracking["t"], np.vstack((tracking["x"], tracking["y"])), copy=False, fill_value="extrapolate")

    positions = interpolator(snapshots["t"])
    return positions

def plot_error_lines(axis, testing_snapshots, training_positions, testing_positions):
    for i, s in enumerate(testing_snapshots["best_snapshot"]):
        axis.arrow(testing_positions[0, i], testing_positions[1, i],
                   training_positions[0, s] - testing_positions[0, i], training_positions[1, s] - testing_positions[1, i],
                   color="gray", linewidth=0.1, head_width=10.0, length_includes_head=True)

def calc_distance_apart(training_tree, testing):
    testing_points = np.transpose(np.vstack((testing["x"], testing["y"])))

    return(training_tree.query(testing_points)[0])

# Read CSV routes
training = load_tracking("tracking_data/training_path_scaled.csv")
testing_raw = load_tracking("tracking_data/testing_path_raw_scaled.csv")
testing_binary = load_tracking("tracking_data/testing_path_binary_scaled.csv")
testing_infomax = load_tracking("tracking_data/testing_path_infomax_take2_scaled.csv")
testing_infomax_binary = load_tracking("tracking_data/testing_path_infomax_binary_scaled.csv")

largest_miny = max(np.amin(training["y"]),
                   np.amin(testing_raw["y"]),
                   np.amin(testing_binary["y"]),
                   np.amin(testing_infomax["y"]),
                   np.amin(testing_infomax_binary["y"]))
smallest_maxy = min(np.amax(training["y"]),
                    np.amax(testing_raw["y"]),
                    np.amax(testing_binary["y"]),
                    np.amax(testing_infomax["y"]),
                    np.amax(testing_infomax_binary["y"]))

training = training[(training["y"] >= largest_miny) & (training["y"] <= smallest_maxy)]
testing_raw = testing_raw[(testing_raw["y"] >= largest_miny) & (testing_raw["y"] <= smallest_maxy)]
testing_binary = testing_binary[(testing_binary["y"] >= largest_miny) & (testing_binary["y"] <= smallest_maxy)]
testing_infomax = testing_infomax[(testing_infomax["y"] >= largest_miny) & (testing_infomax["y"] <= smallest_maxy)]
testing_infomax_binary = testing_infomax_binary[(testing_infomax_binary["y"] >= largest_miny) & (testing_infomax_binary["y"] <= smallest_maxy)]

fig, axis = plt.subplots(figsize=(plot_utils.column_width, 2.25),frameon=False)

axis.set_xlim((0, 650))
axis.set_ylim((0, 240))
axis.set_xlabel("X [cm]")
axis.set_ylabel("Y [cm]")
axis.set_aspect("equal", "box")
plot_utils.remove_axis_junk(axis)

actors = [axis.plot(training["y"], training["x"])[0],
          axis.plot(testing_raw["y"], testing_raw["x"])[0],
          axis.plot(testing_binary["y"], testing_binary["x"])[0],
          axis.plot(testing_infomax["y"], testing_infomax["x"])[0],
          axis.plot(testing_infomax_binary["y"], testing_infomax_binary["x"])[0]]
labels = ["Training", "P.M. raw", "P.M. binary",# "P.M. horizon",
          "Infomax", "Infomax binary"]

fig.legend(actors, labels, loc="lower center", ncol=2, frameon=False)
fig.tight_layout(pad=0, rect=[0.0, 0.5, 1.0, 1.0])

if not plot_utils.presentation:
    fig.savefig("../figures/robot_paths.eps")
'''
training_tree = KDTree(np.transpose(np.vstack((training["x"], training["y"]))))
distances = [calc_distance_apart(training_tree, testing_raw),
             calc_distance_apart(training_tree, testing_binary),
             calc_distance_apart(training_tree, testing_infomax),
             calc_distance_apart(training_tree, testing_infomax_binary)]

print("Error mean:%f, sd:%f" % (np.average(np.hstack(distances)), np.std(np.hstack(distances))))
error_fig, error_axis = plt.subplots(figsize=(plot_utils.column_width, 4.0),frameon=False)
error_axis.boxplot(distances)
error_axis.set_xticklabels(labels[1:], rotation=90, horizontalalignment="right")
error_axis.set_ylabel("Distance to training route [cm]")

error_fig.tight_layout(pad=0, rect=(0, 0.025, 1, 1))

if not plot_utils.presentation:
    error_fig.savefig("../figures/robot_error.eps")

#plot_error_lines(axis, testing_raw_snapshots, training_snapshot_positions, testing_raw_snapshot_positions)
#plot_error_lines(axis, testing_horizon_vectors_snapshots, training_snapshot_positions, testing_horizon_snapshot_positions)
'''



plt.show()
