import constants as const
import some_math as sm
import math as m
from object import Object
import copy

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
    
def count_boundaries_simplified(objs: list[Object], time: float = 0) -> tuple[tuple[float, float], tuple[float, float]] | None:
    if (not (len(objs) > 0)):
        return None
    
    x_min, y_min = objs[0].position[0] - (objs[0].size[0] / 2), objs[0].position[1] - (objs[0].size[1] / 2)
    x_max, y_max = objs[0].position[0] + (objs[0].size[0] / 2), objs[0].position[1] + (objs[0].size[1] / 2)

    for obj in objs:
        x_0, y_0 = obj.position
        x_f, y_f = sm.move_point_by_vector(obj.position, sm.vector_times(obj.speed, time))

        x_min = min(x_min,
                    x_0 - (objs[0].size[0] / 2),
                    x_f - (objs[0].size[0] / 2))
        y_min = min(y_min,
                    y_0 - (objs[0].size[1] / 2),
                    y_f - (objs[0].size[1] / 2))
        x_max = max(x_max,
                    x_0 + (objs[0].size[0] / 2),
                    x_f + (objs[0].size[0] / 2))
        y_max = max(y_max,
                    y_0 + (objs[0].size[1] / 2),
                    y_f + (objs[0].size[1] / 2))

    return ((x_min, y_min), (x_max, y_max))

# two balls collision
def get_speeds_and_time() -> dict:
    def count_angles_and_collision_time(collision_angle: float, obj1: Object, obj2: Object) -> tuple[tuple[float, float], float]:
        shift_angle = sm.vector_from_point_to_point(obj1.position, obj2.position)[1]
        ANGLE_APPROXIMATION = const.ANGLE_APPROXIMATION
        
        def check_not_pi(angle: float) -> bool:
            while (angle < 0):
                angle += 360
            angle_round = int(angle)
            return (((angle_round % 180) > ANGLE_APPROXIMATION) and ((angle_round % 180) < (180 - ANGLE_APPROXIMATION)))
        
        def max_time(angle1: float) -> float:
            angle2 = 180 - (collision_angle + angle1)
            distance = sm.distance(obj1.position, obj2.position)
            v1_abs, v2_abs = obj1.speed[0], obj2.speed[0]
            
            dist1 = distance * m.sin(sm.to_radians(angle2)) / m.sin(sm.to_radians(collision_angle))
            dist2 = distance * m.sin(sm.to_radians(angle1)) / m.sin(sm.to_radians(collision_angle))

            t1_max = dist1 / v1_abs
            t2_max = dist2 / v2_abs

            return max(t1_max, t2_max)

        def approx_time_meet(angle1: float) -> float | None:
            angle2 = (collision_angle + angle1)
            t_max = 2 * max_time(angle1)
            
            v1, v2 = (obj1.speed[0], shift_angle + angle1), (obj2.speed[0], shift_angle + angle2)
            pos1, pos2 = obj1.position, obj2.position
            r1, r2 = obj1.radius, obj2.radius
            
            checking_quantity = 100
            for i in range(checking_quantity):
                t_curr = t_max * (i + 1) / checking_quantity
                pos1_new = sm.move_point_by_vector(pos1, sm.vector_times(v1, t_curr))
                pos2_new = sm.move_point_by_vector(pos2, sm.vector_times(v2, t_curr))
                dist_new = sm.distance(pos1_new, pos2_new)
                if (dist_new <= (r1 + r2)):
                    return t_curr
            return None
        
        def meet_before_cross(angle1: float) -> bool:
            t_meet = approx_time_meet(angle1)
            return (not (t_meet is None))
        
        def find_angle(checker, step, interval) -> float | None:
            first_fitting = None
            last_fitting = None

            start = min(interval[0], interval[1])
            finish = max(interval[0], interval[1])
            steps_quan = int((finish - start) / step)

            for step_numb in range(steps_quan):
                angle = start + (((finish - start) / steps_quan) * step_numb)
                if checker(angle):
                    if (first_fitting is None):
                        first_fitting = angle
                    last_fitting = angle
                else:
                    if (not (last_fitting is None)):
                        result = first_fitting + ((last_fitting - first_fitting) / 2)
                        return result
            
            return None

        if check_not_pi(collision_angle):
            angle_interval = (0, (180 - collision_angle))
            angle_accuracy = 0.2
            angle_predicate = meet_before_cross

            angle1 = find_angle(angle_predicate, angle_accuracy, angle_interval)
            angle2 = (collision_angle + angle1)
            approx_time = approx_time_meet(angle1)
        else:
            angle1, angle2 = 0, 180
            approx_time = sm.distance(obj1.position, obj2.position) / (obj1.speed[0] + obj2.speed[0])
        
        return ((shift_angle + angle1, shift_angle + angle2), approx_time)

    OBJECT1 = Object(None, radius = const.RADIUS1,
                           mass = const.MASS1,
                           position = (const.X1, const.Y1),
                           speed = (const.SPEED1_ABS, None))

    OBJECT2 = Object(None, radius = const.RADIUS2,
                           mass = const.MASS2,
                           position = (const.X2, const.Y2),
                           speed = (const.SPEED2_ABS, None))

    angles, collision_time = count_angles_and_collision_time(const.COLLISION_ANGLE, OBJECT1, OBJECT2)
    SPEED1_ANG, SPEED2_ANG = angles
    process_time = 2 * collision_time

    OBJECT1.speed = (OBJECT1.speed[0], SPEED1_ANG)
    OBJECT2.speed = (OBJECT2.speed[0], SPEED2_ANG)

    boundaries = count_boundaries_simplified([OBJECT1, OBJECT2], process_time)

    res = dict()
    res['speed1'] = OBJECT1.speed
    res['speed2'] = OBJECT2.speed
    res['process time'] = process_time
    res['boundaries'] = boundaries

    return res

# one ball hitting a wall
def get_speed_and_time() -> dict:
    def count_angle_and_collision_time(obj: Object, wall: Object) -> tuple[float, float]:
        concentric_vector = sm.vector_from_point_to_point(obj.position, wall.position)

        def is_point_inside_wall(shift_part: float) -> bool:
            start_point = obj.position
            shift_vector = sm.vector_times(concentric_vector, shift_part)
            point = sm.move_point_by_vector(start_point, shift_vector)
            wall_center = wall.position
            wall_size = wall.size
            result = sm.is_inside_rectangle(point, (wall_center, wall_size))
            return result
        
        vector_length_part_interval = (0, 1)
        vector_length_part_predicate = is_point_inside_wall
        vector_lenght_part_accuracy = 0.001

        vector_length_part = binary_find_argument(vector_length_part_predicate, vector_lenght_part_accuracy, vector_length_part_interval)
        to_border_shift_vector = sm.vector_times(concentric_vector, vector_length_part)
        border_point = sm.move_point_by_vector(obj.position, to_border_shift_vector)

        def find_border_center_point(point: tuple[float, float]) -> bool:
            x, y = point
            x_c, y_c = wall.position
            w, h = wall.size
            x_l, y_l = x_c - (w / 2), y_c
            x_r, y_r = x_c + (w / 2), y_c
            x_t, y_t = x_c, y_c + (h / 2)
            x_b, y_b = x_c, y_c - (h / 2)
            hor_from_border = min(abs(x - x_l), abs(x - x_r)) / (w / 2)
            vert_from_border =  min(abs(y - y_t), abs(y - y_b)) / (h / 2)
            vertical_border = (hor_from_border < vert_from_border)
            if vertical_border:
                y = y_c
            else:
                x = x_c
            return ((x, y), vertical_border)
        
        border_center_point, border_is_vertical = find_border_center_point(border_point)
        radius = obj.radius
        concentric_angle = concentric_vector[1]
        if border_is_vertical:
            move_right = int(m.cos(sm.to_radians(concentric_angle)) > 0) - int(m.cos(sm.to_radians(concentric_angle)) < 0)
            shift_back = (radius, 90 + (90 * move_right))
        else:
            move_up = int(m.sin(sm.to_radians(concentric_angle)) > 0) - int(m.sin(sm.to_radians(concentric_angle)) < 0)
            shift_back = (radius, 0 - (90 * move_up))

        ball_collision_center_point = sm.move_point_by_vector(border_center_point, shift_back)
        tragectory_vector = sm.vector_from_point_to_point(obj.position, ball_collision_center_point)

        angle = tragectory_vector[1]
        collision_time = tragectory_vector[0] / (obj.speed[0])

        return (angle, collision_time)

    OBJECT0 = Object(None, radius = const.RADIUS0,
                           mass = const.MASS0,
                           position = (const.X0, const.Y0),
                           speed = (const.SPEED0_ABS, None))
    
    WALL_OBJECT = Object(None, size = const.WALL_SIZE,
                               mass = const.WALL_MASS,
                               position = (const.WALL_X, const.WALL_Y),
                               speed = (0, 0),
                               movable = False)
    
    SPEED0_ANG, collision_time = count_angle_and_collision_time(OBJECT0, WALL_OBJECT)
    process_time = 2 * collision_time

    OBJECT0.speed = (OBJECT0.speed[0], SPEED0_ANG)

    boundaries = count_boundaries_simplified([OBJECT0, WALL_OBJECT], process_time)

    res = dict()
    res['speed'] = OBJECT0.speed
    res['process time'] = process_time
    res['boundaries'] = boundaries

    return res