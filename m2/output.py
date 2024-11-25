from object import Object

def print_object(object: Object, message: str = None):
  if (message):
    print(message)

  print('  object:')
  x, y = object.position
  print('    coordinates:', x, 'm (hor),', y, 'm (vert)')
  speed_abs, speed_ang = object.speed
  print('    speed:', speed_abs, 'm/s', 'at', speed_ang, 'degrees')
  kinetic_energy = 0.5 * object.mass * (speed_abs ** 2)
  print('    kinetic energy:', kinetic_energy, 'J')
  impulse = object.mass * speed_abs
  print('    impulse:', impulse, 'N*s')

def print_process_result(process_data, message: str = None):
  if (message):
    print(message)

  print('  process:')
  # something else