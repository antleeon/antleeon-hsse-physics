import numpy as np

def generate_time_grid(T, N):
  """
  Генерация временной сетки.
  T: период симуляции, секунды
  N: количество точек дискретизации, безразмерное
  Возвращает:
  t: массив времени, секунды
  dt: шаг дискретизации, секунды
  """
  dt = T / N
  t = np.linspace(0, T, N, endpoint=False)
  return t, dt