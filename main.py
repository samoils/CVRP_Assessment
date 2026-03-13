import json
import os

import ortools_solver
import pyvrp_solver

# Function to load the problem data from the provided JSON file.
def load_data(filename):
    # Get the local directory path in a way that is compatible with various operating systems.
    directory = os.path.dirname(__file__)
    data_file = os.path

    # Open the provided file and load the data into a dictionary.
    with open(os.path.join(directory, filename), 'r') as f:
        data = json.load(f)

    # Restructure the data dictionary into a format that is easier to work with for the optimization methods.
    # For the vehicle capacities this will flatten the list of capacities into a single list.
    problem_data = {
        'problem_name': data['problem_name'],
        'problem_description': data['problem_description'],
        'nodes': data['nodes'],
        'depot_node': 0,
        'num_vehicles': data['vehicles']['count'],
        'vehicle_capacities': [data['vehicles']['capacity_per_vehicle'] for i in range(data['vehicles']['count'])],
        'demands': data['demands'],
        'distance_matrix': data['distance_matrix'],
        'constraints': data['constraints']
    }

    return problem_data

# Main function to run the optimization methods.
def main():
    problem_data = load_data('cvrp_problem_data.json')

    ortools_solver.ortools_solver(problem_data)

    pyvrp_solver.pyvrp_solver(problem_data)

if __name__ == '__main__':
    main()
