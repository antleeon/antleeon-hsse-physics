class Process:
    def __init__(self, objects, update, background, info) -> None:
        self.info = info
        self.objects = objects
        self.update = __import__('types').MethodType(update, self)
        self.background = background
        self.display = __import__('pygame').Surface(background.get_size())
        self.resize = __import__('pygame').transform.scale
        self.process_state = -1
    
    def redraw(self, screen, scale = 1) -> None:
        self.display.blit(self.background, (0,0))
        for obj in self.objects:
            obj_x, obj_y = obj.position
            obj_w, obj_h = obj.size
            image_w, image_h = obj_w * scale, obj_h * scale
            image_scaled = self.resize(obj.image, (image_w, image_h))

            screen_w, screen_h = screen.get_size()
            center_x, center_y = screen_w / 2, screen_h / 2
            pix_x = center_x + (obj_x * scale) - (image_w / 2)
            pix_y = center_y - (obj_y * scale) + (image_h / 2)

            self.display.blit(image_scaled, (pix_x, pix_y))
        screen.blit(self.resize(self.display, screen.get_size()), (0,0))