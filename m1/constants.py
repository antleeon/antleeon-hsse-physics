# object
RADIUS = 0.05 # meters
MASS = 0.3 # kilograms
DRAG_COEFFICIENT = 0.47
# object

# starting conditions
SPEED = (3, 60) # meters per second, degrees
Y_F = -0.3 # meters (meaning the position of the objects center in relation to its lowest position)
X_0, Y_0 = 0, 0 # meters (in relation to abstract coordinate center)
# starting conditions

# environment conditions
ENVIRONMENT_VISCOSITY = 1.78 * (10 ** (-5))
ENVIRONMENT_DENSITY = 1.225
GRAVITATIONAL_ACCELERATION = (9.8, -90) 
# environment conditions

# technical settings
DRAWING_OPACITY = 150 # color opacity as an alpha channel value in RGBA format
TRACE_SEGMENT_LENGTH = 0.6 # length of stroke length in relation to whole segment's length when grawing trace (between 0 and 1)
TRACE_LINE_WIDTH = 3 # width of the trace line in pixels
OPTIMAL_SIMULATION_TIME = 5 # seconds
SCREEN_PADDING = 0.2 # respectful dimension part
MIN_DRAWN_RADIUS = 10 # pixels
MAX_DRAWN_RADIUS = 100 # pixels
MAX_SCREEN_WIDTH = 1800 # pixels
MAX_SCREEN_HEIGHT = 1000 # pixels
# technical settings

# theoretical calculations settings
TIME_ACCURACY = 0.0001 # the prcision of time calculation (in seconds)
TIME_INTERVAL = (0, 10) # the interval, in which the calculations are made (in seconds)
TIME_POINTS_QUANTITY = 100 # the number of time stamps in the calculated interval, for which the further calculation would be made
# theoretical calculations settings