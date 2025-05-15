import matplotlib.pyplot as plt
import numpy as np
from thin_lens import draw_lens
from utils import find_intersection

def draw_ray_with_intersection(ax, ray_origin, ray_angle, lens_system):
  x, y = ray_origin
  rays = []
  for lens in lens_system:
    (x_new, y_new), ray_angle = lens.refract_ray((x, y), ray_angle)
    ax.plot([x, x_new], [y, y_new], color='orange')
    x, y = x_new, y_new
  x_final = x + 10
  y_final = y + (x_final - x) * np.tan(ray_angle)
  ax.plot([x, x_final], [y, y_final], color='orange', linestyle='--')
  rays.append(((x, y), ray_angle))
  return rays

def setup_simulation(lens_system, object_position, ray_angles):
  fig, ax = plt.subplots()
  x_min, x_max = 0, max(lens.position for lens in lens_system) + 5
  y_min, y_max = -10, 10

  for lens in lens_system:
    draw_lens(ax, lens)

  ax.plot([object_position[0]], [object_position[1]], 'ro', label='Object')

  x_min = min(x_min, object_position[0] - 5)
  y_min = min(y_min, object_position[1] - 5)
  y_max = max(y_max, object_position[1] + 5)

  rays = []
  for angle in ray_angles:
    rays.extend(draw_ray_with_intersection(ax, object_position, angle, lens_system))

  intersection = find_intersection(rays)
  if intersection:
    x_intersect, y_intersect = intersection
    for (x, y), angle in rays:
      x_final = x_intersect
      y_final = y + (x_final - x) * np.tan(angle)
      ax.plot([x, x_final], [y, y_final], color='orange', linestyle='--')
    ax.plot(x_intersect, y_intersect, 'go', label='Image')

    x_max = max(x_max, x_intersect + 5)
    y_min = min(y_min, y_intersect - 5)
    y_max = max(y_max, y_intersect + 5)

  ax.set_xlim(x_min, x_max)
  ax.set_ylim(y_min, y_max)
  ax.axhline(0, color='black', linewidth=0.5)
  ax.legend()
  return fig, ax