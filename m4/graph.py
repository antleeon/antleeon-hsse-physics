import constants as const
import math as m
import some_math as sm
import matplotlib.pyplot as plt
import theory_calculations as calc
import numpy as np
import pandas as pd
import seaborn as sns
import pendulum

from object import Object
from process import Process

ANGLE_INTERVAL = (0, 85)
POINTS_QUANTITY = 200
OBJECT_OPTION = 'ball'
ENVIRONMENT_OPTION = 'Earth, air'
PERCENT_STEP = 10

def process_points(x: list[float], y: list[float]) -> list[float]:
    return y

def find_real_period(res: dict) -> float:
    attachment = res['attachment']
    speed = res['speed']
    
    object = pendulum.set_object(OBJECT_OPTION, speed, attachment)
    process = pendulum.set_process(ENVIRONMENT_OPTION, [object], 1, (100, 100), (50, 50), f'')

    real_period = pendulum.get_real_period(process)

    return real_period

if (__name__ == '__main__'):
    angle_points = list()
    
    theory_points = list()
    real_points = list()
    harmonic_points = list()

    percent_done = 0

    for i in range(POINTS_QUANTITY):
        ang = ANGLE_INTERVAL[0] + (((ANGLE_INTERVAL[1] - ANGLE_INTERVAL[0]) / (POINTS_QUANTITY - 1)) * i)
        angle_points.append(abs(ang) * 2)
        const.ANGLE = ang
        #const.ANGULAR_VELOCITY = 0

        theory_res = calc.count(ENVIRONMENT_OPTION, OBJECT_OPTION, True)
        
        theory_period = theory_res['real period']
        real_period = find_real_period(theory_res)
        harmonic_period = theory_res['period']

        theory_points.append(theory_period)
        real_points.append(real_period)
        harmonic_points.append(harmonic_period)

        percent_done_new = ((i / POINTS_QUANTITY * 100) // PERCENT_STEP) * PERCENT_STEP
        if (percent_done_new > percent_done):
            print(f'{int(percent_done_new)}% of calculations complete...')
            percent_done = percent_done_new  

    print('Graph points calculated') # debug

    real_points = process_points(angle_points, real_points)
    theory_points = process_points(angle_points, theory_points)
    harmonic_points = process_points(angle_points, harmonic_points)
    plt.plot(angle_points, real_points)
    plt.plot(angle_points, theory_points)
    plt.plot(angle_points, harmonic_points)
    #plt.ylim(ymin = 0)
    plt.title('Period to amplitude relation')
    plt.xlabel('Angle amplitude, degrees')
    plt.ylabel('Period, seconds')
    plt.grid()
    plt.legend(['real', 'theoretical', 'harmonic'])
    plt.show()