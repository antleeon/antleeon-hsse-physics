import numpy as np

def low_pass_filter(freqs, spectrum, cutoff):
  """
  Фильтр низких частот (ФНЧ).
  freqs: массив частот, Гц
  spectrum: спектр сигнала
  cutoff: частота среза, Гц
  """
  return spectrum * (np.abs(freqs) <= cutoff)

def high_pass_filter(freqs, spectrum, cutoff):
  """
  Фильтр высоких частот (ФВЧ).
  freqs: массив частот, Гц
  spectrum: спектр сигнала
  cutoff: частота среза, Гц
  """
  return spectrum * (np.abs(freqs) > cutoff)

def band_pass_filter(freqs, spectrum, low_cutoff, high_cutoff):
  """
  Узкополосный фильтр.
  freqs: массив частот, Гц
  spectrum: спектр сигнала
  low_cutoff: нижняя граница полосы, Гц
  high_cutoff: верхняя граница полосы, Гц
  """
  return spectrum * ((np.abs(freqs) >= low_cutoff) & (np.abs(freqs) <= high_cutoff))