import constants as c
import math as m
import some_math as sm
import numpy as np
import pygame as pg
from object import Object
from process import Process

def get_update_func(environment_option: str):
    environment = c.ENVIRONMENT_CONDITIONS[environment_option]
    env_dens = environment['density']
    grav_accel = environment['gravitational acceleration']
    kin_vesc = environment['kinematic viscosity']
    env_visc = kin_vesc * env_dens
    with_resist = c.WITH_ENVIRONMENTAL_RESISTANCE

    def update_func(self: Process, passed_time: float, return_period: bool = False) -> list | float:
        def check_amplitude(obj: Object) -> None:
            def is_left_amplitude() -> bool:
                center = obj.attachment_point
                x_c, y_c = center
                posits = obj.positions
                pos_bef, pos, pos_aft = posits[-3][0], posits[-2][0], posits[-1][0]
                x_b, y_b = pos_bef
                x, y = pos
                x_a, y_a = pos_aft
                res = ((x_c - x) > 0) & ((x_b - x) > 0) & ((x_a - x) > 0)
                return res
            
            period_data = None
            if is_left_amplitude():
                amp = obj.positions[-2]
                amp_pos, amp_time = amp
                center = obj.attachment_point
                amp_pos_ang = sm.vector_from_point_to_point(center, amp_pos)[1]
                zero_pos_ang = grav_accel[1]
                amp_ang = abs(zero_pos_ang - amp_pos_ang) % 360
                radius = obj.thread_length
                circle_len = 2 * m.pi * radius
                amplitude = circle_len * amp_ang / 360
                last_time = obj.last_amplitude_time
                if (not (last_time is None)):
                    period = amp_time - last_time
                    if (not return_period):
                        print(f'amplitude: {amplitude:.2f} m, period: {period:.2f} s')
                    
                    period_data = getattr(obj, 'period_data', (0, 0))
                    period_data = (period_data[0] + period, period_data[1] + 1)
                    obj.period_data = period_data
                else:
                    if (not return_period):
                        print(f'amplitude: {amplitude:.2f} m')
                obj.last_amplitude_time = amp_time
                obj.last_amplitude = amplitude
                first_amplitude = getattr(obj, 'first_amplitude', None)
                obj.first_amplitude = amplitude if (first_amplitude is None) else first_amplitude

            max_speed = getattr(obj, 'max_speed', 0)
            obj.max_speed = max(max_speed, abs(obj.speed[0]))

            if ((period_data) and (period_data[1] > 20)):
                return (period_data[0] / period_data[1])
        
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
            arch_accel = archimedes_accel(obj) if c.WITH_ARCHIMEDES_FORCE else (0, 0)
            resist_accel = resistance_accel(obj) if c.WITH_ENVIRONMENTAL_RESISTANCE else (0, 0)

            sum_accel = sm.sum_vectors([grav_accel, arch_accel, resist_accel])

            pos = obj.position
            center = obj.attachment_point
            speed = obj.speed
            radius = obj.thread_length
            t = passed_time

            new_pos_free = sm.move_point_by_vector(pos,
                                                   sm.vector_sum(sm.vector_times(speed, t),
                                                                 sm.vector_times(sum_accel, (t ** 2) / 2)))
            
            radius_vector_old = sm.vector_from_point_to_point(center, pos)
            radius_vector_free = sm.vector_from_point_to_point(center, new_pos_free)
            radius_vector_new = (radius, radius_vector_free[1])

            new_pos = sm.move_point_by_vector(center, radius_vector_new)
            
            speed_turned = (speed[0], speed[1] + (radius_vector_new[1] - radius_vector_old[1]))
            movement_axis = (1, sm.vector_from_point_to_point(pos, new_pos)[1])
            
            pot_accel = sm.vector_sum(grav_accel, arch_accel)
            resist_accel_turned = (resist_accel[0], resist_accel[1] + (movement_axis[1] - speed[1]))

            pot_speed_diff = sm.vector_times(pot_accel, t)
            resist_speed_diff = sm.vector_times(resist_accel_turned, t)

            pot_diff_proj = sm.projection(pot_speed_diff, movement_axis)
            mid_speed = sm.vector_sum(speed_turned, pot_diff_proj)

            max_resist_diff_proj = sm.vector_times(sm.projection(mid_speed, movement_axis), (-1))
            resist_diff_proj = resist_speed_diff if (max_resist_diff_proj[0] >= resist_speed_diff[0]) else max_resist_diff_proj

            new_speed = sm.vector_sum(mid_speed, resist_diff_proj)

            v_0, v_d = speed[0], -(resist_diff_proj[0])
            g = pot_accel[0]
            h_0, h_f = pos[1], new_pos[1]
            v_f = m.sqrt(abs((2 * g * (h_0 - h_f)) + (v_0 ** 2)))
            new_speed = ((v_f + v_d), new_speed[1])

            last_time = obj.positions[-1][1]
            curr_time = last_time + t
            obj.position = new_pos
            obj.positions.append((new_pos, curr_time))
            obj.positions = obj.positions[1:]
            obj.speed = sm.vector_to_standard(new_speed)
            obj.tilt_angle = 90 + radius_vector_new[1]

        def update_motion_new(obj: Object) -> None: # doesn't work on the whole range
            arch_accel = archimedes_accel(obj) if c.WITH_ARCHIMEDES_FORCE else (0, 0)
            resist_accel = resistance_accel(obj) if c.WITH_ENVIRONMENTAL_RESISTANCE else (0, 0)

            sum_accel = sm.sum_vectors([grav_accel, arch_accel, resist_accel])

            pos = obj.position
            center = obj.attachment_point
            speed = obj.speed
            radius = obj.thread_length
            t = passed_time
            l = 2 * m.pi * radius
            
            shift = (speed[0] * t) + (((sm.projection_codirectional(sum_accel, speed)[0]) * (t ** 2)) / 2)
            ang_shift = 360 * (shift / l)

            new_pos_free = sm.move_point_by_vector(pos,
                                                   sm.vector_sum(sm.vector_times(speed, t),
                                                                 sm.vector_times(sum_accel, (t ** 2) / 2)))
            
            radius_vector_old = sm.vector_from_point_to_point(center, pos)
            radius_vector_free = sm.vector_from_point_to_point(center, new_pos_free)
            radius_vector_new = (radius, radius_vector_free[1])

            signed_ang_shift = np.sign(radius_vector_new[1] - radius_vector_old[1]) * abs(ang_shift)
            radius_vector_new = (radius, radius_vector_old[1] + signed_ang_shift)

            new_pos = sm.move_point_by_vector(center, radius_vector_new)
            
            speed_turned = (speed[0], speed[1] + (radius_vector_new[1] - radius_vector_old[1]))
            movement_axis = (1, sm.vector_from_point_to_point(pos, new_pos)[1])
            
            pot_accel = sm.vector_sum(grav_accel, arch_accel)
            resist_accel_turned = (resist_accel[0], resist_accel[1] + (movement_axis[1] - speed[1]))

            pot_speed_diff = sm.vector_times(pot_accel, t)
            resist_speed_diff = sm.vector_times(resist_accel_turned, t)

            pot_diff_proj = sm.projection(pot_speed_diff, movement_axis)
            mid_speed = sm.vector_sum(speed_turned, pot_diff_proj)

            max_resist_diff_proj = sm.vector_times(sm.projection(mid_speed, movement_axis), (-1))
            resist_diff_proj = resist_speed_diff if (max_resist_diff_proj[0] >= resist_speed_diff[0]) else max_resist_diff_proj

            new_speed = sm.vector_sum(mid_speed, resist_diff_proj)

            v_0, v_d = speed[0], -(resist_diff_proj[0])
            g = pot_accel[0]
            h_0, h_f = pos[1], new_pos[1]
            v_f = m.sqrt(abs((2 * g * (h_0 - h_f)) + (v_0 ** 2)))
            new_speed = ((v_f + v_d), new_speed[1])

            last_time = obj.positions[-1][1]
            curr_time = last_time + t
            obj.position = new_pos
            obj.positions.append((new_pos, curr_time))
            obj.positions = obj.positions[1:]
            obj.speed = sm.vector_to_standard(new_speed)
            obj.tilt_angle = 90 + radius_vector_new[1]
        
        trace_data = list()
        
        for obj in self.objects:
            period = check_amplitude(obj)
            update_motion(obj)

            positions = obj.positions
            last_position, new_position = positions[-2][0], positions[-1][0]
            trace_data.append((last_position, new_position, obj.trace_color))

        if (return_period):
            return period
        return trace_data
    
    return update_func

def set_background(window_size: tuple[int, int]):
    background = pg.Surface((window_size), pg.SRCALPHA)
    background.fill((0, 0, 0, 0))
    return background

def get_circle(color: tuple[int, int, int, int], radius: int):
    image = pg.Surface((2 * radius, 2 * radius), pg.SRCALPHA)
    pg.draw.circle(image, color, (radius, radius), radius)
    return image

def get_rect(color: tuple[int, int, int, int], size: tuple[int, int]):
    image = pg.Surface(size, pg.SRCALPHA)
    pg.draw.rect(image, color, pg.Rect(0, 0, size[0], size[1]))
    return image

def set_object(object_option: str, obj_speed: tuple[float, float], attachment: tuple[float, float]) -> Object:
    parameters = c.OBJECTS[object_option]

    obj_shape = parameters['shape']
    obj_drag_coefficient = parameters['drag coefficient']
    obj_mass = parameters['mass']
    color_no_alpha = parameters['color']
    color = (color_no_alpha[0], color_no_alpha[1], color_no_alpha[2], c.DRAWING_OPACITY)
    obj_thread_length = c.THREAD_LENGTH
    obj_position = c.X, c.Y
    if (obj_shape == 'parallelogram'):
        obj_size = parameters['size']
        image = get_rect(color, (100, 100))
        obj = Object(image, size = obj_size,
                            position = obj_position,
                            speed = obj_speed,
                            attachment_point = attachment,
                            shape = obj_shape,
                            mass = obj_mass,
                            trace_color = color_no_alpha,
                            drag_coefficient = obj_drag_coefficient,
                            thread_length = obj_thread_length,
                            movable = True)
    elif (obj_shape == 'sphere'):
        obj_radius = parameters['radius']
        image = get_circle(color, 50)
        obj = Object(image, radius = obj_radius,
                            position = obj_position,
                            speed = obj_speed,
                            attachment_point = attachment,
                            shape = obj_shape,
                            mass = obj_mass,
                            trace_color = color_no_alpha,
                            drag_coefficient = obj_drag_coefficient,
                            thread_length = obj_thread_length,
                            movable = True)
    
    return obj

def set_process(environment_option: str, objects_list: list[Object], draw_scale: float, window_size: tuple[int, int], center: tuple[float, float], process_info: str) -> Process:
    process = Process(objects = objects_list,
                      scale = draw_scale,
                      background = set_background(window_size),
                      center_point = center,
                      description = process_info,
                      update = get_update_func(environment_option))
    return process

def get_real_period(process: Process) -> float:
    UPDATE_TIME_PERIOD = 0.03 # seconds

    period = None
    while (not period):
        period = process.update(UPDATE_TIME_PERIOD, True)

    return period