from simulation import Simulation
import pendulum
import theory_calculations as calc
import constants as const

# auto window sizing
def get_screen_settings(boundaries):
    max_width, max_height = (const.MAX_SCREEN_WIDTH - (2 * const.SCREEN_PADDING)), (const.MAX_SCREEN_HEIGHT - (2 * const.SCREEN_PADDING))
    min_point, max_point = boundaries
    min_x, min_y = min_point
    max_x, max_y = max_point
    padding = const.SCREEN_PADDING
    
    center_point = ((min_x + ((max_x - min_x) / 2)), (min_y + ((max_y - min_y) / 2)))
    abs_width, abs_height = (max_x - min_x), (max_y - min_y)
    scale = min((max_width / abs_width), (max_height / abs_height))
    width, height = ((abs_width * scale) + (2 * padding)), ((abs_height * scale) + (2 * padding))
    width, height = max(width, const.MIN_SCREEN_WIDTH), max(height, const.MIN_SCREEN_HEIGHT)

    return ((width, height), scale, center_point)
# auto window sizing

# simulation generators
def set_simulation(environment_option: str, object_option: str) -> Simulation:
    res = calc.count(environment_option, object_option)
    
    boundaries = res['boundaries']
    period = res['period']
    attachment = res['attachment']
    speed = res['speed']
    max_speed_abs = res['maximum speed module']
    amplitude = res['amplitude']
    
    window_size, draw_scale, center_point = get_screen_settings(boundaries)
    simulation_time_scale = period / const.OPTIMAL_SIMULATION_TIME
    process_info = f"Process information:\n  period: {period} s\n  maximum speed: {max_speed_abs} m/s\n  amplitude: {amplitude} m"

    object = pendulum.set_object(object_option, speed)
    process = pendulum.set_process(environment_option, [object], draw_scale, window_size, center_point, attachment, process_info)
    simulation = Simulation([process], time_scale = simulation_time_scale,
                                       window_dimensions = window_size)

    return simulation
# simulation generators

if (__name__ == '__main__'):
    # choose option:
    simulation = set_simulation('Earth, air', 'ball')
    #simulation = set_simulation('Earth, air', 'brick')
    #simulation = set_simulation('Earth, water', 'ball')
    #simulation = set_simulation('Mars, atmosphere', 'ball')
    
    simulation.run_processes()