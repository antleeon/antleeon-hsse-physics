import constants as const
import some_math as sm
import math as m

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
        trajectory_length = 2 * m.pi * trajectory_radius
        speed_size = (angular_velocity / 360) * trajectory_length # not speed_abs, as it's signed (where negative is opposite direction)
        thread_angle = const.ANGLE
        speed_angle = thread_angle + 180
        speed = (speed_size, speed_angle)
        return sm.vector_to_standard(speed)
    
    def count_boundaries() -> tuple[tuple[float, float], tuple[float, float]]:
        x, y = const.X, const.Y
        speed = count_speed()
        speed_abs = speed[0]
        mass = const.OBJECTS[object_option]['mass']
        shape = const.OBJECTS[object_option]['shape']
        if (shape == 'sphere'):
            radius = const.OBJECTS[object_option]['radius']
            size = (radius * 2, radius * 2)
            w, h = size
        elif (shape == 'parallelogram'):
            size = const.OBJECTS[object_option]['size']
            w, h = size
        kinetic_energy = 0.5 * mass * (speed_abs ** 2)
        g = const.ENVIRONMENT_CONDITIONS[environment_option]['gravitational acceleration']
        thread_angle = const.ANGLE
        thread_len = const.THREAD_LENGTH
        cos = m.cos(sm.to_radians(thread_angle))
        max_possible_uprise = thread_len * (1 + cos)
        max_uprise = max(kinetic_energy / (mass * g[0]), max_possible_uprise)
        x_c, y_c = count_attachment_point()
        min_x, max_x = x_c - (thread_len + w), x_c + (thread_len + w)
        min_y, max_y = y_c - (thread_len + h), y + (max_uprise + h)
        return ((min_x, min_y), (max_x, max_y))
    
    def count_period_very_approximately() -> float:
        angular_velocity = const.ANGULAR_VELOCITY
        return (360 / angular_velocity)

    def count_period() -> float:
        def count_self_accel() -> tuple[float, float]:
            def count_volume() -> float:
                object = const.OBJECTS[object_option]
                shape = object['shape']
                if (shape == 'sphere'):
                    radius = object['radius']
                    volume = (4 / 3) * m.pi * (radius ** 3)
                elif (shape == 'parallelogram'):
                    w, h = object['size']
                    third_dim = h # assuming it's a square from the side
                    volume = w * h * third_dim
                else:
                    volume = 0
                return volume
            
            volume = count_volume()
            mass = const.OBJECTS[object_option]['mass']
            g = const.ENVIRONMENT_CONDITIONS[environment_option]['gravitational acceleration']
            dens = const.ENVIRONMENT_CONDITIONS[environment_option]['density']
            arch_ang = g[1] + 180
            arch_abs = g[0] * volume * dens
            accel_ang = arch_ang
            accel_abs = arch_abs / mass
            self_accel = sm.vector_to_standard((accel_abs, accel_ang))
            
            return self_accel
        
        len = const.THREAD_LENGTH
        gravitational_acceleration = const.ENVIRONMENT_CONDITIONS[environment_option]['gravitational acceleration']
        self_acceleration = count_self_accel()
        acceleration = sm.vector_sum(gravitational_acceleration, self_acceleration)
        vert_accel = sm.projection_codirectional(acceleration, (1, -90))
        accel_abs = vert_accel[0]
        period = 2 * m.pi * m.sqrt(abs(len / accel_abs))

        return period
    
    def count_max_speed_abs() -> float:
        speed = count_speed()
        m = const.OBJECTS[object_option]['mass']
        g = const.ENVIRONMENT_CONDITIONS[environment_option]['gravitational acceleration']
        attachment = count_attachment_point()
        len = const.THREAD_LENGTH
        y_lowest = attachment[1] - len
        x, y = const.X, const.Y
        curr_h = y - y_lowest
        energy_pot = m * g[0] * curr_h
        energy_kin = 0.5 * m * (speed[0] ** 2)
        energy = energy_pot + energy_kin
        max_speed_abs = (2 * energy / m) ** 0.5

        return max_speed_abs
    
    def count_amplitude() -> float:
        l = const.THREAD_LENGTH
        mass = const.OBJECTS[object_option]['mass']
        g = const.ENVIRONMENT_CONDITIONS[environment_option]['gravitational acceleration'][0]
        v = count_max_speed_abs()
        energy_sum = mass * (v ** 2) / 2
        energy_pot_max = mass * g * (2 * l)
        energy_pot = min(energy_sum, energy_pot_max)
        h = energy_pot / (mass * g)
        cos = -((h / l) - 1) # h = l * (1 - cos)
        ang = sm.to_degrees(m.acos(cos))
        circle_length = 2 * m.pi * l
        amplitude = circle_length * (ang / 360)

        return amplitude
    
    res = dict()

    res['boundaries'] = count_boundaries()
    res['period'] = count_period()
    res['attachment'] = count_attachment_point()
    res['speed'] = count_speed()
    res['maximum speed module'] = count_max_speed_abs()
    res['amplitude'] = count_amplitude()

    return res