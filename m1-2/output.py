from object import Object

def print_object(object: Object, message: str = None):
  if (message):
    print(message)

  print('  object:')
  x, y = object.position
  print('    coordinates:', f'{x:.2f}', 'm (hor),', f'{y:.2f}', 'm (vert)')
  speed_abs, speed_ang = object.speed
  print('    speed:', f'{speed_abs:.2f}', 'm/s', 'at', f'{speed_ang:.2f}', 'degrees')
  kinetic_energy = 0.5 * object.mass * (speed_abs ** 2)
  print('    kinetic energy:', f'{kinetic_energy:.2f}', 'J')
  impulse = object.mass * speed_abs
  print('    impulse:', f'{impulse:.2f}', 'N*s')

def print_process_result(process_data: dict, message: str = None):
  if (message):
    print(message)

  print('  process:')
  for key, value in process_data.items():
    print('    ', key, ': ', value, sep = '')