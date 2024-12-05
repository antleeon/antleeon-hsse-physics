import output
import some_math as sm
import constants as const
from time_management import now_milliseconds_since_month as timestamp

class Simulation:
    # constants
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 1000

    DEFAULT_UPDATE_INTERVAL = 30
    MIN_INTERVAL = 5
    TIME_SCALE = 0.2

    APPROXIMATION = 0.001
    FRAMING_STEP = 0.05

    SIMULATION_NAME = 'Simulation'
    DRAW_SCALE = 1400
    # constants
    
    def __init__(self, processes, **kwargs) -> None:
        self.processes = processes
        self.pg = __import__('pygame')
        self.pg.init()
        self.screen = self.pg.display.set_mode(kwargs.get('window_dimensions', (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)), self.pg.DOUBLEBUF)
        self.pg.display.set_caption(kwargs.get('window_name', self.SIMULATION_NAME))
        self.time_scale = kwargs.get('time_scale', self.TIME_SCALE)
        self.approximation = kwargs.get('approximation', self.APPROXIMATION)
        self.reset_update_interval()

    def consider_event(self, event) -> bool:
        return (event.type != self.pg.QUIT)
    
    def reset_update_interval(self) -> None:
        def count_time_interval(obj1, obj2):
            v1, v2 = obj1.speed, obj2.speed
            pos1, pos2 = obj1.position, obj2.position
            axis = sm.vector_from_point_to_point(pos1, pos2)
            v1_pr, v2_pr = sm.projection_codirectional(v1, axis)[0], sm.projection_codirectional(v2, axis)[0]
            v_towards = v1_pr - v2_pr
            size1, size2 = obj1.size, obj2.size
            dim1, dim2 = ((size1[0] ** 2) + (size1[1] ** 2)) ** 0.5, ((size2[0] ** 2) + (size2[1] ** 2)) ** 0.5
            dist = max(sm.distance(pos1, pos2) - (dim1 + dim2), 0)

            if not (v_towards > 0):
                return self.DEFAULT_UPDATE_INTERVAL
            return ((((dist / v_towards) * self.FRAMING_STEP) * 1000) / self.time_scale)

        interval = self.DEFAULT_UPDATE_INTERVAL
        for process in self.processes:
            for i, object1 in enumerate(process.objects):
                for j, object2 in enumerate(process.objects):
                    if (i == j):
                        continue
                    interval = min(count_time_interval(object1, object2), interval)
        self.update_interval = max(int(interval), self.MIN_INTERVAL)

    def get_subscreen(self):
        quantity = len(self.processes)
        screen_width, screen_height = self.screen.get_size()

        #width = screen_width // quantity
        #height = screen_height TODO
        width = screen_width
        height = screen_height

        subscreen = self.pg.Surface((width, height), self.pg.SRCALPHA)
        subscreen.fill((0, 0, 0, 0))
        return subscreen
    
    def get_subscreen_position(self, index):
        screen_width, screen_height = self.screen.get_size()
        width, height = self.get_subscreen().get_size()
        x = width * (index % (screen_width // width))
        y = height * (index // (screen_width // width))
        #return(x, y)

        return (0, 0)
    
    def update_processes(self) -> None:
        self.screen.fill((255, 255, 255))
        subscreen = self.get_subscreen()
        for i, process in enumerate(self.processes):
            if (process.process_state != 1):
                update_time = timestamp()
                time_passed = update_time - process.last_updated
                trace_data = process.update(time_passed * self.time_scale / 1000)
                process.last_updated = update_time

                if (process.process_state == -1):
                    process.begin_time = update_time
                    process.process_state = 0
                elif ((process.process_state == 0) and (((update_time - process.begin_time) * self.time_scale / 1000) >= process.duration)):
                    process.end_time = update_time
                    process.process_state = 1

                for segment in trace_data:
                    process.add_trace_segment(segment[0], segment[1], segment[2])
            elif (not process.result_printed):
                description = process.description
                result_data = process.result_data
                output.print_process_result(result_data, f'Got with settings "{description}":')
                process.result_printed = True
                process.describe()
            curr_subscreen = subscreen.copy()
            process.redraw(curr_subscreen)
            self.screen.blit(curr_subscreen, self.get_subscreen_position(i))
        self.reset_update_interval()
    
    def run_processes(self) -> None:
        for process in self.processes:
            process.result_printed = False
            process.last_updated = timestamp()
            process.describe()
        
        while True:
            events_list = self.pg.event.get()
            for event in events_list:
                if (not self.consider_event(event)):
                    self.pg.quit()
                    return
            self.pg.time.delay(self.update_interval)
            self.update_processes()
            self.pg.display.update()