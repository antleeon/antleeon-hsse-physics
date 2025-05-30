from signals import harmonic_signal, pulse_sequence, modulated_signal, wave_packet, broadband_signal
from filters import low_pass_filter, high_pass_filter, band_pass_filter
from utils import generate_time_grid
from visualization import plot_signals
import numpy as np

def simulate_response(signal_func, filter_func, T=1.0, N=1024, signal_kwargs=None, filter_kwargs=None):
  # Убедимся, что словари аргументов не равны None
  signal_kwargs = signal_kwargs or {}
  filter_kwargs = filter_kwargs or {}
  
  # Генерация временной сетки
  t, dt = generate_time_grid(T, N)
  
  # Генерация входного сигнала
  signal = signal_func(t, **signal_kwargs)
  
  # Преобразование Фурье
  spectrum = np.fft.fft(signal)
  freqs = np.fft.fftfreq(N, dt)
  
  # Применение фильтра
  filtered_spectrum = filter_func(freqs, spectrum, **filter_kwargs)
  
  # Обратное преобразование Фурье
  filtered_signal = np.fft.ifft(filtered_spectrum).real
  
  # Формирование описания
  description = (
    f"Параметры симуляции:\n"
    f"Период: {T} с, Количество точек: {N}\n"
    f"Сигнал: {signal_func.__name__}, Параметры: {signal_kwargs}\n"
    f"Фильтр: {filter_func.__name__}, Параметры: {filter_kwargs}"
  )
  
  # Визуализация
  plot_signals(t, signal, freqs, spectrum, filtered_signal, filtered_spectrum, description)

if __name__ == "__main__":
  # Параметры симуляции
  T = 1.0  # Период симуляции, секунды
  N = 1024  # Количество точек дискретизации (безразмерное)

  # Пример 1: ФНЧ и гармонический сигнал
  simulate_response(
    signal_func=harmonic_signal,
    filter_func=low_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'freq': 50  # Частота гармонического сигнала, Гц
    },
    filter_kwargs={
      'cutoff': 60,  # Частота среза ФНЧ, Гц
      'transition_width': 10  # Ширина переходной области, Гц
    }
  )

  # Пример 2: ФВЧ и последовательность импульсов
  simulate_response(
    signal_func=pulse_sequence,
    filter_func=high_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'freq': 50  # Частота импульсов, Гц
    },
    filter_kwargs={
      'cutoff': 40,  # Частота среза ФВЧ, Гц
      'transition_width': 10  # Ширина переходной области, Гц
    }
  )

  # Пример 3: Узкополосный фильтр и модулированный сигнал
  simulate_response(
    signal_func=modulated_signal,
    filter_func=band_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'carrier_freq': 50,  # Несущая частота, Гц
      'mod_freq': 5        # Частота модуляции, Гц
    },
    filter_kwargs={
      'low_cutoff': 40,  # Нижняя граница полосы, Гц
      'high_cutoff': 60,  # Верхняя граница полосы, Гц
      'transition_width': 10  # Ширина переходной области, Гц
    }
  )

  # Пример 4: ФНЧ и цуг (волновой пакет)
  simulate_response(
    signal_func=wave_packet,
    filter_func=low_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'center_freq': 70,  # Центральная частота, Гц
      'width': 50         # Ширина пакета, безразмерное
    },
    filter_kwargs={
      'cutoff': 60,  # Частота среза ФНЧ, Гц
      'transition_width': 15  # Ширина переходной области, Гц
    }
  )

  # Пример 5: ФВЧ и гармонический сигнал
  simulate_response(
    signal_func=harmonic_signal,
    filter_func=high_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'freq': 30  # Частота гармонического сигнала, Гц
    },
    filter_kwargs={
      'cutoff': 40,  # Частота среза ФВЧ, Гц
      'transition_width': 5  # Ширина переходной области, Гц
    }
  )

  # Частоты для широкополосного сигнала
  broadband_freqs = [10, 30, 50, 70, 90]

  # Пример 6: ФНЧ и широкополосный сигнал
  simulate_response(
    signal_func=broadband_signal,
    filter_func=low_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'freqs': broadband_freqs  # Частоты, входящие в сигнал
    },
    filter_kwargs={
      'cutoff': 40,  # Частота среза ФНЧ, Гц
      'transition_width': 10  # Ширина переходной области, Гц
    }
  )

  # Пример 7: ФВЧ и широкополосный сигнал
  simulate_response(
    signal_func=broadband_signal,
    filter_func=high_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'freqs': broadband_freqs  # Частоты, входящие в сигнал
    },
    filter_kwargs={
      'cutoff': 60,  # Частота среза ФВЧ, Гц
      'transition_width': 10  # Ширина переходной области, Гц
    }
  )

  # Пример 8: Узкополосный фильтр и широкополосный сигнал
  simulate_response(
    signal_func=broadband_signal,
    filter_func=band_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'freqs': broadband_freqs  # Частоты, входящие в сигнал
    },
    filter_kwargs={
      'low_cutoff': 40,  # Нижняя граница полосы, Гц
      'high_cutoff': 70,  # Верхняя граница полосы, Гц
      'transition_width': 10  # Ширина переходной области, Гц
    }
  )

  # Пример 9: Узкополосный фильтр, отсекающий несущую частоту, с двумя модулирующими частотами
  simulate_response(
    signal_func=modulated_signal,
    filter_func=band_pass_filter,
    T=T,
    N=N,
    signal_kwargs={
      'carrier_freq': 50,  # Несущая частота, Гц
      'mod_freq': [5, 10]  # Две модулирующие частоты, Гц
    },
    filter_kwargs={
      'low_cutoff': 5,  # Нижняя граница полосы, Гц
      'high_cutoff': 20,  # Верхняя граница полосы, Гц
      'transition_width': 5  # Ширина переходной области, Гц
    }
  )