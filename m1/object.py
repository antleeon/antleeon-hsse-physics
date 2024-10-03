class Object:
    # constants
    STARTING_SPEED = (10, 0)
    POSITION = (3, 3)
    # constants

    def __init__(self, image, position = POSITION, speed = STARTING_SPEED) -> None:
        self.image = image
        self.position = position
        self.speed = speed

