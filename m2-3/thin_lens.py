import numpy as np

class ThinLens:
  def __init__(self, focal_length, position):
    self.focal_length = focal_length
    self.position = position

  def refract_ray(self, ray_origin, ray_angle):
    x0, y0 = ray_origin
    ang = ray_angle
    x_l = self.position
    y_l = y0 + (x_l - x0) * np.tan(ang)
    x_f = x_l + self.focal_length
    y_f = self.focal_length * np.tan(ang)
    new_angle = np.arctan2((y_f - y_l), (x_f - x_l))
    return (x_l, y_l), new_angle

def draw_lens(ax, lens):
  lens_color = 'blue' if lens.focal_length > 0 else 'purple'
  lens_type = 'Converging' if lens.focal_length > 0 else 'Diverging'

  ax.axvline(lens.position, color=lens_color, linestyle='--', label=f'{lens_type} Lens (f={lens.focal_length})')

  if lens.focal_length != 0:
    f1 = lens.position + lens.focal_length
    f2 = lens.position - lens.focal_length
    ax.axvline(f1, color='gray', linestyle=':')
    ax.axvline(f2, color='gray', linestyle=':')