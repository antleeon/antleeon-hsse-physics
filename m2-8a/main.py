import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === Параметры симуляции ===
width, height = 50, 50
num_particles = 5000
max_steps = 500
start = (width // 2, height // 2)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# === Инициализация ===
temperature_map = np.zeros((width, height), dtype=int)         # Накопленная температура
escape_counts = np.zeros(max_steps + 1, dtype=int)             # Выход частиц
particle_positions = [[start] for _ in range(num_particles)]   # Пути частиц
current_density_map = np.zeros((width, height), dtype=int)     # Частицы в ячейках сейчас

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

plt.tight_layout()

# === Обновление на каждом шаге ===
def update(step):
    global particle_positions, temperature_map, escape_counts, current_density_map
    current_density_map.fill(0)  # Сброс перед каждым шагом

    for i in range(len(particle_positions)):
        if step < len(particle_positions[i]):
            continue  # Частица уже вышла
        x, y = particle_positions[i][-1]

        # Частица вышла за пределы
        if not (0 <= x < width and 0 <= y < height):
            escape_counts[step] += 1
            particle_positions[i].append((-1, -1))  # Маркер выхода
            continue

        # Учёт посещения и текущей плотности
        temperature_map[x, y] += 1
        current_density_map[x, y] += 1

        # Случайное движение
        dx, dy = directions[np.random.randint(4)]
        new_x, new_y = x + dx, y + dy
        particle_positions[i].append((new_x, new_y))

    im1.set_array(temperature_map.T)
    im2.set_array(current_density_map.T)
    return [im1, im2]

# Анимация
ani = animation.FuncAnimation(fig, update, frames=max_steps, interval=50, repeat=False)
plt.show()

# === Постобработка: построение финальных графиков ===

# Карта температур
plt.figure(figsize=(6, 5))
plt.title("Карта температур (частоты посещений)")
plt.imshow(temperature_map.T, cmap='hot', origin='lower')
plt.colorbar(label='Количество посещений')
plt.xlabel("X (ширина)")
plt.ylabel("Y (высота)")
plt.grid(False)
plt.show()

# График времени выхода частиц
steps = np.arange(max_steps + 1)
plt.figure(figsize=(6, 4))
plt.title("Распределение времени выхода тепловых частиц")
plt.plot(steps, escape_counts, color='blue')
plt.xlabel("Шаги до выхода")
plt.ylabel("Количество частиц")
plt.grid(True)
plt.show()
