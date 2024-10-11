from simulation import Simulation
import throwing_ball
from process import Process

def set_process():
    return [Process(throwing_ball.set_objects(), throwing_ball.update_function_line, throwing_ball.set_background()),
            Process(throwing_ball.set_objects(), throwing_ball.update_function_curve, throwing_ball.set_background())]
                
if (__name__ == '__main__'):
    process = set_process()
    simulation = Simulation(process)
    simulation.run_processes()