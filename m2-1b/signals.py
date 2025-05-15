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
  mod_freq: одна или несколько модулирующих частот, Гц (может быть числом или списком)
  """
  if isinstance(mod_freq, (list, tuple)):  # Если передан список частот
    modulation = sum(np.sin(2 * np.pi * f * t) for f in mod_freq)
  else:  # Если передано одно значение частоты
    modulation = np.sin(2 * np.pi * mod_freq * t)
  
  return np.sin(2 * np.pi * carrier_freq * t) * (1 + 0.5 * modulation)

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