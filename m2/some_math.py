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

def vector_diff(vector1: tuple[float, float], vector2: tuple[float, float]) -> tuple[float, float]:
    minus_vector2 = vector_times(vector2, -1)
    result_vector = sum_vectors([vector1, minus_vector2])
    return result_vector

def vector_from_point_to_point(start_point: tuple[float, float], end_point: tuple[float, float]) -> tuple[float, float]:
    start_vector = coord_to_vect(start_point)
    end_vector = coord_to_vect(end_point)
    result_vector = vector_diff(end_vector, start_vector)
    return result_vector

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

def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    x1, y1 = point1
    x2, y2 = point2
    dist = (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5
    return dist

def is_inside_circle(point: tuple[float, float], circle: tuple[tuple[float, float], float]) -> bool:
    center, radius = circle
    dist = distance(point, center)
    return (dist < radius)

# TODO: def is_inside_triangle(point: tuple[float, float], triangle: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]) -> bool:

def is_inside_rectangle(point: tuple[float, float], rectangle: tuple[tuple[float, float], tuple[float, float]]) -> bool:
    x, y = point    
    center, size = rectangle
    x_c, y_c = center
    w, h = size
    inside_hor = abs(x - x_c) <= (w / 2)
    inside_vert = abs(y - y_c) <= (h / 2)
    return (inside_hor and inside_vert)
