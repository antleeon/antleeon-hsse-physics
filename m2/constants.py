# objects
RADIUS1 = 0.05 # meters
RADIUS2 = 0.05 # meters
MASS1 = 0.3 # kilograms
MASS2 = 0.3 # kilograms
COLOR1 = (255, 0, 0) # RGB, no alpha
COLOR2 = (0, 255, 0) # RGB, no alpha
# objects

# starting conditions
X1, Y1 = -5, 0 # meters (in relation to abstract coordinate center)
X2, Y2 = 5, 0 # meters (in relation to abstract coordinate center)
SPEED1_ABS = 3 # meters per second
SPEED2_ABS = 3 # meters per second
COLLISION_ANGLE = 180 # degrees
# starting conditions

# technical settings
DRAWING_OPACITY = 255 # color opacity as an alpha channel value in RGBA format
TRACE_SEGMENT_LENGTH = 0.6 # length of stroke length in relation to whole segment's length when grawing trace (between 0 and 1)
TRACE_LINE_WIDTH = 3 # width of the trace line in pixels
OPTIMAL_SIMULATION_TIME = 5 # seconds
SCREEN_PADDING = 30 # pixels
MIN_DRAWN_RADIUS = 10 # pixels
MAX_DRAWN_RADIUS = 100 # pixels
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