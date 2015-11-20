from retino import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
import time
import seaborn as sns
from PIL import Image
from multiprocessing import *

def plot_axon_growth_algorithm(origin, end, target):
  t = time.time()
  a_origin = origin
  a_end = end
  origin = np.array(a_end)  

  desired_direction_weight = 1.1
  momentum_direction_weight = 1

  desired_direction = get_unit_direction_vector(origin, target)
  momentum_direction = get_unit_direction_vector(a_origin, a_end)

  desired_and_momentum = desired_direction_weight * desired_direction + momentum_direction_weight * momentum_direction
  desired_and_momentum = get_unit_vector(desired_and_momentum)

  prenoise_pol = cart_to_pol(desired_and_momentum)[1]
  results = []
  for i in range(50):
    r = np.random.normal(3.0,1.0, size=1)[0]
    noise = np.random.normal(0,.5,size=1)[0]
    theta = prenoise_pol + noise
    cart_result = pol_to_cart(np.asarray([r,theta]))
    results.append(cart_result)  

  desired_direction = desired_direction * 3
  momentum_direction = momentum_direction * 3
  desired_and_momentum = desired_and_momentum * 3

  fig, ax = plt.subplots(figsize=(5,5))
  ax.plot([a_origin[0],a_end[0]], [a_origin[1],a_end[1]], color="y", linewidth=3.0, label="Segment of Origin")
  ax.plot([0,desired_direction[0]], [0,desired_direction[1]], color="g", linewidth=3.0, label="Desired Direction")
  ax.plot([0,momentum_direction[0]], [0,momentum_direction[1]], color="r", linewidth=3.0, label="Momentum Direction")
  ax.plot([0,desired_and_momentum[0]], [0,desired_and_momentum[1]], color="b", linewidth=3.0, label="Weighted Guide Direction")
  ax.set_aspect(1)
  ax.set_title("Choosing Guide Direction")
  legend = ax.legend(loc='best', shadow=True, fancybox=True)
  plt.tight_layout()
  plt.savefig("Plots/GrowthAlgorithmGuideDirection-Direction=" + str(desired_and_momentum) + ".pdf")
  plt.close(fig)
  
  fig, ax = plt.subplots(figsize=(5,5))
  ax.plot([a_origin[0],a_end[0]], [a_origin[1],a_end[1]], color="y", linewidth=3.0, label="Segment of Origin")
  ax.plot([0,desired_and_momentum[0]], [0,desired_and_momentum[1]], color="b", linewidth=3.0, label="Weighted Guide Direction")
  for i in range(50):
    ax.plot([0, results[i][0]], [0, results[i][1]], color="r", alpha=.3, linewidth=1.0)
  ax.set_aspect(1)
  ax.set_title("A Family of Possible Axon Growths")
  plt.tight_layout()
  plt.savefig("Plots/GrowthAlgorithmNewSegmentFamily-Direction=" + str(desired_and_momentum) + ".pdf")
  plt.close(fig)
  print("Finished GrowthAlgorithmGuideDirection-Direction=" + str(desired_and_momentum) + " in " + str(time.time() - t))

def plot_demo_for_synapse_growth(origin, end, pool_size, jitter, points_count):
  t = time.time()
  direction = cart_to_pol(end - origin)
  pool = generate_points_along_line(origin, direction, pool_size)
  jittered_pool = add_jitter_to_points(pool, jitter)
  origins = choose_points_subset(jittered_pool, points_count)
  fig, ax = plt.subplots(figsize=(5,5))
  ax.scatter([p[0] for p in pool], [p[1] for p in pool], label="1. Pool of Points Along Axon", color="y", s=4)
  ax.scatter([p[0] for p in jittered_pool], [p[1] for p in jittered_pool], label="2. Pool with 0.1 Jitter", color="r", s=10)
  ax.scatter([p[0] for p in origins], [p[1] for p in origins], label="3. Chosen Origins for Post Synaptic Attempts", color="b", s=20)  
  ax.set_title("PostSynaptic Connection Growth")

  legend = ax.legend(loc='upper left', shadow=True)
  ax.set_aspect('equal', 'datalim')
  plt.tight_layout()
  plt.savefig("Plots/SynapseGrowth-Pool=" + str(pool_size) + "-Jitter=" + str(jitter) + "-Points=" + str(points_count) + ".pdf")
  plt.close(fig)

  print("Finished SynapseGrowth-Pool=" + str(pool_size) + "-Jitter=" + str(jitter) + "-Points=" + str(points_count) + " in " + str(time.time() - t))


def produce_demo_for_synapses_to_postsynapses():
  origin = np.asarray([5.0,5.0])
  end = np.asarray([13.0, 14.0])
  direction = cart_to_pol(end - origin)
  origins = generate_random_points_along_line(origin, direction, 100, 20)

  number_of_circles = 250
  circle_origins = [produce_bounded_random_point(15.0,15.0) for i in range(number_of_circles)]
  circle_radiuses = [np.random.normal(1.5, 0.5, size=1)[0] for i in range(number_of_circles)]

  fig, ax = plt.subplots()
  ax.plot([origin[0], end[0]], [origin[1], end[1]], color="y", linewidth=1.0, label="Axon Segment")
  ax.scatter([p[0] for p in origins], [p[1] for p in origins], label="Chosen Origins for Post Synaptic Attempts", 
        color="b", s=15, zorder=5)  

  ax.add_collection(EllipseCollection(widths=[2*x for x in circle_radiuses], heights=[2*x for x in circle_radiuses], angles=0, units='xy',
             facecolors='r',
             offsets=circle_origins, transOffset=ax.transData, alpha=0.1, label="Pool of Postsynapses"))
  
  chosen_circle_origins = []
  chosen_circle_radiuses = []
  for origin in origins:
    i = choose_random_circle_as_connection_index(origin, circle_origins, circle_radiuses)
    chosen_circle_origins.append(circle_origins[i][:])
    chosen_circle_radiuses.append(circle_radiuses[i])

  ax.add_collection(EllipseCollection(widths=[x*2 for x in chosen_circle_radiuses], heights=[x*2 for x in chosen_circle_radiuses], angles=0, units='xy',
             facecolors='g',
             offsets=chosen_circle_origins, transOffset=ax.transData, alpha=0.2, label="Connected Postsynapses")) 

  ax.set_title("PostSynapse Choosing For Growth")
  ax.set_aspect('equal', 'datalim')
  legend = ax.legend(loc='upper left', shadow=True)
  plt.tight_layout()
  plt.savefig("Plots/SynapseChoosingForGrowth.pdf")
  plt.close(fig)
  print("Finished SynapseChoosingForGrowth in " + str(time.time() - t))


def plot_demo_for_colouring_circles_by_gradients():
  t = time.time()
  number_of_circles = 2500
  origins = [produce_bounded_random_point(100.0,100.0) for i in range(number_of_circles)]
  colors = [convert_ndpoint_to_gradients(p, [100.0,100.0]) for p in origins]
  
  for axis in ["X","Y"]:
    fig, ax = plt.subplots(1)
    if axis == "X":
      ax.scatter([p[0] for p in origins], [p[1] for p in origins], 
            color=[c[0] for c in colors], s=15, zorder=5)  
    if axis == "Y":
      ax.scatter([p[0] for p in origins], [p[1] for p in origins], 
            color=[c[1] for c in colors], s=15, zorder=5)  

    axarr[0].set_title("Colored Points by Gradient Along X")
    ax.set_xlim([0,100.0])
    ax.set_ylim([0,100.0])
    plt.tight_layout()
    plt.savefig("Plots/ColoredPointsByGradient-" + axis + ".pdf")
    plt.close(fig)  

  print("Finished ColoredPointsByGradient in " + str(time.time() - t))


def plot_demo_for_activity_black_white_signal(image_str):
  t = time.time()
  origins, colors = image_to_activity_points("../images/" + image_str)
  origins = add_jitter_to_points(origins, .5)
  fig, ax = plt.subplots(1)
  ax.scatter([p[0] for p in origins], [p[1] for p in origins], c=colors, s=5)
  ax.set_xlim([0,100.0])
  ax.set_ylim([0,100.0])
  ax.set_aspect('equal', 'datalim')
  plt.tight_layout()
  plt.savefig("Plots/GrayscalePointsByActivity-" + image_str[:-4] + ".png", dpi=300)
  print("Finished GrayscalePointsByActivity-" + image_str[:-4] + " in " + str(time.time() - t))


if __name__ == '__main__':

  origin = np.asarray([-2.5,-2.5])
  end = np.asarray([0.0,0.0])
  target = np.asarray([3.0,8.0])
  p1 = Process(target=plot_axon_growth_algorithm, args=(origin, end, target,))
  p1.start()
  print("Started P1")

  origin = np.asarray([-2.5,-2.5])
  end = np.asarray([0.0,0.0])
  target = np.asarray([-4.0,-3.0])
  p2 = Process(target=plot_axon_growth_algorithm, args=(origin, end, target,))
  p2.start()
  print("Started P2")

  origin = np.asarray([0.0,0.0])
  end = np.asarray([12.0, 12.0])
  p3 = Process(target=plot_demo_for_synapse_growth, args=(origin, end, 24, .2,8,))
  p3.start()
  print("Started P3")

  origin = np.asarray([0.0,0.0])
  end = np.asarray([12.0, 12.0])
  p4 = Process(target=plot_demo_for_synapse_growth, args=(origin, end, 82, .2,8,))
  p4.start()
  print("Started P4")

  p5 = Process(target=plot_demo_for_colouring_circles_by_gradients, args=())
  p5.start()
  print("Started P5")

  image_str = "chaplin.jpg"
  p6 = Process(target=plot_demo_for_activity_black_white_signal, args=(image_str,))
  p6.start()
  print("Started P6")
