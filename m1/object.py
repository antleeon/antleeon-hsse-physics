class Object:
    # constants
    STARTING_SPEED = (10, 0)
    POSITION = (0, 0)
    SIZE = (1, 1)
    # constants

    def __init__(self, image, size = SIZE, position = POSITION, speed = STARTING_SPEED) -> None:
        self.image = image
        self.size = size
        self.position = position
        self.speed = speed

