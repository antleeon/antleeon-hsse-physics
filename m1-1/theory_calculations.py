import scipy
import constants as const
import some_math
import math
    
def height_func_linear_resistance(t):
    m = const.MASS
    g = const.GRAVITATIONAL_ACCELERATION[0]
    k = 6 * math.pi * const.KINEMATIC_VISCOSITY * const.ENVIRONMENT_DENSITY * const.RADIUS
    v_0_y = (some_math.projection_codirectional(const.SPEED, (1, 90)))[0]
    e = math.e

    height = (m / k) * (((m * g / k) + v_0_y) * (1 - (e ** (-k * t / m))) - (g * t))
    
    return height

# def height_func_quadratic_resistance(t): TODO

height_funcs_dict = {'linear': height_func_linear_resistance}

def distance_func_linear_resistance(t):
    m = const.MASS
    k = 6 * math.pi * const.KINEMATIC_VISCOSITY * const.ENVIRONMENT_DENSITY * const.RADIUS
    v_0_x = (some_math.projection_codirectional(const.SPEED, (1, 0)))[0]
    e = math.e

    distance = (m * v_0_x / k) * (1 - (e ** (-k * t / m)))
    
    return distance

# def distance_func_quadratic_resistance(t): TODO

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

distance_funcs_dict = {'linear': distance_func_linear_resistance}

def count(air_resistance_type):
    
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

def auto_height(air_resistance_type):
    def time_predicate(time):
        boundaries = (count_trace(air_resistance_type, time))[1]
        return ((boundaries[1][1] - boundaries[0][1]) > (boundaries[1][0] - boundaries[0][0]))

    least_time = (count(air_resistance_type))[0]
    max_time = least_time

    while (not time_predicate(max_time)):
        max_time *= 2

    real_time = binary_find_argument(time_predicate, const.TIME_ACCURACY, (least_time, max_time))
    height_func = height_funcs_dict.get(air_resistance_type, 'linear')
    height = height_func(real_time)
    const.Y_F = height