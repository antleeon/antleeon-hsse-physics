class Object:
    # constants
    STARTING_SPEED = (0.1, 0)
    POSITION = (0.1, 0.1)
    # constants

    def __init__(self, image, position = POSITION, speed = STARTING_SPEED) -> None:
        self.image = image
        self.position = position
        self.speed = speed

