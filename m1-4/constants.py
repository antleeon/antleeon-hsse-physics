# object
OBJECTS = {
  'ball': {
    'shape': 'sphere', # 3D shape
    'drag coefficient': 0.47, # depends on the shape
    'radius': 0.05, # meters
    'mass': 0.3, # kilograms
    'color': (255, 0, 0) # RGB color
  },
  'brick': {
    'shape': 'parallelogram', # 3D shape
    'drag coefficient': 1.05, # depends on the shape
    'size': (0.1, 0.13), # meters * meters
    'mass': 0.5, # kilograms
    'color': (0, 200, 50) # RGB color
  },
  'baloon': {
    'shape': 'sphere', # 3D shape
    'drag coefficient': 0.47, # depends on the shape
    'radius': 0.1, # meters
    'mass': 0.005, # kilograms
    'color': (255, 100, 200) # RGB color
  }
}
THREAD_LENGTH = 0.7 # meters
THREAD_COLOR = (100, 100, 0) # RGB color
THREAD_LINE_WIDTH = 4 # pixels
# object

# starting conditions
ANGULAR_VELOCITY = 25 # degrees per second
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
WITH_ENVIRONMENTAL_RESISTANCE = False
WITH_ARCHIMEDES_FORCE = True
# environment conditions

# technical settings
DRAWING_OPACITY = 255 # color opacity as an alpha channel value in RGBA format
FADE_OPACITY = 2 # RGB alpha channel value for trace overpaint (e.i. speed of its fading out)
TRACE_SEGMENT_LENGTH = 0.1 # length of stroke length in relation to whole segment's length when grawing trace (between 0 and 1)
TRACE_LINE_WIDTH = 3 # width of the trace line in pixels
OPTIMAL_SIMULATION_TIME = 3 # seconds
SCREEN_PADDING = 30 # pixels
MIN_DRAWN_RADIUS = 10 # pixels
MAX_DRAWN_RADIUS = 100 # pixels
MAX_SCREEN_WIDTH = 1800 # pixels
MAX_SCREEN_HEIGHT = 1000 # pixels
MIN_SCREEN_WIDTH = 500 # pixels
MIN_SCREEN_HEIGHT = 500 # pixels
# technical settings