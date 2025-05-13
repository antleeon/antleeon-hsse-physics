import math

def to_radians(angle):
    return (angle * math.pi / 180)

def to_degrees(angle):
    return (angle * 180 / math.pi)

def vector_to_standard(vector):
    length, angle = vector
    angle += (180 * (length < 0))
    angle = (((angle + 180) % 360) - 180)
    length = abs(length)
    return (length, angle)

def vect_to_coord(vector):
    length, angle = vector
    x = length * math.cos(to_radians(angle))
    y = length * math.sin(to_radians(angle))
    return (x, y)

def coord_to_vect(coordinates):
    x, y = coordinates
    length = ((x ** 2) + (y ** 2)) ** 0.5
    angle = to_degrees(math.atan2(y, x))
    return vector_to_standard((length, angle))

def sum_vectors(vectors):
    x, y = 0, 0
    for v in vectors:
        x_shift, y_shift = vect_to_coord(v)
        x += x_shift
        y += y_shift
    return vector_to_standard(coord_to_vect((x, y)))

def projection(vector, onto):
    _, angle = onto
    or_len, or_ang = vector
    length = or_len * math.cos(to_radians(angle - or_ang))
    return vector_to_standard((length, angle))

def projection_codirectional(vector, onto):
    _, angle = vector_to_standard(onto)
    or_len, or_ang = vector
    length = or_len * math.cos(to_radians(angle - or_ang))
    return (length, angle)

def perpendicular(vector):
    length, angle = vector
    angle += 90
    return vector_to_standard((length, angle))

def move_point_by_vector(coordinates, vector):
    point_as_vector = coord_to_vect(coordinates)
    result_as_vector = sum_vectors([point_as_vector, vector])
    result_as_point = vect_to_coord(result_as_vector)
    return result_as_point

def vector_times(vector, scalar):
    length, angle = vector
    new_length = scalar * length
    return vector_to_standard((new_length, angle))

def circle_length(radius):
    return (2 * radius * math.pi)