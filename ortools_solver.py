from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import print_results

def ortools_solver(problem_data):
    # Prepare the manager that will control the optimization. This adds the distance data, the number of vehicles,
    # and the depot node value to the manager.
    manager = pywrapcp.RoutingIndexManager(len(problem_data['distance_matrix']), problem_data['num_vehicles'],
                                           problem_data['depot_node'])

    # Add the Manager to the routing model.
    routing = pywrapcp.RoutingModel(manager)

    # Prepare the callback that returns the distance between the from_index and the to_index by indexing into the
    # distance matrix. This will be used Routing Model.
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return problem_data['distance_matrix'][from_node][to_node]

    # Register the distance_callback with the Routing Model and also set the Arc Cost Evaluator.
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Prepare the demand_callback. This indexes into the demand list to get the cargo capacity at each node that will
    # be required to be picked up by the vehicle.
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return problem_data['demands'][from_node]

    # Register the demand_callback with the Routing Model and also set Capacity dimensions for each vehicle.
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, problem_data['vehicle_capacities'],
                                            True, 'Capacity')

    # Set the default routing search parameters and then set the first solution strategy to find the cheapest arc.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Set the local search metaheuristic to guided local search and apply a time limit of 1 second.
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Collect the results from the problem solution.
    total_distance = 0
    total_load = 0
    routes = []
    loads = []
    for vehicle_id in range(problem_data['num_vehicles']):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_load = 0
        route = []

        # Get the route, route distance, and route loads from the solution and put them into a format to be passed to
        # the print_results function.
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += problem_data['demands'][node_index]
            route.append(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        routes.append(route)
        loads.append(route_load)
        total_distance += route_distance
        total_load += route_load

    # Print the data using the print_results function in the print_results module.
    print_results.print_results("OrTools", routes, loads, total_distance)
    return True