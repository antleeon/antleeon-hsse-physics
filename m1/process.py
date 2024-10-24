import constants as const
import some_math

class Process:
    def __init__(self, objects, update, background, scale = 1, info = '') -> None:
        self.info = info
        self.objects = objects
        self.update = __import__('types').MethodType(update, self)
        self.background = background
        self.display = __import__('pygame').Surface(background.get_size(), __import__('pygame').SRCALPHA)
        self.trace_screen = self.display.copy()
        self.trace_screen.fill((0, 0, 0, 0))
        self.resize = __import__('pygame').transform.scale
        self.process_state = -1
        self.scale = scale

    def point_to_pixel(self, point):
        screen_w, screen_h = self.display.get_size()
        center_x, center_y = screen_w / 2, screen_h / 2
        pix_x = center_x + (point[0] * self.scale)
        pix_y = center_y - (point[1] * self.scale)
        return (pix_x, pix_y)

    def redraw(self, screen) -> None:
        self.display.fill((0, 0, 0, 0))
        self.display.blit(self.background, (0,0))
        self.display.blit(self.trace_screen, (0, 0))
        for obj in self.objects:
            obj_x, obj_y = obj.position
            obj_w, obj_h = obj.size
            image_w, image_h = obj_w * self.scale, obj_h * self.scale
            image_scaled = self.resize(obj.image, (image_w, image_h))

            pix_x, pix_y = self.point_to_pixel(((obj_x - (obj_w / 2)), (obj_y + (obj_h / 2))))

            self.display.blit(image_scaled, (pix_x, pix_y))
        screen.blit(self.resize(self.display, screen.get_size()), (0,0))

    def add_trace_segment(self, point1, point2, color_no_alpha):
        real_color = (color_no_alpha[0], color_no_alpha[1], color_no_alpha[2], const.DRAWING_OPACITY)
        
        radius_vector1 = some_math.coord_to_vect(point1)
        radius_vector2 = some_math.coord_to_vect(point2)
        vector = some_math.sum_vectors([some_math.vector_times(radius_vector1, -1), radius_vector2])
        side_spacing_length = vector[0] * ((1 - const.TRACE_SEGMENT_LENGTH) / 2)

        begin_point = some_math.move_point_by_vector(point1, (side_spacing_length, vector[1]))
        end_point = some_math.move_point_by_vector(point2, (side_spacing_length, (some_math.vector_times(vector, -1))[1]))

        begin_pix = self.point_to_pixel(begin_point)
        end_pix = self.point_to_pixel(end_point)

        __import__('pygame').draw.line(self.trace_screen, real_color, begin_pix, end_pix, const.TRACE_LINE_WIDTH)