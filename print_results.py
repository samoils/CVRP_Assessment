def print_results(opt_method, routes, loads, distance):
    print(f"Optimzation method: {opt_method}")

    total_load = 0
    for route, load in zip(routes, loads):
        print(f"Route: {route}, Load: {load}")
        total_load += load

    print(f"Total distance: {distance}")
    print(f"Total load: {total_load}")
