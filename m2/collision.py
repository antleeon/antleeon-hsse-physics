from object import Object
from process import Process
import pygame as pg
import math as m
import some_math as sm
import constants as const
import theory_calculations as calc
from time_management import now_milliseconds_since_month as timestamp

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
    objects.append(Object(image1, radius = const.RADIUS1,
                                  position = (const.X1, const.Y1),
                                  speed = speed1,
                                  mass = const.MASS1,
                                  trace_color = const.COLOR1))
    
    image2 = pg.Surface((100, 100), pg.SRCALPHA)
    color2 = (const.COLOR2[0], const.COLOR2[1], const.COLOR2[2], const.DRAWING_OPACITY)
    pg.draw.circle(image2, color2, (50, 50), 50)
    objects.append(Object(image2, radius = const.RADIUS2,
                                  position = (const.X2, const.Y2),
                                  speed = speed2,
                                  mass = const.MASS2,
                                  trace_color = const.COLOR2))

    return objects

def set_process_two_balls_impulse(objects_list: list[Object], process_time: float, draw_scale: float, window_size: tuple[int, int], center: tuple[float, float]) -> Process:
    process = Process(objects = objects_list,
                      duration = process_time,
                      scale = draw_scale,
                      background = set_background(window_size),
                      center_point = center,
                      description = 'two balls colliding with constant impulse',
                      update = two_balls_impulse_update)