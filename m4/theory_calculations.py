import constants as const
import some_math as sm
import math as m

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

def count(environment_option: str, object_option: str) -> dict:
    def count_attachment_point() -> tuple[float, float]:
        angle = const.ANGLE
        thread_len = const.THREAD_LENGTH
        sin, cos = m.sin(sm.to_radians(angle)), m.cos(sm.to_radians(angle))
        x_shift, y_shift = -sin * thread_len, cos * thread_len
        attachment = (const.X + x_shift, const.Y + y_shift)
        return attachment
    
    def count_speed() -> tuple[float, float]:
        angular_velocity = const.ANGULAR_VELOCITY
        trajectory_radius = const.THREAD_LENGTH
        speed_size = (angular_velocity / 360) * trajectory_radius # not speed_abs, as it's signed (where negative is opposite direction)
        thread_angle = const.ANGLE
        speed_angle = thread_angle + 90
        speed = (speed_size, speed_angle)
        return sm.vector_to_standard(speed)
    
    def count_boundaries() -> tuple[tuple[float, float], tuple[float, float]]:
        x, y = const.X, const.Y
        speed = count_speed()
        speed_abs = speed[0]
        mass = const.OBJECTS[object_option]['mass']
        kinetic_energy = 0.5 * mass * (speed_abs ** 2)
        g = const.ENVIRONMENT_CONDITIONS[environment_option]['gravitational acceleration']
        thread_angle = const.ANGLE
        thread_len = const.THREAD_LENGTH
        cos = m.cos(sm.to_radians(thread_angle))
        max_possible_uprise = thread_len * (1 + cos)
        max_uprise = max(kinetic_energy / (mass * g), max_possible_uprise)
        x_c, y_c = count_attachment_point()
        min_x, max_x = x_c - thread_len, x_c + thread_len
        min_y, max_y = y_c - thread_len, y + max_uprise
        return ((min_x, min_y), (max_x, max_y))
    
    def count_period_very_approximately() -> float:
        angular_velocity = const.ANGULAR_VELOCITY
        return (360 / angular_velocity)
    
    res = dict()

    res['boundaries'] = count_boundaries()
    res['period'] = count_period_very_approximately()
    res['attachment'] = count_attachment_point()
    res['speed'] = count_speed()

    return res