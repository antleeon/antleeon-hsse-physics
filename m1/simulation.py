class Simulation:
    # constants
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    UPDATE_INTERVAL = 30
    SIMULATION_NAME = 'Simulation'
    DRAW_SCALE = 30
    # constants
    def __init__(self, process, window_dimensions = (WINDOW_WIDTH, WINDOW_HEIGHT), update_interval = UPDATE_INTERVAL, window_name = SIMULATION_NAME, draw_scale = DRAW_SCALE) -> None:
        self.process = process
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
    
    def update_process(self) -> None:
        self.process.update(self.update_interval)
        self.process.redraw(self.screen, self.draw_scale)
        self.reset_update_interval()
    
    def run_process(self) -> None:
        while True:
            events_list = self.pg.event.get()
            for event in events_list:
                if (not self.consider_event(event)):
                    self.pg.quit()
                    return
            self.pg.time.delay(self.update_interval)
            self.update_process()
            self.pg.display.update()