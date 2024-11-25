from object import Object
from process import Process
import pygame as pg
import math as m
import some_math as sm
import constants as const
import theory_calculations as calc
from time_management import now_milliseconds_since_month as timestamp

def update_motion(obj: Object, passed_time: float) -> None:
    v = obj.speed
    pos = obj.position
    
    obj.position = sm.move_point_by_vector(pos, sm.vector_times(v, passed_time))

def count_impulse_debts(objs: list[Object]) -> None:
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

                dist = sm.distance(obj1.position, obj2.position)
                r_sum = obj1.radius + obj2.radius
                if (dist < r_sum):
                    unite_groups(groups, groups_map, i, j)
        
        return groups
    
    imp_groups = group_objects(objs)
    for group in imp_groups:
        imp = sm.sum_vectors([sm.vector_times(objs[i].speed, objs[i].mass) for i in group])
        group_mass = sum([objs[i].mass for i in group])
        for i in group:
            objs[i].impulse_debt = sm.sum_vectors([sm.vector_times(objs[i].speed, ((-1) * objs[i].mass)), (imp * objs[i].mass / group_mass)])

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
                          trace_color = const.COLOR1)
    objects.append(obj1)
    
    image2 = pg.Surface((100, 100), pg.SRCALPHA)
    color2 = (const.COLOR2[0], const.COLOR2[1], const.COLOR2[2], const.DRAWING_OPACITY)
    pg.draw.circle(image2, color2, (50, 50), 50)
    obj2 = Object(image2, radius = const.RADIUS2,
                          position = (const.X2, const.Y2),
                          speed = speed2,
                          mass = const.MASS2,
                          trace_color = const.COLOR2)
    objects.append(obj2)

    for obj in objects:
        obj.impulse_debt = (0, 0)

    return objects

def set_process_two_balls_impulse(objects_list: list[Object], process_time: float, draw_scale: float, window_size: tuple[int, int], center: tuple[float, float]) -> Process:
    process = Process(objects = objects_list,
                      duration = process_time,
                      scale = draw_scale,
                      background = set_background(window_size),
                      center_point = center,
                      description = 'two balls colliding with constant impulse',
                      update = two_balls_impulse_update)