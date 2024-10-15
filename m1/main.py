from simulation import Simulation
import throwing_ball
from process import Process

# different setups
def update_function_linear_movement_linear_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'linear', 'linear')

def update_function_linear_movement_quadratic_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'linear', 'quadratic')

def update_function_curved_movement_linear_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'curved', 'linear')

def update_function_curved_movement_quadratic_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'curved', 'quadratic')
# different setups

def set_process():
    return [Process(throwing_ball.set_objects(), update_function_linear_movement_linear_resistance, throwing_ball.set_background()),
            Process(throwing_ball.set_objects(), update_function_linear_movement_quadratic_resistance, throwing_ball.set_background()),
            Process(throwing_ball.set_objects(), update_function_curved_movement_linear_resistance, throwing_ball.set_background()),
            Process(throwing_ball.set_objects(), update_function_curved_movement_quadratic_resistance, throwing_ball.set_background())]
                
if (__name__ == '__main__'):
    process = set_process()
    simulation = Simulation(process)
    simulation.run_processes()