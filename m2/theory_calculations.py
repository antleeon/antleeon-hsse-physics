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

# two balls collision
def get_speeds_and_time() -> dict:
    def count_angles_and_collision_time(collision_angle: float, obj1: Object, obj2: Object) -> tuple[tuple[float, float], float]:
        def max_time(angle1: float) -> float:
            angle2 = 180 - (collision_angle + angle1)
            distance = sm.distance(obj1.position, obj2.position)
            v1_abs, v2_abs = obj1.speed[0], obj2.speed[0]
            
            dist1 = distance * m.sin(sm.to_radians(angle2)) / m.sin(sm.to_radians(collision_angle))
            dist2 = distance * m.sin(sm.to_radians(angle1)) / m.sin(sm.to_radians(collision_angle))

            t1_max = dist1 / v1_abs
            t2_max = dist2 / v2_abs

            return min(t1_max, t2_max)

        def approx_time_meet(angle1: float) -> float | None:
            angle2 = 180 - (collision_angle + angle1)
            t_max = max_time(angle1)
            
            v1, v2 = (obj1.speed[0], angle1), (obj2.speed[0], angle2)
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
        
        angle_interval = (-180, 0)
        angle_accuracy = 0.2
        angle_predicate = meet_before_cross

        angle1 = binary_find_argument(angle_predicate, angle_accuracy, angle_interval)
        angle2 = 180 - (collision_angle + angle1)

        approx_time = approx_time_meet(angle1)
        
        return ((angle1, angle2), approx_time)
    
    def count_boundaries(obj1: Object, obj2: Object, time: float) -> tuple[tuple[float, float], tuple[float, float]]:
        x1, y1 = obj1.position
        x2, y2 = obj2.position
        
        x3, y3 = sm.move_point_by_vector(obj1.position, sm.vector_times(obj1.speed, time))
        x4, y4 = sm.move_point_by_vector(obj2.position, sm.vector_times(obj2.speed, time))

        x_min, y_min = min(x1, x2, x3, x4), min(y1, y2, y3, y4)
        x_max, y_max = max(x1, x2, x3, x4), max(y1, y2, y3, y4)

        return ((x_min, y_min), (x_max, y_max))

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

    OBJECT1.speed[1] = SPEED1_ANG
    OBJECT2.speed[1] = SPEED2_ANG

    boundaries = count_boundaries(OBJECT1, OBJECT2, process_time)

    res = dict()
    res['speed1'] = OBJECT1.speed
    res['speed2'] = OBJECT2.speed
    res['process time'] = process_time
    res['boundaries'] = boundaries

    return res