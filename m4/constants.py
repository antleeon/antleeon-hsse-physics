# object
RADIUS = 0.05 # meters
MASS = 0.3 # kilograms
DRAG_COEFFICIENT = 0.47 # depends on the shape
THREAD_LENGTH = 0.7 # meters
# object

# starting conditions
ANGULAR_VELOCITY = 10 # degrees per second
ANGLE = 30 # degrees (starting position)
X, Y = 0, 0 # meters (in relation to abstract coordinate center)
# starting conditions

# environment conditions
ENVIRONMENT_CONDITIONS = {
  'Earth, air': {
    'kinematic viscosity': 1.47 * (10 ** (-5)),
    'density': 1.225,
    'gravitational acceleration': (9.8, -90)
  },
  'Earth, water': {
    'kinematic viscosity': 8.9 * (10 ** (-7)),
    'density': 1000,
    'gravitational acceleration': (9.8, -90)
  },
  'Mars, atmosphere': {
    'kinematic viscosity': 10 ** (-3),
    'density': 1.5 * (-2),
    'gravitational acceleration': (3.7, -90)
  }
}
# environment conditions

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