class Object:
    # constants
    STARTING_SPEED = (10, 0)
    POSITION = (0, 0)
    SIZE = (1, 1)
    MASS = 1
    TRACE_COLOR = (0, 0, 0)
    SHAPE = 'brick'
    SHAPE_RADIUS = 'ball'
    MOVABLE = True
    # constants

    def __init__(self, image, **kwargs) -> None:
        self.image = image
        self.size = kwargs.get('size', self.SIZE)
        self.position = kwargs.get('position', self.POSITION)
        self.speed = kwargs.get('speed', self.STARTING_SPEED)
        self.mass = kwargs.get('mass', self.MASS)
        self.shape = kwargs.get('shape', self.SHAPE)
        if ('radius' in kwargs.keys()):
            self.radius = kwargs['radius']
            self.size = (self.radius * 2, self.radius * 2)
            self.shape = kwargs.get('shape', self.SHAPE_RADIUS)
        self.trace_color = kwargs.get('trace_color', self.TRACE_COLOR)
        self.movable = kwargs.get('movable', self.MOVABLE)