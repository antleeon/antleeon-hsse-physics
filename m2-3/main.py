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

  # Пример 3: Лупа
  lens_system_loupe = [
    ThinLens(focal_length=10, position=15)  # Положительная линза
  ]
  object_position_loupe = (10, 2)  # Предмет перед линзой
  ray_angles_loupe = [np.radians(-5), np.radians(0), np.radians(5)]
  print("Симуляция: Лупа")
  run_simulation(lens_system_loupe, object_position_loupe, ray_angles_loupe)

  # Пример 4: Микроскоп
  lens_system_microscope = [
    ThinLens(focal_length=5, position=10),  # Объектив
    ThinLens(focal_length=5, position=31)  # Окуляр
  ]
  object_position_microscope = (3, 1)  # Маленький объект перед объективом
  ray_angles_microscope = [np.radians(-5), np.radians(0), np.radians(5)]
  print("Симуляция: Микроскоп")
  run_simulation(lens_system_microscope, object_position_microscope, ray_angles_microscope)

  # Пример 5: Телескоп
  lens_system_telescope = [
    ThinLens(focal_length=15, position=5),  # Объектив
    ThinLens(focal_length=5, position=25)  # Окуляр
  ]
  object_positions_telescope = [(0, -2), (0, 0), (0, 2)]  # Три объекта
  ray_angles_telescope = [0, 0, 0]  # Один прямой луч из каждого объекта
  print("Симуляция: Телескоп")
  
  # Рисуем все объекты и их лучи на одном графике
  fig, ax = plt.subplots()
  for object_position, ray_angle in zip(object_positions_telescope, ray_angles_telescope):
    setup_simulation(lens_system_telescope, object_position, [np.radians(ray_angle)], ax=ax)
  plt.show()