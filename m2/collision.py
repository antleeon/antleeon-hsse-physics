from object import Object
from process import Process
import pygame as pg
import math as m
import some_math as sm
import constants as const
import theory_calculations as calc
from time_management import now_milliseconds_since_month as timestamp

def is_colliding(obj1: Object, obj2: Object) -> bool:
    # here i assume that bricks are never tilted (always standing/laying 90 degrees straight)
    sh1 = obj1.shape
    sh2 = obj2.shape

    if (sh1 == sh2 == 'ball'):
        r_sum = obj1.radius + obj2.radius
        dist = sm.distance(obj1.position, obj2.position)

        return (dist < r_sum)
    elif (sh1 == sh2 == 'brick'):
        w1, h1 = obj1.size
        w2, h2 = obj2.size
        x1, y1 = obj1.position
        x2, y2 = obj2.position

        cross_hor = abs(x1 - x2) <= ((w1 + w2) / 2)
        cross_vert = abs(y1 - y2) <= ((h1 + h2) / 2)

        return (cross_hor and cross_vert)
    elif (([sh1, sh2].sort()) == (['ball', 'brick'].sort())):
        if (sh1 == 'ball'):
            ball, brick = obj1, obj2
        else:
            ball, brick = obj2, obj1
        
        brick_center = brick.position
        w, h = brick.size
        ball_center = ball.position
        r = ball.radius

        vert1 = (brick_center[0] - (w / 2), brick_center[1] + (h / 2))
        vert2 = (brick_center[0] + (w / 2), brick_center[1] + (h / 2))
        vert3 = (brick_center[0] + (w / 2), brick_center[1] - (h / 2))
        vert4 = (brick_center[0] - (w / 2), brick_center[1] - (h / 2))

        brick_bubble = {'rect1': (brick_center, (w + 2 * r, h)),
                        'rect2': (brick_center, (w, h + 2 * r)),
                        'circle1': (vert1, r),
                        'circle2': (vert2, r),
                        'circle3': (vert3, r),
                        'circle4': (vert4, r)}
        
        result = any([sm.is_inside_rectangle(ball_center, brick_bubble['rect1']),
                      sm.is_inside_rectangle(ball_center, brick_bubble['rect2']),
                      sm.is_inside_circle(ball_center, brick_bubble['circle1']),
                      sm.is_inside_circle(ball_center, brick_bubble['circle2']),
                      sm.is_inside_circle(ball_center, brick_bubble['circle3']),
                      sm.is_inside_circle(ball_center, brick_bubble['circle4'])])

        return result
    else:
        return False
    
def get_collision_direction(obj1: Object, obj2: Object) -> tuple[float, float]:
    if (obj1.shape == obj2.shape == 'ball'):
        return sm.vector_from_point_to_point(obj1.position, obj2.position)
    else:
        x1_c, y1_c = obj1.position
        x2_c, y2_c = obj2.position
        w1, h1 = obj1.size
        w2, h2 = obj2.size
        
        x1_min, y1_min = x1_c - (w1 / 2), y1_c - (h1 / 2)
        x1_max, y1_max = x1_c + (w1 / 2), y1_c + (h1 / 2)
        x2_min, y2_min = x2_c - (w2 / 2), y2_c - (h2 / 2)
        x2_max, y2_max = x2_c + (w2 / 2), y2_c + (h2 / 2)

        hor_dist = min(abs(x1_min - x2_min), abs(x1_min - x2_max), abs(x1_max - x2_min), abs(x1_max - x2_max))
        vert_dist = min(abs(y1_min - y2_min), abs(y1_min - y2_max), abs(y1_max - y2_min), abs(y1_max - y2_max))

        if (hor_dist < vert_dist):
            return sm.vector_to_standard((x2_c - x1_c), 0)
        else:
            return sm.vector_to_standard((y2_c - y1_c), 90)

def count_impulse_debts(objs: list[Object]) -> None: # not using this currently
    def group_objects(objects: list[Object]) -> list[set]:
        def unite_groups(gr: list[set], gr_map: list[int], a: int, b: int) -> None:
            idx1 = gr_map[a]
            idx2 = gr_map[b]

            if (idx1 == idx2):
                return
            
            gr.append(gr[idx1] | gr[idx2])

            idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
            gr.pop(idx2)
            gr.pop(idx1)

            new_idx = len(gr) - 1
            gr_map[a] = new_idx
            gr_map[b] = new_idx
        
        groups = list()
        groups_map = list()
        for i, obj in enumerate(objects):
            groups.append({int(i)})
            groups_map.append(i)

        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if (i == j):
                    continue

                if is_colliding(obj1, obj2):
                    unite_groups(groups, groups_map, i, j)
        
        return groups
    
    imp_groups = group_objects(objs)
    for group in imp_groups:
        imp = sm.sum_vectors([sm.vector_times(objs[i].speed, objs[i].mass) for i in group])
        group_mass = sum([objs[i].mass for i in group])
        for i in group:
            objs[i].impulse_debt = sm.sum_vectors([sm.vector_times(objs[i].speed, ((-1) * objs[i].mass)), (imp * objs[i].mass / group_mass)])

def update_motion(obj: Object, passed_time: float) -> None:
    if (not (obj.movable)):
        return
    
    v = obj.speed
    pos = obj.position
    
    obj.position = sm.move_point_by_vector(pos, sm.vector_times(v, passed_time))

def check_collision(obj1: Object, obj2: Object) -> None:
    if (not is_colliding(obj1, obj2)):
        return
    
    col_dir = get_collision_direction(obj1, obj2)

def update_speed(obj: Object) -> None:
    v = obj.speed
    imp_diff = obj.impulse_debt
    m = obj.mass

    obj.speed = sm.sum_vectors([v, sm.vector_times(imp_diff, (1 / m))])
    obj.impulse_debt = (0, 0)

def two_balls_impulse_update(self, passed_time):
    
    
    return list()

def set_background(window_size: tuple[int, int]):
    background = pg.Surface((window_size), pg.SRCALPHA)
    background.fill((0, 0, 0, 0))
    return background

def set_objects_two_balls(speed1: tuple[float, float], speed2: tuple[float, float]) -> list[Object]:
    objects = list()

    image1 = pg.Surface((100, 100), pg.SRCALPHA)
    color1 = (const.COLOR1[0], const.COLOR1[1], const.COLOR1[2], const.DRAWING_OPACITY)
    pg.draw.circle(image1, color1, (50, 50), 50)
    obj1 = Object(image1, radius = const.RADIUS1,
                          position = (const.X1, const.Y1),
                          speed = speed1,
                          mass = const.MASS1,
                          trace_color = const.COLOR1,
                          shape = 'ball')
    objects.append(obj1)
    
    image2 = pg.Surface((100, 100), pg.SRCALPHA)
    color2 = (const.COLOR2[0], const.COLOR2[1], const.COLOR2[2], const.DRAWING_OPACITY)
    pg.draw.circle(image2, color2, (50, 50), 50)
    obj2 = Object(image2, radius = const.RADIUS2,
                          position = (const.X2, const.Y2),
                          speed = speed2,
                          mass = const.MASS2,
                          trace_color = const.COLOR2,
                          shape = 'ball')
    objects.append(obj2)

    return objects

def set_process_two_balls_impulse(objects_list: list[Object], process_time: float, draw_scale: float, window_size: tuple[int, int], center: tuple[float, float]) -> Process:
    process = Process(objects = objects_list,
                      duration = process_time,
                      scale = draw_scale,
                      background = set_background(window_size),
                      center_point = center,
                      description = 'two balls colliding with constant impulse',
                      update = two_balls_impulse_update)