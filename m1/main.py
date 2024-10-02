class Simulation:
    # constants
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    SIMULATION_FPS = 40
    SIMULATION_NAME = 'Simulation'
    # constants
    def __init__(self, window_dimensions = (WINDOW_WIDTH, WINDOW_HEIGHT), fps = SIMULATION_FPS, window_name = SIMULATION_NAME) -> None:
        self.pg = __import__('pygame')
        self.pg.init()
        self.pg.display.set_mode(window_dimensions)
        self.pg.display.set_caption(window_name)
        self.fps = fps
        self.clock = self.pg.time.Clock()

    def consider_event(self, event) -> bool:
        return (event.type != self.pg.QUIT)
    
    def update_process(self) -> None:
        self.pg.display.update()
    
    def run_process(self) -> None:
        while True:
            events_list = self.pg.event.get()
            for event in events_list:
                if (not self.consider_event(event)):
                    self.pg.quit()
                    return
            self.clock.tick(self.fps)
            self.update_process()
                
if (__name__ == '__main__'):
    simulation = Simulation()
    simulation.run_process()