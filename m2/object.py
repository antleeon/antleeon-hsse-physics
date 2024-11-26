class Object:
    # constants
    STARTING_SPEED = (10, 0)
    POSITION = (0, 0)
    SIZE = (1, 1)
    MASS = 1
    TRACE_COLOR = (0, 0, 0)
    IMPULSE_DEBT = (0, 0)
    SHAPE = 'ball'
    MOVABLE = True
    # constants

    def __init__(self, image, **kwargs) -> None:
        self.image = image
        self.size = kwargs.get('size', self.SIZE)
        self.position = kwargs.get('position', self.POSITION)
        self.speed = kwargs.get('speed', self.STARTING_SPEED)
        self.mass = kwargs.get('mass', self.MASS)
        if ('radius' in kwargs.keys()):
            self.radius = kwargs['radius']
            self.size = (self.radius * 2, self.radius * 2)
        self.trace_color = kwargs.get('trace_color', self.TRACE_COLOR)
        self.impulse_debt = kwargs.get('impulse_debt', self.IMPULSE_DEBT)
        self.shape = kwargs.get('shape', self.SHAPE)
        self.movable = kwargs.get('movable', self.MOVABLE)