import scipy
import constants as const
import some_math
import math
    
def height_func_linear_resistance(t):
    m = const.MASS
    g = const.GRAVITATIONAL_ACCELERATION[0]
    k = 6 * math.pi * const.ENVIRONMENT_VISCOSITY * const.RADIUS
    v_0_vertical = some_math.vector_to_standard(some_math.projection(const.SPEED, (1, 90)))
    if (0 <= v_0_vertical[1] <= 180):
        v_0_y = v_0_vertical[0]
    else:
        v_0_y = -v_0_vertical[0]
    e = math.e

    height = (m / k) * (((m * g / k) + v_0_y) * (1 - (e ** (-k * t / m))) - (g * t))
    
    return height

# def height_func_quadratic_resistance(t): TODO

height_funcs_dict = {'linear': height_func_linear_resistance}

def distance_func_linear_resistance(t):
    m = const.MASS
    k = 6 * math.pi * const.ENVIRONMENT_VISCOSITY * const.RADIUS
    v_0_horizontal = (some_math.projection(const.SPEED, (1, 0)))
    if (-90 <= v_0_horizontal[1] <= 90):
        v_0_x = v_0_horizontal[0]
    else:
        v_0_x = -v_0_horizontal[0]
    e = math.e

    distance = (m * v_0_x / k) * (1 - (e ** (-k * t / m)))
    
    return distance

# def distance_func_quadratic_resistance(t): TODO

distance_funcs_dict = {'linear': distance_func_linear_resistance}

def count(air_resistance_type):
    def binary_find_argument(predicate, accuracy, interval):
        left, right = interval

        if (predicate(left) == predicate(right)):
            return right
        is_right = predicate(right)

        while ((right - left) > accuracy):
            check = left + ((right - left) / 2)
            if (predicate(check) == is_right):
                right = check
            else:
                left = check

        return right
    
    TIME_ACCURACY = const.TIME_ACCURACY
    TIME_INTERVAL = const.TIME_INTERVAL
        
    HEIGHT = const.Y_F
    
    def get_height_predicate(height_f, height_needed):
        def predicate(time):
            return (height_f(time) <= height_needed)
        return predicate

    height_func = height_funcs_dict.get(air_resistance_type, height_func_linear_resistance)
    distance_func = distance_funcs_dict.get(air_resistance_type, distance_func_linear_resistance)

    time = binary_find_argument(get_height_predicate(height_func, HEIGHT), TIME_ACCURACY, TIME_INTERVAL)

    height = height_func(time)
    distance = distance_func(time)

    final_coordinates = ((const.X_0 + distance), height)

    return (time, final_coordinates)

def count_trace(air_resistance_type, time):
    TIME_POINTS_QUANTITY = const.TIME_POINTS_QUANTITY

    height_func = height_funcs_dict.get(air_resistance_type, height_func_linear_resistance)
    distance_func = distance_funcs_dict.get(air_resistance_type, distance_func_linear_resistance)

    x_0, y_0 = const.X_0, 0
    x, y = x_0, y_0
    min_x, min_y = x, y
    max_x, max_y = x, y

    coordinates = [(x, y)]

    for i in range(TIME_POINTS_QUANTITY):
        time_passed = time * (i + 1) / TIME_POINTS_QUANTITY
        height = height_func(time_passed)
        distance = distance_func(time_passed)
        x, y = x_0 + distance, y_0 + height
        coordinates.append((x, y))
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    boundaries = ((min_x, min_y), (max_x, max_y))
    
    return (coordinates, boundaries)
