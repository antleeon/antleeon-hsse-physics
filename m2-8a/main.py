import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === Параметры симуляции ===
width, height = 50, 50
num_particles = 5000
max_steps = 1000
start = (width // 2, height // 2)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# === Инициализация ===
temperature_map = np.zeros((width, height), dtype=int)         # Накопленная температура
escape_counts = np.zeros(max_steps + 1, dtype=int)             # Сколько частиц вышло на каждом шаге
particle_positions = [[start] for _ in range(num_particles)]   # Пути частиц
current_density_map = np.zeros((width, height), dtype=int)     # Частицы в ячейках сейчас
step_count_per_particle = np.full(num_particles, -1, dtype=int)   # Шаг выхода для каждой частицы
time_in_radiator = np.zeros(num_particles, dtype=int)          # Время каждой частицы в радиаторе
temperature_distribution = []  # Список для сохранения температурных карт

# Новый список для хранения среднего количества шагов до выхода на каждом шаге
avg_steps_to_exit_over_time = []

# === Подготовка графиков ===
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Карта температур
im1 = ax1.imshow(temperature_map.T, cmap='hot', origin='lower', vmin=0, vmax=10)
ax1.set_title("Карта температур (накопленная)")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")

# Карта текущей плотности
im2 = ax2.imshow(current_density_map.T, cmap='plasma', origin='lower', vmin=0, vmax=20)
ax2.set_title("Текущая плотность тепловых частиц")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")

# Добавляем текст для отображения суммарного тепла на втором графике
heat_text_ax2 = ax2.text(0.02, 0.95, '', transform=ax2.transAxes, color='white', fontsize=12, 
                         bbox=dict(facecolor='black', alpha=0.5))

plt.tight_layout()

# === Обновление на каждом шаге ===
def update(step):
  global particle_positions, temperature_map, escape_counts, current_density_map
  current_density_map.fill(0)

  for i in range(len(particle_positions)):
    if step < len(particle_positions[i]):
      continue  # Частица уже вышла
    x, y = particle_positions[i][-1]

    # Частица вышла за пределы
    if not (0 <= x < width and 0 <= y < height):
      if step_count_per_particle[i] == -1:  # Только если это первое пересечение границы
        escape_counts[step] += 1
        step_count_per_particle[i] = step
        time_in_radiator[i] = len(particle_positions[i])
      particle_positions[i].append((-1, -1))  # Маркер выхода
      continue

    # Обновление температуры и плотности
    temperature_map[x, y] += 1
    current_density_map[x, y] += 1

    # Случайный шаг
    dx, dy = directions[np.random.randint(4)]
    new_x, new_y = x + dx, y + dy
    particle_positions[i].append((new_x, new_y))

  # Сохраняем копию температурной карты
  temperature_distribution.append(temperature_map.copy())

  # Обновляем массив со средними шагами до выхода
  valid_steps = step_count_per_particle[step_count_per_particle >= 0]
  if len(valid_steps) > 0:
    avg_steps_to_exit_over_time.append(np.mean(valid_steps))
  else:
    avg_steps_to_exit_over_time.append(0)

  # Обновляем графики
  im1.set_array(temperature_map.T)
  im2.set_array(current_density_map.T)

  # Обновляем текст с суммарным количеством тепла
  total_heat = np.sum(current_density_map)
  heat_text_ax2.set_text(f"Суммарное тепло: {total_heat}")

  return [im1, im2, heat_text_ax2]

# Анимация
ani = animation.FuncAnimation(fig, update, frames=max_steps, interval=50, repeat=False)
plt.show()

# === Постобработка ===
# Среднее количество шагов до выхода
final_valid_steps = step_count_per_particle[step_count_per_particle >= 0]
avg_steps_total = np.mean(final_valid_steps)

print(f"Среднее количество шагов до выхода: {int(avg_steps_total)}")

# Построение финальных графиков ===

# Карта температур
plt.figure(figsize=(6, 5))
plt.title("Карта температур (частоты посещений)")
plt.imshow(temperature_map.T, cmap='hot', origin='lower')
plt.colorbar(label='Количество посещений')
plt.xlabel("X (ширина)")
plt.ylabel("Y (высота)")
plt.grid(False)
plt.show()

# График времени выхода частиц и изменения среднего количества шагов до выхода
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# График времени выхода частиц
steps = np.arange(max_steps + 1)
ax1.set_title("Распределение времени выхода тепловых частиц")
ax1.plot(steps, escape_counts, color='blue')
ax1.set_xlabel("Шаг симуляции")
ax1.set_ylabel("Частиц вышло")
ax1.grid(True)

# График изменения среднего количества шагов до выхода
ax2.set_title("Изменение среднего количества шагов до выхода")
ax2.plot(avg_steps_to_exit_over_time, label="Среднее количество шагов до выхода", color='green')
ax2.set_xlabel("Шаг симуляции")
ax2.set_ylabel("Среднее количество шагов")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()