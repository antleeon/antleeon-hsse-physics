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

        result = (dist < r_sum)

        return result
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

        hor_dist = min(abs(abs(x1_min - x2_min) - (w1 + w2)),
                       abs(abs(x1_min - x2_max) - (w1 + w2)),
                       abs(abs(x1_max - x2_min) - (w1 + w2)),
                       abs(abs(x1_max - x2_max) - (w1 + w2))) / (w1 + w2)
        vert_dist = min(abs(abs(y1_min - y2_min) - (h1 + h2)),
                        abs(abs(y1_min - y2_max) - (h1 + h2)),
                        abs(abs(y1_max - y2_min) - (h1 + h2)),
                        abs(abs(y1_max - y2_max) - (h1 + h2))) / (h1 + h2)

        if (hor_dist < vert_dist):
            return sm.vector_to_standard(((x2_c - x1_c), 0))
        else:
            return sm.vector_to_standard(((y2_c - y1_c), 90))

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

def update_motion(obj: Object, passed_time: float) -> tuple[tuple[float, float], tuple[float, float], tuple[int, int, int]] | None:
    if (not (obj.movable)):
        obj.speed = (0, 0)
        return None
    
    v = obj.speed
    pos = obj.position
    new_pos = sm.move_point_by_vector(pos, sm.vector_times(v, passed_time))
    obj.position = new_pos

    return (pos, new_pos, obj.trace_color)

def check_conservation_collision(obj1: Object, obj2: Object) -> None:
    # checking if objects could be colliding
    if (not is_colliding(obj1, obj2)):
        return
    # checking if both objects are movable
    if (obj1.movable and obj2.movable):
        # temporary cartesian coordinate axes, where x axis is co-directed with the collision line
        x_axis = sm.resize_vector(get_collision_direction(obj1, obj2), 1)
        y_axis = sm.resize_vector(sm.perpendicular(x_axis), 1)
        # objects' properties (before collision)
        m1, m2 = obj1.mass, obj2.mass
        v1_vect, v2_vect = obj1.speed, obj2.speed
        # projecting speeds onto the axes
        v1, v2 = v1_vect[0], v2_vect[0]
        v1_x, v2_x = sm.projection_codirectional(v1_vect, x_axis)[0], sm.projection_codirectional(v2_vect, x_axis)[0]
        v1_y, v2_y = sm.projection_codirectional(v1_vect, y_axis)[0], sm.projection_codirectional(v2_vect, y_axis)[0]
        # checking if they're actually moving towards each other
        v_x_towards = v1_x - v2_x
        if (v_x_towards <= 0):
            return
        # some constants for formulas simplification
        c1 = (m1 * (v1 ** 2)) + (m2 * (v2 ** 2))
        c2 = (m1 * v1_x) + (m2 * v2_x)
        c3 = (m1 * (v1_y ** 2)) + (m2 * (v2_y ** 2))
        # coefficients of the final quadratic equation & discriminant formula
        a = (m1 * m2) + (m1 ** 2)
        b = (-2) * m1 * c2
        c = (c2 ** 2) - (m2 * c1) + (m2 * c3)
        D = (b ** 2) - (4 * a * c)
        # new x axis speeds projections (after collision)
        v1f_x = (-b - (D ** 0.5)) / (2 * a)
        v2f_x = (c2 - (m1 * v1f_x)) / m2
        # back to vectors
        v1f_x_vect, v2f_x_vect = sm.resize_vector(x_axis, v1f_x), sm.resize_vector(x_axis, v2f_x)
        v1f_y_vect, v2f_y_vect = sm.resize_vector(y_axis, v1_y), sm.resize_vector(y_axis, v2_y)
        v1f_vect, v2f_vect = sm.sum_vectors([v1f_x_vect, v1f_y_vect]), sm.sum_vectors([v2f_x_vect, v2f_y_vect])
        # returning the new speeds to objects
        obj1.speed, obj2.speed = v1f_vect, v2f_vect
        obj1.collided, obj2.collided = True, True
    else:
        if (obj1.movable):
            obj_mov, obj_stat = obj1, obj2
        elif (obj2.movable):
            obj_mov, obj_stat = obj2, obj1
        else:
            return
        # temporary cartesian coordinate axes, where x axis is co-directed with the collision line
        x_axis = sm.resize_vector(get_collision_direction(obj_mov, obj_stat), 1)
        y_axis = sm.resize_vector(sm.perpendicular(x_axis), 1)
        # speed before collision
        v_vect = obj_mov.speed
        # projecting it onto the axes
        v = v_vect[0]
        v_x = sm.projection_codirectional(v_vect, x_axis)[0]
        v_y = sm.projection_codirectional(v_vect, y_axis)[0]
        # checking if the object is actually moving towards the other
        if (v_x <= 0):
            return
        # new x axis speed projection (after collision)
        vf_x = -v_x
        # back to vectors
        vf_x_vect = sm.resize_vector(x_axis, vf_x)
        vf_y_vect = sm.resize_vector(y_axis, v_y)
        vf_vect = sm.sum_vectors([vf_x_vect, vf_y_vect])
        # returning the new speed to object
        obj_mov.speed = vf_vect
        obj_mov.collided, obj_stat.collided = True, False

def conserv_update_result_data(result_data: dict | None, objs: list[Object]) -> dict:
    impulse_sum = (0, 0)
    energy_sum = 0
    for obj in objs:
        v = obj.speed
        m = obj.mass

        impulse = sm.vector_times(v, m)
        energy = 0.5 * m * ((v[0]) ** 2)

        impulse_sum = sm.sum_vectors([impulse_sum, impulse])
        energy_sum = sum([energy_sum, energy])

    if (result_data is None):
        result_data = dict()
        
        result_data['starting impulse'] = impulse_sum
        result_data['starting energy'] = energy_sum

        result_data['max impulse difference percent'] = 0
        result_data['max energy difference percent'] = 0
    else:
        impulse_start = result_data.get('starting impulse', impulse_sum)
        impulse_diff = sm.vector_diff(impulse_sum, impulse_start)
        impulse_diff_percent = int(100 * impulse_diff[0] / impulse_start[0])

        energy_start = result_data.get('starting energy', energy_sum)
        energy_diff = energy_sum - energy_start
        energy_diff_percent = int(100 * energy_diff / energy_start)

        max_impulse_diff_percent = result_data.get('max impulse difference percent', impulse_diff_percent)
        max_energy_diff_percent = result_data.get('max energy difference percent', energy_diff_percent)

        result_data['max impulse difference percent'] = max(impulse_diff_percent, max_impulse_diff_percent)
        result_data['max energy difference percent'] = max(energy_diff_percent, max_energy_diff_percent)

    result_data['last impulse'] = impulse_sum
    result_data['last energy'] = energy_sum

    return result_data

def conserv_update_func(self: Process, passed_time: float) -> list:    
    trace_data = list()
    for obj in self.objects:
        trace_segment = update_motion(obj, passed_time)
        if (not (trace_segment is None)):
            trace_data.append(trace_segment)
        obj.collided = False

    for i, obj1 in enumerate(self.objects):
        if obj1.collided:
            continue
        for j, obj2 in enumerate(self.objects):
            if ((i != j) and (not obj1.collided) and (not obj2.collided)):
                check_conservation_collision(obj1, obj2)
            if obj1.collided:
                break

    self.result_data = conserv_update_result_data(self.result_data, self.objects)
    
    return trace_data

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

def set_objects_one_ball(speed: tuple[float, float]) -> list[Object]:
    objects = list()

    image0 = pg.Surface((100, 100), pg.SRCALPHA)
    color0 = (const.COLOR0[0], const.COLOR0[1], const.COLOR0[2], const.DRAWING_OPACITY)
    pg.draw.circle(image0, color0, (50, 50), 50)
    obj0 = Object(image0, radius = const.RADIUS0,
                          position = (const.X0, const.Y0),
                          speed = speed,
                          mass = const.MASS0,
                          trace_color = const.COLOR0,
                          shape = 'ball')
    objects.append(obj0)
    
    wall_image = pg.Surface((100, 100), pg.SRCALPHA)
    wall_color = (const.WALL_COLOR[0], const.WALL_COLOR[1], const.WALL_COLOR[2], const.DRAWING_OPACITY)
    pg.draw.rect(wall_image, wall_color, pg.Rect(0, 0, 100, 100))
    wall_obj = Object(wall_image, size = const.WALL_SIZE,
                                  position = (const.WALL_X, const.WALL_Y),
                                  speed = (0, 0),
                                  mass = const.WALL_MASS,
                                  trace_color = const.WALL_COLOR,
                                  shape = 'brick',
                                  movable = False)
    objects.append(wall_obj)

    return objects

def set_process_two_balls_conserv(objects_list: list[Object], process_time: float, draw_scale: float, window_size: tuple[int, int], center: tuple[float, float]) -> Process:
    process = Process(objects = objects_list,
                      duration = process_time,
                      scale = draw_scale,
                      background = set_background(window_size),
                      center_point = center,
                      description = 'two balls colliding according to laws of energy and impulse conservation',
                      update = conserv_update_func)
    return process

def set_process_one_ball_conserv(objects_list: list[Object], process_time: float, draw_scale: float, window_size: tuple[int, int], center: tuple[float, float]) -> Process:
    process = Process(objects = objects_list,
                      duration = process_time,
                      scale = draw_scale,
                      background = set_background(window_size),
                      center_point = center,
                      description = 'one ball hitting a wall according to laws of energy and impulse conservation',
                      update = conserv_update_func)
    return process