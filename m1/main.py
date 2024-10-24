from simulation import Simulation
import throwing_ball
from process import Process
import theory_calculations as calc
import output
import constants as const

# different setups
def update_function_linear_movement_linear_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'linear', 'linear')

def update_function_linear_movement_quadratic_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'linear', 'quadratic')

def update_function_curved_movement_linear_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'curved', 'linear')

def update_function_curved_movement_quadratic_resistance(self, passed_time):
    return throwing_ball.update_function(self, passed_time, 'curved', 'quadratic')

def theory_trace_update_function(self, passed_time):
    return throwing_ball.theory_trace(self)
# different setups

def set_processes(draw_scale, screen_size, center_point = (0, 0)):
    processes = list()
    
    processes.append(Process(throwing_ball.set_objects((255, 0, 0)), update_function_linear_movement_linear_resistance, throwing_ball.set_background(screen_size), center_point, draw_scale, 'linear movement, linear resistance (red)'))
    processes.append(Process(throwing_ball.set_objects((0, 255, 0)), update_function_linear_movement_quadratic_resistance, throwing_ball.set_background(screen_size), center_point, draw_scale, 'linear movement, quadratic resistance (green)'))
    #processes.append(Process(throwing_ball.set_objects((0, 0, 255)), update_function_curved_movement_linear_resistance, throwing_ball.set_background(screen_size), center_point, draw_scale, 'curved movement, linear resistance (blue)'))
    #processes.append(Process(throwing_ball.set_objects((255, 255, 0)), update_function_curved_movement_quadratic_resistance, throwing_ball.set_background(screen_size), center_point, draw_scale, 'curved movement, quadratic resistance (yellow)'))
    
    processes.append(Process([], theory_trace_update_function, throwing_ball.set_background(screen_size), center_point, draw_scale, 'theoreticaly calculated trajectory (black)'))
    
    return processes
                
def get_screen_settings(boundaries):
    obj_w, obj_h = (2 * const.RADIUS), (2 * const.RADIUS)
    max_width, max_height = (const.MAX_SCREEN_WIDTH - (2 * const.SCREEN_PADDING)), (const.MAX_SCREEN_HEIGHT - (2 * const.SCREEN_PADDING))
    min_point, max_point = boundaries
    min_x, min_y = min_point
    max_x, max_y = max_point
    padding = const.SCREEN_PADDING
    
    center_point = ((min_x + ((max_x - min_x) / 2)), (min_y + ((max_y - min_y) / 2)))
    abs_width, abs_height = (obj_w + max_x - min_x), (obj_h + max_y - min_y)
    scale = min((max_width / abs_width), (max_height / abs_height))
    width, height = ((abs_width * scale) + (2 * const.SCREEN_PADDING)), ((abs_height * scale) + (2 * const.SCREEN_PADDING))
    width, height = max(width, const.MIN_SCREEN_WIDTH), max(height, const.MIN_SCREEN_HEIGHT)

    return ((width, height), scale, center_point)

if (__name__ == '__main__'):
    calculated = calc.count('linear')
    output.print_result('Calculated with linear air resistance:', calculated)
    
    theory_time = calculated[0]
    trace_coordinates, boundaries = calc.count_trace('linear', theory_time)

    simulation_time_scale = theory_time / const.OPTIMAL_SIMULATION_TIME
    window_size, draw_scale, center_point = get_screen_settings(boundaries)

    processes = set_processes(draw_scale, window_size, center_point)
    simulation = Simulation(processes, time_scale = simulation_time_scale,
                                       window_dimensions = window_size)
    simulation.run_processes()