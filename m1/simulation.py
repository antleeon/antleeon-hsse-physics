class Simulation:
    # constants
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 800

    UPDATE_INTERVAL = 30
    SIMULATION_NAME = 'Simulation'
    DRAW_SCALE = 800
    # constants
    def __init__(self, processes, window_dimensions = (WINDOW_WIDTH, WINDOW_HEIGHT), update_interval = UPDATE_INTERVAL, window_name = SIMULATION_NAME, draw_scale = DRAW_SCALE) -> None:
        self.processes = processes
        self.pg = __import__('pygame')
        self.pg.init()
        self.screen = self.pg.display.set_mode(window_dimensions, self.pg.DOUBLEBUF)
        self.pg.display.set_caption(window_name)
        self.update_interval = update_interval
        self.draw_scale = draw_scale

    def consider_event(self, event) -> bool:
        return (event.type != self.pg.QUIT)
    
    def reset_update_interval(self) -> None:
        self.update_interval = self.update_interval

    def get_subscreen(self):
        quantity = len(self.processes)
        screen_width, screen_height = self.screen.get_size()

        width = screen_width // quantity
        height = screen_height

        subscreen = self.pg.Surface((width, height))
        return subscreen
    
    def get_subscreen_position(self, index):
        screen_width, screen_height = self.screen.get_size()
        width, height = self.get_subscreen().get_size()
        x = width * (index % (screen_width // width))
        y = height * (index // (screen_width // width))
        return (x, y)
    
    def update_processes(self) -> None:
        subscreen = self.get_subscreen()
        for i, process in enumerate(self.processes):
            process.update(self.update_interval)
            curr_subscreen = subscreen
            process.redraw(curr_subscreen, self.draw_scale)
            self.screen.blit(curr_subscreen, self.get_subscreen_position(i))
        self.reset_update_interval()
    
    def run_processes(self) -> None:
        while True:
            events_list = self.pg.event.get()
            for event in events_list:
                if (not self.consider_event(event)):
                    self.pg.quit()
                    return
            self.pg.time.delay(self.update_interval)
            self.update_processes()
            self.pg.display.update()