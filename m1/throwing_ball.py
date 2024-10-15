from object import Object
import pygame as pg
import math
import some_math

MIN_Y_POSITION = -0.15

def set_objects():
    objects = list()
    image = pg.Surface((100, 100), pg.SRCALPHA)
    pg.draw.circle(image, (255, 0, 0, 255), (50, 50), 50)
    objects.append(Object(image, (0.1, 0.1), (-0.5, 0), (3, 60)))
    return objects

def set_background():
    background = pg.Surface((800, 800))
    background.fill((255, 255, 255))
    return background

def update_function_line(self, passed_time):
    def update_motion(coordinates, speed, acceleration, time):
        new_speed = some_math.sum_vectors([speed, some_math.vector_times(acceleration, time)])
        average_speed = some_math.sum_vectors([some_math.vector_times(speed, 0.5), some_math.vector_times(new_speed, 0.5)])
        shift = some_math.vector_times(average_speed, time)
        new_coordinates = some_math.move_point_by_vector(coordinates, (shift[0], shift[1]))
        return (new_coordinates, new_speed)

    accelerators = [(9.8, -90)]
    acceleration = some_math.sum_vectors(accelerators)
    sec_time = passed_time / 1000

    for obj in self.objects:
        if ((obj.position)[1] > MIN_Y_POSITION):
            obj.position, obj.speed = update_motion(obj.position, obj.speed, acceleration, sec_time)
            obj.last_acceleration = acceleration
        else:
            obj.position = (obj.position[0], MIN_Y_POSITION)
            obj.last_acceleration = (0, 0)

def update_function_curve(self, passed_time):
    def update_motion(coordinates, speed, acceleration, time):
        accel_tang = some_math.projection(acceleration, speed)
        accel_norm = some_math.projection(acceleration, some_math.perpendicular(speed))
        moving_clockwise = (math.sin(some_math.to_radians(speed[1] - accel_norm[1])) > 0)
        angle_multyplier = (1 * (not moving_clockwise)) + (-1 * (moving_clockwise))
        radius = (speed[0] ** 2) / accel_norm[0]
        circle_center = some_math.move_point_by_vector(coordinates, (radius, accel_norm[1]))
        circle_len = some_math.circle_length(radius)
        curve_len = (speed[0] * time) + (accel_tang[0] * (time ** 2) * 0.5)
        curve_angle = 360 * (curve_len / circle_len)
        move_angle = curve_angle * angle_multyplier
        start_point_angle = (some_math.vector_times(accel_norm, -1))[1]
        end_point_angle = start_point_angle + move_angle
        new_coordinates = some_math.move_point_by_vector(circle_center, (radius, end_point_angle))
        # new_speed = (speed[0] + (accel_tang[0] * time), speed[1] + move_angle)
        new_speed = some_math.sum_vectors([speed, some_math.vector_times(acceleration, time)])
        return (new_coordinates, new_speed)

    accelerators = [(9.8, -90)]
    acceleration = some_math.sum_vectors(accelerators)
    sec_time = passed_time / 1000

    for obj in self.objects:
        if ((obj.position)[1] > MIN_Y_POSITION):
            obj.position, obj.speed = update_motion(obj.position, obj.speed, acceleration, sec_time)
            obj.last_acceleration = acceleration
        else:
            obj.position = (obj.position[0], MIN_Y_POSITION)
            obj.last_acceleration = (0, 0)
