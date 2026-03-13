import pyvrp
import pyvrp.plotting
import pyvrp.stop

import print_results

def pyvrp_solver(problem_data):
    # Prepare the model for solving.
    m = pyvrp.Model()

    # Add the Depot node to the model. PyVRP has 2D indexing compared to OR-Tools so need to "fake" the coordinates
    # by repeating them.
    start_depot = m.add_depot(x=0,y=0)

    # Add vehicles to the model. First add the start depot location created above, only allow 1 of each vehicle,
    # and then add the capacity for each vehicle from the problem data.
    m.add_vehicle_type(start_depot=start_depot, num_available=1, capacity=problem_data['vehicle_capacities'][0])
    m.add_vehicle_type(start_depot=start_depot, num_available=1, capacity=problem_data['vehicle_capacities'][1])

    # Add all the drop-off locations to the model. Similar to the Depot the 2D indexing needs to be "faked" by
    # repeating the index.
    for i in range(len(problem_data['nodes']['delivery_locations']) + 1):
        m.add_client(x=i, y=i, delivery=problem_data['demands'][i])

    # Add the distance values to the model. This nested for loop iterates over all of the distances and skips the
    # self-referencing distances.
    for frm in m.locations:
        for to in m.locations:
            if frm != to:
                m.add_edge(frm, to, distance=problem_data['distance_matrix'][int(frm.x)][int(to.x)])

    # Solve the problem. Set the max runtime to 1 second.
    res = m.solve(stop=pyvrp.stop.MaxRuntime(1), display=False)

    # Prepare the data for printing.
    routes = []
    loads = []
    #distance = []
    for route in res.best.routes():
        # PyVRP indexes the node locations starting at 1, need to subtract 1 to match how OR-Tools reports values
        # PyVRP also appears to not include the depot node in the list for only the first vehicle
        routes.append([r - 1 for r in route.visits()])
        loads.append(sum(route.delivery()))

    # Print the data using the print_results function in the print_results module.
    print_results.print_results("PyVRP", routes, loads, res.best.distance())
