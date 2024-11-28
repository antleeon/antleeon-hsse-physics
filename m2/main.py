from simulation import Simulation
import collision
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
def two_balls_conserv_sim_setter() -> Simulation:
    const.DRAWING_OPACITY = 255

    res = calc.get_speeds_and_time()
    window_size, draw_scale, center_point = get_screen_settings(res['boundaries'])
    simulation_time_scale = res['process time'] / const.OPTIMAL_SIMULATION_TIME

    objects = collision.set_objects_two_balls(res['speed1'], res['speed2'])
    process = collision.set_process_two_balls_conserv(objects, res['process time'], draw_scale, window_size, center_point)
    simulation = Simulation([process], time_scale = simulation_time_scale,
                                       window_dimensions = window_size)

    return simulation

def one_ball_conserv_sim_setter() -> Simulation:
    const.DRAWING_OPACITY = 255

    res = calc.get_speed_and_time()
    window_size, draw_scale, center_point = get_screen_settings(res['boundaries'])
    simulation_time_scale = res['process time'] / const.OPTIMAL_SIMULATION_TIME

    objects = collision.set_objects_one_ball(res['speed'])
    process = collision.set_process_one_ball_conserv(objects, res['process time'], draw_scale, window_size, center_point)
    simulation = Simulation([process], time_scale = simulation_time_scale,
                                       window_dimensions = window_size)

    return simulation

simulation_setters = {'two balls, conservation': two_balls_conserv_sim_setter,
                      'one ball, conservation': one_ball_conserv_sim_setter}

def set_simulation(option: str) -> Simulation:
    sim_setter = simulation_setters.get(option, two_balls_conserv_sim_setter)
    return sim_setter()
# simulation generators

if (__name__ == '__main__'):
    # choose option:
    simulation = set_simulation('two balls, conservation')
    #simulation = set_simulation('one ball, conservation')
    
    simulation.run_processes()