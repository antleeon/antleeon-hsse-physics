import constants as c
import math as m
import some_math as sm
from object import Object
from process import Process

def get_update_func(environment_option: str) -> function:
    environment = c.ENVIRONMENT_CONDITIONS[environment_option]
    env_dens = environment['density']
    grav_accel = environment['gravity acceleration']
    kin_vesc = environment['kinematic viscosity']
    env_visc = kin_vesc * env_dens
    with_resist = c.WITH_ENVIRONMENTAL_RESISTANCE

    def update_func(self: Process, passed_time: float) -> list:
        def resistance_accel(obj: Object) -> tuple[float, float]: # quadratic
            drag = obj.drag_coefficient
            speed = obj.speed
            mass = obj.mass
            ref_area = obj.reference_area()

            force_abs = 0.5 * env_dens * (speed[0] ** 2) * drag * ref_area
            accel_abs = force_abs / mass
            accel_ang = speed[1] + 180
            
            return sm.vector_to_standard((accel_abs, accel_ang))
        
        def archimedes_accel(obj: Object) -> tuple[float, float]:
            mass = obj.mass
            volume = obj.volume()

            force_abs = env_dens * volume * grav_accel[0]
            accel_abs = force_abs / mass
            accel_ang = grav_accel[1] + 180

            return sm.vector_to_standard((accel_abs, accel_ang))

        def update_motion(obj: Object) -> None:
            resist_accel = resistance_accel(obj) if with_resist else (0, 0)
            arch_accel = archimedes_accel(obj)
            min_accel = sm.vector_sum(grav_accel, arch_accel)

            speed = sm.vector_to_standard(obj.speed)
            speed_proj = speed[0]
            min_accel_proj = sm.projection_codirectional(min_accel, speed)[0]
            resist_accel_proj = sm.projection_codirectional(resist_accel, speed)[0]

            t = passed_time
            v = speed_proj
            a0 = min_accel_proj
            a1 = resist_accel_proj

            shift_no_resist = (v * t) + (a0 * (t ** 2) / 2)
            shift_with_resist = (v * t) + ((a0 + a1) * (t ** 2) / 2)
            shift = shift_with_resist if ((shift_no_resist * shift_with_resist) >= 0) else 0

            radius = obj.thread_length
            circle_len = 2 * m.pi * radius
            shift_angle = 360 * shift / circle_len
            
            pos = obj.positions[-1][0]
            center = obj.attachment_point
            to_center = sm.vector_from_point_to_point(pos, center)
            moving_clockwise = (m.sin(sm.to_radians(speed[1] - to_center[1])) > 0)
            angle_coeff = (-1) if moving_clockwise else 1
            
            from_center_old = sm.vector_from_point_to_point(center, pos)
            from_center_new = (radius, (from_center_old[1] + (shift_angle * angle_coeff)))
            
            new_pos = sm.move_point_by_vector(pos, from_center_new)
            last_time = obj.positions[-1][1]
            curr_time = last_time + passed_time
            obj.positions.append((new_pos, curr_time))
            obj.positions = obj.positions[1:]

            a_real = 2 * (shift - (v * t)) / (t ** 2)
            v_new = v + (a_real * t)
            ang_new = from_center_new[1] - (90 * angle_coeff)
            speed_new = sm.vector_to_standard((v_new, ang_new))
            obj.speed = speed_new
            obj.last_acceleration = sm.vector_to_standard((a_real, ang_new))
        
        trace_data = list()
        
        for obj in self.objects:
            check_amplitude(obj)
            update_motion(obj)

            positions = obj.positions
            last_position, new_position = positions[-2][0], positions[-1][0]
            trace_data.append((last_position, new_position, obj.trace_color))

        return trace_data

    
    return update_func