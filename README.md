# CVPR_Routing

This project implements a solution to a Capacitated Vehicle Routing Problem (CVPR). Two separate methods are tested to
provide validation that the correct solution is being found. Several different methods were originally considered,
however, due to implementation practicalities and time constraints the OR-Tools solver and PyVRP were chosen.

## CVRP Problem Description
The Capacitated Vehicle Routing Problem (CVRP) is a combinatorial optimization problem that is a generalization of the
traveling salesman problem. This problems is tasked with determining an optimal route through a set of delivery nodes
utilizing a set of vehicles with a maximum capacity for cargo that must be delivered. Further generalizations of this
problem extend it to include both pickups and deliveries, time constraints, reloading of vehicles, and more.

In the case of the problem being solved for this project a set of 1 vehicles, each with a maximum capacity of 100, are
sent to deliver to 20 nodes. The starting node is the 0-th node. The capacity limits of the vehicles must not be
exceeded and the vehicles must only deliver to each node exactly once. The start and finish node of the problem is the
0-th node.

## Dependencies
- uv (optional)
- Python > 3.13
- OR-Tools
- PyVRP

## Instructions to run the project
Prepare a virtual environment of choice (uv was used for development) and install the dependencies.

Run project using:

```python main.py```

## Summary of Results


### Optimzation method: OR-Tools

Route 0: [0, 5, 14, 6, 10, 9, 19, 13, 4, 3, 1], Load: 92

Route 1: [0, 11, 12, 17, 8, 7, 18, 16, 15, 20, 2], Load: 98

Total distance: 215

Total load: 190

### Optimzation method: PyVRP

Route 0: [5, 14, 6, 10, 9, 19, 13, 4, 3, 1], Load: 92

Route 1: [0, 11, 12, 17, 8, 7, 18, 16, 15, 20, 2], Load: 98

Total distance: 215

Total load: 190

## Key Design Decisions and Assumptions

An initial survey was conducted of the available approaches, algorithms, and libraries available to solve CVRP problems.
From this survey a short list of candidate libraries was found:

- OR-Tools
- PyVRP
- Qiskit Optimization
- CPLEX (docplex)
- cuOpt
- D-Wave Ocean CVRP solver
- Gurobi

The Gurobi, D-Wave Ocean CVRP solver, CPLEX, and Qiskit Optimization libraries were eliminated due to the complexity
and commericial license requirements. This left OR-Tools, PyVRP, and cuOpt. To ensure the widest range of compatibility,
and the time constraints around implementation, it was determined that cuOpt was not an ideal candidate. This left 
OR-Tools and PyVRP as the remaining candidates.

To ensure that the results of the solvers were valid it was determined that both solvers should be implemented for
comparison. 