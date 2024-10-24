from simulation import Simulation
import throwing_ball
from process import Process
import theory_calculations as calc
import output

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

def set_processes():
    return [Process(throwing_ball.set_objects((255, 0, 0)), update_function_linear_movement_linear_resistance, throwing_ball.set_background(), 1000, 'linear movement, linear resistance'),
            Process(throwing_ball.set_objects((0, 255, 0)), update_function_linear_movement_quadratic_resistance, throwing_ball.set_background(), 1000, 'linear movement, quadratic resistance'),
            Process(throwing_ball.set_objects((0, 0, 255)), update_function_curved_movement_linear_resistance, throwing_ball.set_background(), 1000, 'curved movement, linear resistance'),
            Process(throwing_ball.set_objects((255, 255, 0)), update_function_curved_movement_quadratic_resistance, throwing_ball.set_background(), 1000, 'curved movement, quadratic resistance')]
                
if (__name__ == '__main__'):
    calculated = calc.count('linear')
    output.print_result('Calculated with linear air resistance:', calculated)

    process = set_processes()
    simulation = Simulation(process)
    simulation.run_processes()