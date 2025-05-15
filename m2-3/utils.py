import numpy as np

def find_intersection(rays):
  intersections = []
  for i in range(len(rays)):
    for j in range(i + 1, len(rays)):
      (x1, y1), angle1 = rays[i]
      (x2, y2), angle2 = rays[j]
      k1 = np.tan(angle1)
      k2 = np.tan(angle2)
      if np.isclose(k1, k2):
        continue
      x_intersect = (y2 - y1 + k1 * x1 - k2 * x2) / (k1 - k2)
      y_intersect = y1 + k1 * (x_intersect - x1)
      intersections.append((x_intersect, y_intersect))
  if not intersections:
    return None
  x_avg = np.mean([point[0] for point in intersections])
  y_avg = np.mean([point[1] for point in intersections])
  return x_avg, y_avg