import constants as const
import some_math
import math

class Process:

    # default values
    def UPDATE(self):
        return
    
    CENTER_POINT = (0, 0)
    SCALE = 1
    OBJECTS = list()
    BACKGROUND = None
    DESCRIPTION = None
    DURATION = None
    # default values

    def __init__(self, **kwargs) -> None:
        self.description = kwargs.get('description', self.DESCRIPTION)
        self.objects = kwargs.get('objects', self.OBJECTS)
        self.update = __import__('types').MethodType(kwargs.get('update', self.UPDATE), self)
        self.background = kwargs.get('background', self.BACKGROUND)
        self.scale = kwargs.get('scale', self.SCALE)
        self.center_point = kwargs.get('center_point', self.CENTER_POINT)
        self.duration = kwargs.get('duration', self.DURATION)
        self.process_state = -1
        self.transform = __import__('pygame').transform
        self.result_data = None

        if (not (self.background is None)):
            self.display = __import__('pygame').Surface(self.background.get_size(), __import__('pygame').SRCALPHA)
            self.trace_screen = self.display.copy()
            self.trace_screen.fill((0, 0, 0, 0))

    def point_to_pixel(self, point):
        screen_w, screen_h = self.display.get_size()
        center_x, center_y = screen_w / 2, screen_h / 2
        x_abs, y_abs = point
        center_x_abs, center_y_abs = self.center_point
        pix_x = center_x + ((x_abs - center_x_abs) * self.scale)
        pix_y = center_y - ((y_abs - center_y_abs) * self.scale)
        return (pix_x, pix_y)

    def get_image_size(self, obj_size):
        obj_w, obj_h = obj_size
        try_img_w, try_img_h = obj_w * self.scale, obj_h * self.scale
        img_w, img_h = try_img_w, try_img_h

        max_size = const.MAX_DRAWN_RADIUS * 2
        min_size = const.MIN_DRAWN_RADIUS * 2

        if (try_img_w > max_size) :
            img_w = max_size
            img_h = try_img_h * img_w / try_img_w
        elif (try_img_w < min_size) :
            img_w = min_size
            img_h = try_img_h * img_w / try_img_w

        if (try_img_h > max_size) :
            img_h = max_size
            img_w = try_img_w * img_h / try_img_h
        elif (try_img_h < min_size) :
            img_h = min_size
            img_w = try_img_w * img_h / try_img_h

        rescale = img_w / try_img_w
        obj_w, obj_h = obj_w * rescale, obj_h * rescale

        return ((obj_w, obj_h), (img_w, img_h))
    
    def redraw(self, screen) -> None:
        self.display.fill((0, 0, 0, 0))
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.trace_screen, (0, 0))
        for obj in self.objects:
            obj_x, obj_y = obj.position
            obj_size, image_size = self.get_image_size(obj.size)
            obj_w, obj_h = obj_size
            tilt_angle = obj.tilt_angle
            attachment = obj.attachment_point
            image_w, image_h = image_size

            image_scaled = self.transform.scale(obj.image, (image_w, image_h))
            image_tilted = self.transform.rotate(image_scaled, tilt_angle)

            sin, cos = abs(math.sin(some_math.to_radians(tilt_angle))), abs(math.cos(some_math.to_radians(tilt_angle)))
            new_w, new_h = (obj_w * cos) + (obj_h * sin), (obj_h * cos) + (obj_w * sin)

            pix_x, pix_y = self.point_to_pixel(((obj_x - (new_w / 2)), (obj_y + (new_h / 2))))
            attach_cent_pix = self.point_to_pixel(attachment)
            attach_obj_pix = self.point_to_pixel((obj_x, obj_y))
            
            thr_col_no_alpha = const.THREAD_COLOR
            thr_col_opacity = const.DRAWING_OPACITY
            thr_col = (thr_col_no_alpha[0], thr_col_no_alpha[1], thr_col_no_alpha[2], thr_col_opacity)
            thr_line_w = const.THREAD_LINE_WIDTH

            __import__('pygame').draw.line(self.display, thr_col, attach_obj_pix, attach_cent_pix, thr_line_w)
            self.display.blit(image_tilted, (pix_x, pix_y))
        screen.blit(self.transform.scale(self.display, screen.get_size()), (0, 0))

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

    def describe(self) -> None:
        print(self.description)