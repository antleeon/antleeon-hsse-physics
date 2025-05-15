from thin_lens import ThinLens
from simulation import setup_simulation
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(lens_system, object_position, ray_angles):
  setup_simulation(lens_system, object_position, ray_angles)
  plt.show()

if __name__ == "__main__":
  lens_system_1 = [
    ThinLens(focal_length=5, position=10),
    ThinLens(focal_length=-5, position=12)
  ]
  object_position_1 = (0, 5)
  ray_angles_1 = [np.radians(-10), np.radians(0), np.radians(10)]
  run_simulation(lens_system_1, object_position_1, ray_angles_1)

  lens_system_2 = [
    ThinLens(focal_length=8, position=15),
    ThinLens(focal_length=4, position=20)
  ]
  object_position_2 = (0, 7)
  ray_angles_2 = [np.radians(-5), np.radians(0), np.radians(5)]
  run_simulation(lens_system_2, object_position_2, ray_angles_2)