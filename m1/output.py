def print_result(message, result):
    if (message):
        print(message)

    time, coordinates = result
    print('  time (s):', time)
    print('  coordinates (m * m):', coordinates)