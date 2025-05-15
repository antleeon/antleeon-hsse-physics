import numpy as np

def low_pass_filter(freqs, spectrum, cutoff, transition_width=10):
  """
  Фильтр низких частот (ФНЧ) с плавным спадом.
  freqs: массив частот, Гц
  spectrum: спектр сигнала
  cutoff: частота среза, Гц
  transition_width: ширина переходной области, Гц
  """
  filter_mask = 1 / (1 + np.exp((np.abs(freqs) - cutoff) / transition_width))
  return spectrum * filter_mask

def high_pass_filter(freqs, spectrum, cutoff, transition_width=10):
  """
  Фильтр высоких частот (ФВЧ) с плавным спадом.
  freqs: массив частот, Гц
  spectrum: спектр сигнала
  cutoff: частота среза, Гц
  transition_width: ширина переходной области, Гц
  """
  filter_mask = 1 / (1 + np.exp(-(np.abs(freqs) - cutoff) / transition_width))
  return spectrum * filter_mask

def band_pass_filter(freqs, spectrum, low_cutoff, high_cutoff, transition_width=10):
  """
  Узкополосный фильтр с плавным спадом.
  freqs: массив частот, Гц
  spectrum: спектр сигнала
  low_cutoff: нижняя граница полосы, Гц
  high_cutoff: верхняя граница полосы, Гц
  transition_width: ширина переходной области, Гц
  """
  low_pass = 1 / (1 + np.exp((np.abs(freqs) - high_cutoff) / transition_width))
  high_pass = 1 / (1 + np.exp(-(np.abs(freqs) - low_cutoff) / transition_width))
  filter_mask = low_pass * high_pass
  return spectrum * filter_mask