import matplotlib.pyplot as plt
import matplotlib.collections as mc

import retino
from retino.utils import *

import seaborn as sns

sns.set_style("ticks")


def convert_activity_to_rgb(activity):
    return plt.get_cmap("plasma")(0.99) if activity >= 0.8 else plt.get_cmap("plasma")(activity + 0.1)


def plot_post_synapses(output_file, post_synapses):
    fig, ax = plt.subplots(1, figsize=(8, 6), facecolor="#D6D6D6")
    ax.set_axis_bgcolor("#242424")
    colors = [convert_post_synapse_activity_to_rgb(x.activity) for x in post_synapses]
    sizes = [x.size * 50 for x in post_synapses]
    ax.scatter([x.origin[0] for x in post_synapses], [x.origin[1] for x in post_synapses],
               color=colors, s=sizes, alpha=0.3)
    plt.savefig(output_file)
    plt.close(fig)


def add_postsynapticcells_to_axis(post_synapses, ax, color="activity", alpha=0.3, size_scale=100):
    sizes = [x.size * size_scale for x in post_synapses]
    if color is "activity":
        colors = [convert_activity_to_rgb(x.activity) for x in post_synapses]
    else:
        colors = [color] * len(post_synapses)
    ax.scatter([x.origin[0] for x in post_synapses], [x.origin[1] for x in post_synapses],
               color=colors, s=sizes, alpha=alpha)


def add_postsynapticcell_to_axarr_by_mapping(postsynapticcell, axarr, xlim, ylim, size=20, alpha=.4):
    colors = convert_ndpoint_to_gradients(postsynapticcell.get_average_mapping(), [xlim, ylim])
    for i in range(len(axarr)):
        axarr[i].scatter(postsynapticcell.origin[0], postsynapticcell.origin[1],
                         color=colors[i], s=size, alpha=alpha)


def add_axon_to_axis(axon, ax, axon_color="activity", target_color="red", target_size=10, axon_alpha=0.6,
                     target_alpha=0.8):
    if axon_color is "activity":
        colors = [convert_activity_to_rgb(axon.activity)] * (len(axon.segments))
    elif axon_color is "origin":
        raise RuntimeError
    else:
        colors = [axon_color] * len(axon.segments)
    line_collection = mc.LineCollection(segments_to_lines(axon.segments), colors=list(colors), linewidths=1,
                                        alpha=axon_alpha)
    ax.add_collection(line_collection)
    ax.scatter(axon.target[0], axon.target[1], s=target_size, color=target_color, alpha=target_alpha)


def convert_ndpoint_to_gradients(point, bounds):
    return [plt.get_cmap("rainbow")(point[i] / bounds[i]) for i in range(len(point))]


def convert_linepoint_to_gradient_color(position, colormap_name, bound):
    return plt.get_cmap(colormap_name)(position / bound)


def plot_axon(axon, filename, xlim, ylim, dpi=100):
    fig, ax = plt.subplots(1, figsize=(8, 6))
    activities = [segment.activity for segment in axon.segments]
    colors = [convert_activity_to_rgb(activity) for activity in activities]
    lines = [[tuple(segment.origin), tuple(segment.end)] for segment in axon.segments]
    line_collection = mc.LineCollection(lines, colors=list(colors), linewidths=2, alpha=.8)
    ax.add_collection(line_collection)
    ax.scatter(axon.target[0], axon.target[1], s=20, c="r")
    ax.set_xlim([0, xlim])
    ax.set_ylim([0, ylim])
    ax.set_aspect(xlim / ylim)
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi, pad_inches=0)
    plt.close(fig)


def add_synapses_to_axarr_by_axon(axon, axarr, xlim, ylim, size=5, alpha=.4):
    points = [synapse.origin for synapse in axon.synapses]
    colors = convert_ndpoint_to_gradients(axon.target, [xlim, ylim])
    for i in range(len(axarr)):
        axarr[i].scatter([p[0] for p in points], [p[1] for p in points],
                         color=colors[i], s=size, alpha=alpha)


def plot_activity_array(activities_df, ax, size=10, alpha=1):
    points = np.mgrid[0:100, 0:100].reshape(2, -1).T
    activities = [activities_df.ix[p[0], p[1]] for p in points]
    colors = list(map(convert_activity_to_rgb, activities))
    ax.scatter([p[0] for p in points], [p[1] for p in points],
               color=colors, s=size, alpha=alpha)


def add_average_post_synapse_to_axarr_by_axon(axon, axarr, time, xlim, ylim):
    history = axon.history[time]
    points = history[3]
    p = get_average_of_points(points)
    colors = convert_ndpoint_to_gradients(axon.target, [xlim, ylim])
    for i in range(len(axarr)):
        axarr[i].scatter(p[0], p[1],
                         color=colors[i], s=5, alpha=.4)


def plot_model_summary(model, output):
    fig, [[activity_ax, axonal_growth_ax], [synapse_ax_x, synapse_ax_y], [postsynatic_ax_x, postsynatic_ax_y]] \
        = plt.subplots(3, 2, figsize=(10, 15))
    add_postsynapticcells_to_axis(model.postsynapticcells, axonal_growth_ax, color="cornflowerblue", alpha=0.2)
    for axon in model.axons:
        add_axon_to_axis(axon, axonal_growth_ax)
        add_synapses_to_axarr_by_axon(axon, [synapse_ax_x, synapse_ax_y], 100, 100)
    plot_activity_array(model.activities_df, activity_ax)
    for postsynapticcell in model.postsynapticcells:
        add_postsynapticcell_to_axarr_by_mapping(postsynapticcell, [postsynatic_ax_x, postsynatic_ax_y], 100.0, 100.0)
    for ax in [activity_ax, axonal_growth_ax, synapse_ax_x, synapse_ax_y, postsynatic_ax_x, postsynatic_ax_y]:
        ax.set_aspect(1)
        ax.set_xlim([0, retino.TECTUM_SIZE_X])
        ax.set_ylim([0, retino.TECTUM_SIZE_Y])

    activity_ax.set_title("Input Activity")
    axonal_growth_ax.set_title("Axonal Growth")
    synapse_ax_x.set_title("Synapses by X")
    synapse_ax_y.set_title("Synapses by Y")
    postsynatic_ax_x.set_title("Post Synapse Mapping by X")
    postsynatic_ax_y.set_title("Post Synapse Mapping by Y")

    sns.despine(offset=5.0)
    plt.tight_layout()
    plt.savefig(output + "-overview.png", dpi=300)
    plt.close(fig)


def plot_model_activity_summary(model, output):
    fig, [axon_activity, postsynapticcell_activity] = plt.subplots(2, figsize=(5, 10))
    for axon in model.axons:
        add_axon_to_axis(axon, axon_activity)
    add_postsynapticcells_to_axis(model.postsynapticcells, postsynapticcell_activity)
    for ax in [axon_activity, postsynapticcell_activity]:
        ax.set_aspect(1)
        ax.set_xlim([0, retino.TECTUM_SIZE_X])
        ax.set_ylim([0, retino.TECTUM_SIZE_Y])
    axon_activity.set_title("Axonal Activity")
    postsynapticcell_activity.set_title("Post Synaptic Cell Activity")
    sns.despine(offset=5.0)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close(fig)


def plot_model_axons(model, output):
    fig, ax = plt.subplots(1, figsize=(5, 5))
    for axon in model.axons:
        add_axon_to_axis(axon, ax)
    ax.set_xlim([0, retino.TECTUM_SIZE_X])
    ax.set_ylim([0, retino.TECTUM_SIZE_Y])
    ax.set_aspect(1)
    sns.despine(offset=5.0)
    plt.tight_layout()
    plt.savefig(output + "synapses.png", dpi=300)
    plt.close(fig)
