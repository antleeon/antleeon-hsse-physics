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
def earth_air_sim_setter() -> Simulation:
    res = calc.count()
    boundaries = res['boundaries']
    period = res['period']
    attachment = res['attachment']
    speed = res['speed']
    
    window_size, draw_scale, center_point = get_screen_settings(boundaries)
    simulation_time_scale = period / const.OPTIMAL_SIMULATION_TIME

    object = pendulum.set_object_ball(speed)
    process = pendulum.set_process_earth_air([object], draw_scale, window_size, center_point, attachment)
    simulation = Simulation([process], time_scale = simulation_time_scale,
                                       window_dimensions = window_size)

    return simulation

def earth_water_sim_setter():
    return

def mars_atmosphere_sim_setter():
    return
# simulation generators

simulation_setters = {'Earth, air': earth_air_sim_setter,
                      'Earth, water': earth_water_sim_setter,
                      'Mars, atmosphere': mars_atmosphere_sim_setter}

def set_simulation(option: str) -> Simulation:
    sim_setter = simulation_setters.get(option, earth_air_sim_setter)
    return sim_setter()

if (__name__ == '__main__'):
    # choose option:
    simulation = set_simulation('Earth, air')
    #simulation = set_simulation('Earth, water')
    #simulation = set_simulation('Mars, atmosphere')
    
    simulation.run_processes()