import numpy as np

def harmonic_signal(t, freq):
  """
  Генерация гармонического сигнала.
  t: массив времени, секунды
  freq: частота сигнала, Гц
  """
  return np.sin(2 * np.pi * freq * t)

def pulse_sequence(t, freq, duty_cycle=0.5):
  """
  Генерация последовательности импульсов.
  t: массив времени, секунды
  freq: частота импульсов, Гц
  duty_cycle: скважность (доля времени, когда сигнал активен), безразмерное
  """
  return (np.sin(2 * np.pi * freq * t) > 0).astype(float) * duty_cycle

def modulated_signal(t, carrier_freq, mod_freq):
  """
  Генерация модулированного сигнала.
  t: массив времени, секунды
  carrier_freq: несущая частота, Гц
  mod_freq: частота модуляции, Гц
  """
  return np.sin(2 * np.pi * carrier_freq * t) * (1 + 0.5 * np.sin(2 * np.pi * mod_freq * t))

def wave_packet(t, center_freq, width):
  """
  Генерация цуга (волнового пакета).
  t: массив времени, секунды
  center_freq: центральная частота, Гц
  width: ширина пакета, безразмерное
  """
  return np.exp(-width * (t - t.mean())**2) * np.sin(2 * np.pi * center_freq * t)

def broadband_signal(t, freqs):
  """
  Генерация широкополосного сигнала.
  t: массив времени, секунды
  freqs: список частот, Гц
  """
  signal = np.zeros_like(t)
  for freq in freqs:
    signal += np.sin(2 * np.pi * freq * t)
  return signal