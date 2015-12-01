import numpy as np
import random
import retino
from PIL import Image

def cart_to_pol(nparr):
  r = np.sqrt(nparr[0]**2 + nparr[1]**2)
  theta = np.arctan2(nparr[1], nparr[0])
  return np.asarray([r, theta])

def pol_to_cart(nparr):
  x = nparr[0] * np.cos(nparr[1])
  y = nparr[0] * np.sin(nparr[1])
  return np.asarray([x,y])

def segments_to_lines(segments):
  return [[tuple(segment.origin), tuple(segment.end)] for segment in segments]  

# def generate_weighted_direction(weights, directions):
#   thetas = [cart_to_pol(direction)[1] for direction in directions]
#   thetas_weighted = np.multiply(weights, thetas)
#   theta_average = np.average(thetas)
#   return cart_to_pol(np.asarray([1, theta_average]))

def generate_random_points_along_line(origin, direction, pool_size, points_count, jitter=0.4):
  pool = generate_points_along_line(origin, direction, pool_size)
  jittered_pool = add_jitter_to_points(pool, jitter)
  origins = choose_points_subset(jittered_pool, points_count)
  return origins

def get_unit_direction_vector(a, b):
  desired_direction = b - a
  desired_direction  = desired_direction/(np.linalg.norm(desired_direction))
  return desired_direction

def get_unit_vector(v):
  return v/(np.linalg.norm(v))

def generate_points_along_line(origin, vector_direction, points_count):
  points_on_vector = [np.asarray([i * vector_direction[0]/points_count, vector_direction[1]]) for i in range(points_count)]
  points_on_line = [pol_to_cart(p) for p in points_on_vector]
  points_on_line = [point + origin for point in points_on_line]
  return points_on_line

def add_jitter_to_points(points, jitter_amount):
  points = [point + np.asarray([np.random.normal(0, jitter_amount), np.random.normal(0, jitter_amount)]) for point in points]
  return points

def choose_points_subset(points, count):
  return random.sample(points, count)

def is_point_within_circle(p, circle_origin, circle_size):
  return np.linalg.norm(circle_origin - p) < circle_size

def choose_random_circle_as_connection_index(point, circle_origins, circle_sizes):
  circles = zip(circle_origins, circle_sizes)
  circle_indices_overlapping_point = []
  for i in range(len(circle_origins)):
    if np.linalg.norm(circle_origins[i] - point) < circle_sizes[i]:
      circle_indices_overlapping_point.append(i)
  if len(circle_indices_overlapping_point) > 0:
    return random.sample(circle_indices_overlapping_point, 1)[0]
  else:
    return None

def produce_bounded_random_point(xlim, ylim):
  return np.array([np.random.uniform(0, xlim, size=1)[0], np.random.uniform(0, ylim, size=1)[0]])

def select_item_from_list_by_beta_distribution(length, a, b):
  position = np.random.beta(a, b, size=1)
  index = np.int32(np.ceil(position * length)[0]) - 1
  return index

def get_average_point_error(target, points):
  if(len(points) > 10):
    return np.average([np.linalg.norm(target-p) for p in points])
  else:
    return retino.TECTUM_WIDTH

def image_to_activity_points(image_str, resolution=100):
  im = Image.open(image_str)
  activities = []
  for y in range(resolution):
    for x in range(resolution):
      activities.append(1.0 - np.average(np.asarray(im.getpixel((x,99-y))))/255.0)
  origins = list(zip(list(range(resolution))*resolution, np.asarray([[i]*resolution for i in range(resolution)]).flatten()))
  return [origins, activities]

def fire_by_activity_points(target, activity_origins):
  distance = 99999999
  best_match_activity = -1
  for activity in activity_origins:
    curr_distance = np.linalg.norm(activity[0] - target) 
    if(curr_distance < distance):
      best_match_activity = activity[1]
      distance = curr_distance
  return best_match_activity

def generate_tex_friendly_filename(filename):
  filename = filename.replace(".",",")
  filename = filename.replace(" ","-")
  return filename

def choose_to_branch(a=6, b=1):
  if np.random.normal(a,b,size=1)[0] > 0.95:
    return True
  else:
    return False
