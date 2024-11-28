# objects
WALL_SIZE = (0.3, 1) # meters x meters (width x height)
RADIUS0 = 0.1 # meters
RADIUS1 = 0.1 # meters
RADIUS2 = 0.2 # meters
WALL_MASS = 10 # kilograms (absolutely useless)
MASS0 = 0.3 # kilograms
MASS1 = 0.3 # kilograms
MASS2 = 0.6 # kilograms
WALL_COLOR = (0, 0, 0) # RGB, no alpha
COLOR0 = (150, 0, 150) # RGB, no alpha
COLOR1 = (255, 0, 0) # RGB, no alpha
COLOR2 = (0, 255, 0) # RGB, no alpha
# objects

# starting conditions
WALL_X, WALL_Y = 1, 0 # meters
X0, Y0 = 0, 1 # meters
X1, Y1 = -0.5, 1 # meters (in relation to abstract coordinate center)
X2, Y2 = 0.5, -1 # meters (in relation to abstract coordinate center)
SPEED0_ABS = 3 # meters per second
SPEED1_ABS = 7 # meters per second
SPEED2_ABS = 3 # meters per second
COLLISION_ANGLE = 90 # degrees
ANGLE_APPROXIMATION = 10 # degrees
# starting conditions

# technical settings
DRAWING_OPACITY = 255 # color opacity as an alpha channel value in RGBA format
TRACE_SEGMENT_LENGTH = 0.6 # length of stroke length in relation to whole segment's length when grawing trace (between 0 and 1)
TRACE_LINE_WIDTH = 3 # width of the trace line in pixels
OPTIMAL_SIMULATION_TIME = 5 # seconds
SCREEN_PADDING = 70 # pixels
MIN_DRAWN_RADIUS = 10 # pixels
MAX_DRAWN_RADIUS = 500 # pixels
MAX_SCREEN_WIDTH = 1800 # pixels
MAX_SCREEN_HEIGHT = 1000 # pixels
MIN_SCREEN_WIDTH = 500 # pixels
MIN_SCREEN_HEIGHT = 500 # pixels
# technical settings

# theoretical calculations settings
TIME_ACCURACY = 0.0001 # the prcision of time calculation (in seconds)
TIME_INTERVAL = (0, 100) # the interval, in which the calculations are made (in seconds)
TIME_POINTS_QUANTITY = 100 # the number of time stamps in the calculated interval, for which the further calculation would be made
# theoretical calculations settings