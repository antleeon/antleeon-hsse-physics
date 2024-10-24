# object
RADIUS = 0.05 # meters
MASS = 0.3 # kilograms
DRAG_COEFFICIENT = 0.47
# object

# starting conditions
SPEED = (3, 60) # meters per second, degrees
HEIGHT = 0.3 # meters (meaning the position of the objects center in relation to its lowest position)
X_0 = -0.45 # meters (in relation to abstract coordinate center)
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
SCREEN_PADDING = 0.05 # respectful dimension percentage
MIN_DRAWN_RADIUS = 5 # pixels
MAX_DRAWN_RADIUS = 100 # pixels
# technical settings