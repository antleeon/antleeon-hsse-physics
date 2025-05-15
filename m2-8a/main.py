import numpy as np
import matplotlib.pyplot as plt

# === Настройки симуляции ===
width, height = 50, 50         # Размер радиатора (в ячейках)
num_particles = 10000          # Количество тепловых частиц
max_steps = 1000               # Максимальное число шагов на частицу
start = (width // 2, height // 2)  # Центр (имитация процессора)

# Направления движения (вверх, вниз, влево, вправо)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Карта температуры (считаем количество посещений каждой ячейки)
temperature_map = np.zeros((width, height), dtype=int)
escape_counts = np.zeros(max_steps + 1, dtype=int)

# === Основной цикл симуляции ===
for _ in range(num_particles):
    x, y = start
    for step in range(max_steps):
        if 0 <= x < width and 0 <= y < height:
            temperature_map[x, y] += 1
        else:
            # Частица покинула радиатор
            escape_counts[step] += 1
            break
        dx, dy = directions[np.random.randint(4)]
        x += dx
        y += dy

# === Визуализация результатов ===

# Карта температуры (распределение тепла по радиатору)
plt.figure(figsize=(6, 5))
plt.title("Карта температур (частоты посещения)")
plt.imshow(temperature_map.T, cmap='hot', origin='lower')
plt.colorbar(label='Количество посещений')
plt.xlabel("X (ширина)")
plt.ylabel("Y (высота)")
plt.grid(False)
plt.show()

# График распределения по времени выхода тепловых частиц
steps = np.arange(max_steps + 1)
plt.figure(figsize=(6, 4))
plt.title("Распределение времени выхода тепловых частиц")
plt.plot(steps, escape_counts, color='blue')
plt.xlabel("Шаги до выхода")
plt.ylabel("Количество частиц")
plt.grid(True)
plt.show()
