import matplotlib.pyplot as plt
import numpy as np

class ThinLens:
    def __init__(self, focal_length, position):
        self.focal_length = focal_length
        self.position = position

    def refract_ray(self, ray_origin, ray_angle):
        # Рассчитываем пересечение луча с плоскостью линзы
        x0, y0 = ray_origin
        ang = ray_angle
        x_l = self.position
        y_l = y0 + (x_l - x0) * np.tan(ang)
        x_f = x_l + self.focal_length
        y_f = self.focal_length * np.tan(ang)
        
        new_angle = np.arctan2((y_f - y_l), (x_f - x_l))

        return (x_l, y_l), new_angle

def draw_lens(ax, lens):
    ax.axvline(lens.position, color='blue', linestyle='--', label='Lens')

def find_intersection(rays):
    """
    Находит усредненную точку пересечения всех лучей.
    Если лучи параллельны, возвращает None.
    """
    intersections = []

    # Перебираем все пары лучей
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            (x1, y1), angle1 = rays[i]
            (x2, y2), angle2 = rays[j]

            # Коэффициенты наклона прямых
            k1 = np.tan(angle1)
            k2 = np.tan(angle2)

            # Проверяем, параллельны ли прямые
            if np.isclose(k1, k2):
                continue

            # Решаем систему уравнений для нахождения точки пересечения
            x_intersect = (y2 - y1 + k1 * x1 - k2 * x2) / (k1 - k2)
            y_intersect = y1 + k1 * (x_intersect - x1)

            intersections.append((x_intersect, y_intersect))

    # Если пересечений нет, возвращаем None
    if not intersections:
        return None

    # Усредняем все точки пересечения
    x_avg = np.mean([point[0] for point in intersections])
    y_avg = np.mean([point[1] for point in intersections])

    return x_avg, y_avg

def draw_ray_with_intersection(ax, ray_origin, ray_angle, lens_system):
    x, y = ray_origin
    rays = []  # Список для хранения конечных точек лучей и их углов

    for lens in lens_system:
        # Преломление луча через линзу
        (x_new, y_new), ray_angle = lens.refract_ray((x, y), ray_angle)
        ax.plot([x, x_new], [y, y_new], color='orange')
        x, y = x_new, y_new

    # Сохраняем конечную точку и угол луча
    rays.append(((x, y), ray_angle))

    # Продление луча после последней линзы
    x_final = x + 10  # Длина продления
    y_final = y + (x_final - x) * np.tan(ray_angle)
    ax.plot([x, x_final], [y, y_final], color='orange', linestyle='--')

    return rays

def simulate():
    # Создаем систему линз
    lens1 = ThinLens(focal_length=5, position=10)
    lens2 = ThinLens(focal_length=-5, position=12)  # Рассеивающая линза
    lens_system = [lens1, lens2]

    # Сортируем линзы по их позиции
    lens_system = sorted(lens_system, key=lambda lens: lens.position)

    # Настраиваем график
    fig, ax = plt.subplots()

    # Определяем начальные границы графика
    x_min = 0
    x_max = max(lens.position for lens in lens_system) + 5  # Немного отступа справа
    y_min = -10
    y_max = 10

    # Рисуем линзы
    for lens in lens_system:
        draw_lens(ax, lens)

    # Рисуем объект
    object_position = (0, 5)
    ax.plot([object_position[0]], [object_position[1]], 'ro', label='Object')  # Красный цвет для объекта

    # Обновляем границы графика с учетом объекта
    x_min = min(x_min, object_position[0] - 5)
    y_min = min(y_min, object_position[1] - 5)
    y_max = max(y_max, object_position[1] + 5)

    # Рисуем лучи и собираем их конечные точки
    ray_angles = [np.radians(-10), np.radians(0), np.radians(10)]  # Углы лучей
    rays = []
    for angle in ray_angles:
        rays.extend(draw_ray_with_intersection(ax, object_position, angle, lens_system))

    # Рассчитываем усредненную точку пересечения лучей
    intersection = find_intersection(rays)
    if intersection:
        x_intersect, y_intersect = intersection

        # Продлеваем все лучи до точки пересечения
        for (x, y), angle in rays:
            x_final = x_intersect
            y_final = y + (x_final - x) * np.tan(angle)
            ax.plot([x, x_final], [y, y_final], color='orange', linestyle='--')

        # Отмечаем точку пересечения
        ax.plot(x_intersect, y_intersect, 'go', label='Image')  # Зеленый цвет для изображения

        # Обновляем границы графика с учетом изображения
        x_max = max(x_max, x_intersect + 5)
        y_min = min(y_min, y_intersect - 5)
        y_max = max(y_max, y_intersect + 5)

    # Устанавливаем границы графика
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.axhline(0, color='black', linewidth=0.5)

    ax.legend()
    plt.show()

if __name__ == "__main__":
    simulate()