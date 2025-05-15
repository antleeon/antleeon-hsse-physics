import matplotlib.pyplot as plt
import numpy as np

def plot_signals(t, signal, freqs, spectrum, filtered_signal, filtered_spectrum, description):
  """
  Визуализация сигналов и их спектров.
  t: массив времени, секунды
  signal: входной сигнал
  freqs: массив частот, Гц
  spectrum: спектр входного сигнала
  filtered_signal: отфильтрованный сигнал
  filtered_spectrum: спектр отфильтрованного сигнала
  description: строка с описанием параметров схемы и фильтров
  """
  plt.figure(figsize=(12, 8))
  
  # Входной сигнал
  plt.subplot(2, 2, 1)
  plt.plot(t, signal)
  plt.title("Входной сигнал")
  plt.xlabel("Время (с)")
  plt.ylabel("Амплитуда (В)")
  
  # Спектр входного сигнала
  plt.subplot(2, 2, 2)
  plt.plot(freqs, np.abs(spectrum))
  plt.title("Спектр входного сигнала")
  plt.xlabel("Частота (Гц)")
  plt.ylabel("Амплитуда (В)")
  
  # Отфильтрованный сигнал
  plt.subplot(2, 2, 3)
  plt.plot(t, filtered_signal)
  plt.title("Отфильтрованный сигнал")
  plt.xlabel("Время (с)")
  plt.ylabel("Амплитуда (В)")
  
  # Спектр отфильтрованного сигнала
  plt.subplot(2, 2, 4)
  plt.plot(freqs, np.abs(filtered_spectrum))
  plt.title("Спектр отфильтрованного сигнала")
  plt.xlabel("Частота (Гц)")
  plt.ylabel("Амплитуда (В)")
  
  # Добавление текстового описания
  plt.gcf().text(0.5, 0.01, description, ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
  
  # Увеличиваем нижний отступ
  plt.tight_layout(rect=[0, 0.1, 1, 1])  # Увеличиваем нижний отступ до 0.1
  plt.show()