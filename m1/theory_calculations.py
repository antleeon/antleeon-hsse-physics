import scipy
import constants as const
import some_math
import math

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
    
    TIME_ACCURACY = 0.0001
    TIME_INTERVAL = (0, 5)
        
    HEIGHT = -(const.HEIGHT)
        
    def height_func_linear_resistance(t):
        m = const.MASS
        g = const.GRAVITATIONAL_ACCELERATION[0]
        k = 6 * math.pi * const.ENVIRONMENT_VISCOSITY * const.RADIUS
        v_0 = (some_math.projection(const.SPEED, (1, 90)))[0]
        e = math.e

        height = (m / k) * (((m * g / k) + v_0) * (1 - (e ** (-k * t / m))) - (g * t))
        
        return height
    
    # def height_func_quadratic_resistance(t): TODO
    
    height_funcs_dict = {'linear': height_func_linear_resistance}

    def distance_func_linear_resistance(t):
        m = const.MASS
        k = 6 * math.pi * const.ENVIRONMENT_VISCOSITY * const.RADIUS
        v_0 = (some_math.projection(const.SPEED, (1, 0)))[0]
        e = math.e

        distance = (m * v_0 / k) * (1 - (e ** (-k * t / m)))
        
        return distance
    
    # def distance_func_quadratic_resistance(t): TODO
    
    distance_funcs_dict = {'linear': distance_func_linear_resistance}
    
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

