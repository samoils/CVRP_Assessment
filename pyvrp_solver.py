import pyvrp
import pyvrp.plotting
import pyvrp.stop

def pyvrp_solver(problem_data):


    m = pyvrp.Model()
    m.add_depot(x=0,y=0)
    m.add_vehicle_type(num_available=problem_data['num_vehicles'], capacity=problem_data['vehicle_capacities'][0])

    for i in range(len(problem_data['nodes']['delivery_locations']) + 1):
        m.add_client(x=i, y=i, delivery=problem_data['demands'][i])

    for frm in m.locations:
        for to in m.locations:
            if frm != to:
                m.add_edge(frm, to, distance=problem_data['distance_matrix'][int(frm.x)][int(to.x)])

    res = m.solve(stop=pyvrp.stop.MaxRuntime(10))
   
    return True