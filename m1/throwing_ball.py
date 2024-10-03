from object import Object
import pygame as pg
import math

def set_objects():
    objects = list()
    image = pg.Surface((100, 100), pg.SRCALPHA)
    pg.draw.circle(image, (255, 0, 0, 255), (50, 50), 50)
    objects.append(Object(image, (1, 1), (-10, 0), (15, 60)))
    return objects

def set_background():
    background = pg.Surface((1200, 800))
    background.fill((255, 255, 255))
    return background

def update_function(self, passed_time):
    def to_radians(angle):
        return (angle * math.pi / 180)
    
    def to_degrees(angle):
        return (angle * 180 / math.pi)
    
    def vect_to_coord(vector):
        length, angle = vector
        x = length * math.cos(to_radians(angle))
        y = length * math.sin(to_radians(angle))
        return (x, y)

    def coord_to_vect(coordinates):
        x, y = coordinates
        length = ((x ** 2) + (y ** 2)) ** 0.5
        angle = to_degrees(math.atan2(y, x))
        return (length, angle)
    
    def sum_vectors(vectors):
        x, y = 0, 0
        for v in vectors:
            x_shift, y_shift = vect_to_coord(v)
            x += x_shift
            y += y_shift
        return (coord_to_vect((x, y)))
    
    def update_motion(coordinates, speed, acceleration, time):
        x, y = coordinates
        speed_x, speed_y = vect_to_coord(speed)
        accel_x, accel_y = vect_to_coord(acceleration)
        
        x += (speed_x * time) + (accel_x * (time ** 2) / 2)
        y -= (speed_y * time) + (accel_y * (time ** 2) / 2)
        speed_x += accel_x * time
        speed_y += accel_y * time

        return ((x, y), coord_to_vect((speed_x, speed_y)))

    accelerators = [(9.8, -90)]
    acceleration = sum_vectors(accelerators)
    sec_time = passed_time / 1000

    for obj in self.objects:
        obj.position, obj.speed = update_motion(obj.position, obj.speed, acceleration, sec_time)
