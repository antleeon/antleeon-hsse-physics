class Process:
    def __init__(self, objects, update, background) -> None:
        self.objects = objects
        self.update = update
        self.background = background
        self.display = __import__('pygame').Surface(background.get_size())
        self.resize = __import__('pygame').transform.scale
    
    def redraw(self, screen, scale = 1) -> None:
        self.display.blit(self.background, (0,0))
        for obj in self.objects:
            obj_x, obj_y = obj.position
            sprite_w, sprite_h = obj.image.get_size()
            pix_x = (obj_x * scale) - (sprite_w / 2)
            pix_y = (obj_y * scale) - (sprite_h / 2)
            self.display.blit(obj.image, (pix_x, pix_y))
        screen.blit(self.resize(self.display, screen.get_size()), (0,0))