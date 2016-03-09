import pickle

import retino
from retino.plot import *
from retino.utils import *

sns.set_style("ticks")


def plot_axon_growth_direction_algorithm(origin, end, target, ax):
    a_origin = origin
    a_end = end

    desired_direction_weight = 1.1
    momentum_direction_weight = 1

    desired_direction = get_unit_direction_vector(a_end, target)
    momentum_direction = get_unit_direction_vector(a_origin, a_end)

    desired_and_momentum = desired_direction_weight * desired_direction + momentum_direction_weight * momentum_direction
    desired_and_momentum = get_unit_vector(desired_and_momentum)

    prenoise_pol = cart_to_pol(desired_and_momentum)[1]
    results = []
    for i in range(100):
        r = np.random.normal(2.0, 1.0, size=1)[0]
        noise = np.random.normal(0, .4, size=1)[0]
        theta = prenoise_pol + noise
        cart_result = pol_to_cart(np.asarray([r, theta]))
        results.append(cart_result)

    desired_direction = (desired_direction * 2 + a_end)
    momentum_direction = (momentum_direction * 2 + a_end)
    desired_and_momentum = (desired_and_momentum * 2 + a_end)

    for i in range(25):
        ax.plot([a_end[0], results[i][0] + a_end[0]], [a_end[1], results[i][1] + a_end[1]], color="crimson", alpha=.2,
                linewidth=1.0)

    ax.plot([a_origin[0], a_end[0]], [a_origin[1], a_end[1]], color="gold", linewidth=2.0, label="Segment of Origin")
    ax.plot([a_end[0], desired_direction[0]], [a_end[1], desired_direction[1]], color="seagreen", linewidth=2.0,
            label="Desired Direction")
    ax.plot([a_end[0], momentum_direction[0]], [a_end[1], momentum_direction[1]], color="darkorange", linewidth=2.0,
            label="Momentum Direction")
    ax.plot([a_end[1], desired_and_momentum[0]], [a_end[1], desired_and_momentum[1]], color="dodgerblue", linewidth=3.0,
            label="Weighted Guide Direction")

    ax.set_aspect(1)
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])


fig, direction_determination = plt.subplots(1, figsize=(5, 5), dpi=300)

origin = np.asarray([-3.5, -3.5])
end = np.asarray([-1.0, -1.0])
target = np.asarray([-5.0, 5.0])
print("Plotting for growth direction fig")
plot_axon_growth_direction_algorithm(origin, end, target, direction_determination)
direction_determination.set_title("Growth Direction Determination")

sns.despine(offset=5)
plt.tight_layout()
plt.savefig("figs/growth-direction-determination.pdf")
plt.close(fig)

#############

print("Plotting axon growth demos")
with open("singleaxonmodel/20.pickle", "rb") as f:
    model = pickle.load(f)

fig, growth_t1 = plt.subplots(1, figsize=(5, 5), dpi=300)

add_axon_to_axis(model.axons[0], growth_t1, axon_color="seagreen")
growth_t1.set_aspect(1)
growth_t1.set_xlim([0, retino.TECTUM_SIZE_X])
growth_t1.set_ylim([0, retino.TECTUM_SIZE_Y])
growth_t1.set_title("Axon A1 at 20 Iterations")

sns.despine(offset=5)
plt.tight_layout()
plt.savefig("figs/axon-at-20-iterations.pdf")
plt.close(fig)

#############

with open("singleaxonmodel/70.pickle", "rb") as f:
    model = pickle.load(f)

fig, growth_t2 = plt.subplots(1, figsize=(5, 5), dpi=300)

add_axon_to_axis(model.axons[0], growth_t2, axon_color="seagreen")
growth_t2.set_aspect(1)
growth_t2.set_xlim([0, retino.TECTUM_SIZE_X])
growth_t2.set_ylim([0, retino.TECTUM_SIZE_Y])
growth_t2.set_title("A1 at 70 Iterations")

sns.despine(offset=5)
plt.tight_layout()
plt.savefig("figs/axon-at-70-iterations.pdf")
plt.close(fig)

#############

with open("singleaxonmodel/140.pickle", "rb") as f:
    model = pickle.load(f)

fig, growth_t3 = plt.subplots(1, figsize=(5, 5), dpi=300)

postsynapses = list(set([synapse.postsynapticcell() for synapse in model.axons[0].synapses]))
add_postsynapticcell_to_axis(postsynapses, growth_t3, color="cornflowerblue", alpha=0.1, size_scale=80)
add_axon_to_axis(model.axons[0], growth_t3, axon_color="seagreen")
growth_t3.set_aspect(1)
growth_t3.set_xlim([0, retino.TECTUM_SIZE_X])
growth_t3.set_ylim([0, retino.TECTUM_SIZE_Y])
growth_t3.set_title("A1 at 140 Iterations")

sns.despine(offset=5)
plt.tight_layout()
plt.savefig("figs/axon-at-140-iterations.pdf")
plt.close(fig)

#############

with open("multipleaxonmodel/25axons.pickle", "rb") as f:
    model = pickle.load(f)

fig, [synapse_color_x, synapse_color_y] = plt.subplots(1, 2, figsize=(10, 5), dpi=300)

for axon in model.axons:
    add_axon_to_axis(axon, synapse_color_x, axon_color="seagreen", axon_alpha=0.2, target_alpha=0)
    add_axon_to_axis(axon, synapse_color_y, axon_color="seagreen", axon_alpha=0.2, target_alpha=0)
    add_synapses_to_axarr_by_axon(axon, [synapse_color_x, synapse_color_y],
                                  retino.TECTUM_SIZE_X, retino.TECTUM_SIZE_Y)

synapse_color_x.set_aspect(1)
synapse_color_x.set_xlim([0, retino.TECTUM_SIZE_X])
synapse_color_x.set_ylim([0, retino.TECTUM_SIZE_Y])
synapse_color_x.set_title("Synapses Coloured by X Gradient")

synapse_color_y.set_aspect(1)
synapse_color_y.set_xlim([0, retino.TECTUM_SIZE_X])
synapse_color_y.set_ylim([0, retino.TECTUM_SIZE_Y])
synapse_color_y.set_title("Synapses Coloured by Y Gradient")

sns.despine(offset=5)
plt.tight_layout()

plt.savefig("figs/25axis-synapse-colouring.pdf")

#############

with open("multipleaxonmodel/625axons.pickle", "rb") as f:
    model = pickle.load(f)

fig, [other1, other2] = plt.subplots(1, 2, figsize=(10, 5), dpi=500)

for axon in model.axons:
    add_synapses_to_axarr_by_axon(axon, [other1, other2],
                                  retino.TECTUM_SIZE_X, retino.TECTUM_SIZE_Y, alpha=0.2)

other1.set_aspect(1)
other1.set_xlim([0, retino.TECTUM_SIZE_X])
other1.set_ylim([0, retino.TECTUM_SIZE_Y])
other1.set_title("Synapses Coloured by X Gradient")

other2.set_aspect(1)
other2.set_xlim([0, retino.TECTUM_SIZE_X])
other2.set_ylim([0, retino.TECTUM_SIZE_Y])
other2.set_title("Synapses Coloured by Y Gradient")

sns.despine(offset=5)
plt.tight_layout()
plt.savefig("figs/625-axon-axis-synapse-colouring.png", dpi=1000)

############

fig, [postsynatic_ax_x, postsynatic_ax_y] = plt.subplots(1, 2)

for postsynapticcell in model.postsynapticcells:
    add_postsynapticcell_to_axarr_by_mapping(postsynapticcell, [postsynatic_ax_x, postsynatic_ax_y], 100.0, 100.0)
for ax in [postsynatic_ax_x, postsynatic_ax_y]:
    ax.set_aspect(1)
    ax.set_xlim([0, retino.TECTUM_SIZE_X])
    ax.set_ylim([0, retino.TECTUM_SIZE_Y])

postsynatic_ax_x.set_title("Post Synapse Mapping by X")
postsynatic_ax_y.set_title("Post Synapse Mapping by Y")

sns.despine(offset=5)
plt.tight_layout()
plt.savefig("figs/625-axon-postsynaptic-mapping-colour.pdf")
