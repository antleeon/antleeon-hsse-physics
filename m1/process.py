class Process:
    def __init__(self, objects, update, background) -> None:
        self.objects = objects
        self.update = __import__('types').MethodType(update, self)
        self.background = background
        self.display = __import__('pygame').Surface(background.get_size())
        self.resize = __import__('pygame').transform.scale
    
    def redraw(self, screen, scale = 1) -> None:
        self.display.blit(self.background, (0,0))
        for obj in self.objects:
            obj_x, obj_y = obj.position
            image_w, image_h = obj.image.get_size()
            pix_x = (obj_x * scale) - (image_w / 2)
            pix_y = (obj_y * scale) - (image_h / 2)
            self.display.blit(obj.image, (pix_x, pix_y))
        screen.blit(self.resize(self.display, screen.get_size()), (0,0))