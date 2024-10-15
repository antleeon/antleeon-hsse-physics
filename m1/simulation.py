class Simulation:
    # constants
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 800

    DEFAULT_UPDATE_INTERVAL = 50
    MIN_INTERVAL = 5
    TIME_SCALE = 0.2

    APPROXIMATION = 0.01

    SIMULATION_NAME = 'Simulation'
    DRAW_SCALE = 800
    # constants
    def __init__(self, processes, **kwargs) -> None:
        self.processes = processes
        self.pg = __import__('pygame')
        self.pg.init()
        self.screen = self.pg.display.set_mode(kwargs.get('window_dimensions', (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)), self.pg.DOUBLEBUF)
        self.pg.display.set_caption(kwargs.get('window_name', self.SIMULATION_NAME))
        self.reset_update_interval()
        self.time_scale = kwargs.get('time_scale', self.TIME_SCALE)
        self.draw_scale = kwargs.get('draw_scale', self.DRAW_SCALE)
        self.approximation = kwargs.get('approximation', self.APPROXIMATION)

    def consider_event(self, event) -> bool:
        return (event.type != self.pg.QUIT)
    
    def reset_update_interval(self) -> None:
        def count_time_interval(object):
            accel = getattr(object, 'last_acceleration', (0, 0))
            speed = getattr(object, 'speed', (0, 0))
            accel_proj = __import__('some_math').projection(accel, speed)
            sp_abs = abs(speed[0])
            ac_abs = abs(accel_proj[0])
            if not ((sp_abs > 0) and (ac_abs > 0) and (self.approximation > 0)):
                return self.DEFAULT_UPDATE_INTERVAL
            return (((self.approximation * sp_abs / ac_abs) * 1000) / self.time_scale)

        interval = self.DEFAULT_UPDATE_INTERVAL
        for process in self.processes:
            for object in process.objects:
                interval = min(count_time_interval(object), interval)
        self.update_interval = max(int(interval), self.MIN_INTERVAL)

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
            process.update(self.update_interval * self.time_scale)
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