'''
Alex Costanzino
MSc student in Artificial Intelligence
@ Alma Mater Studiorum, University of Bologna
October, 2021
'''

ins = r'C:\Users\AlexC\OneDrive\Desktop\cdmo-m1_project\data\instances\ins-'
outs = r'C:\Users\AlexC\OneDrive\Desktop\cdmo-m1_project\SMT\out\outs-'

TIME_LIMIT = 300 # Time limit in seconds.

import sys
sys.path.append('../')

from utils.instance_reader import read_instance, write_solution_rot

from z3 import Int, Or, Optimize, sat, And, Implies

from timeit import default_timer as timer
from tqdm import trange

def rotation_model(width: int, ICs_number: int, IC_widths: list, IC_heights: list) -> tuple:
    '''
    Implement the rotation model for the 2d strip packing problem.

    Parameters
    ----------
    width : int
        Width of the silicon plate.
    ICs_number : int
        Number of integrated circuits to place.
    IC_widths : list
        Widths of each integrated circuits to place.
    IC_heights : list
        Heights of each integrated circuits to place.

    Returns
    -------
    tuple
        Model solution with elapsed time.
    
    '''
    
    ''' Parameters '''
    upper_bound = sum(IC_heights) # Worst case, all ICs are piled.
    lower_bound = min(IC_heights)
    
    ''' Decision variables '''
    # Height of the plate.
    height = Int('height')
    
    # Arrays that contains the left bottom corners of each component and rotation state of each component.
    x = [Int('x_{}'.format(i)) for i in range(ICs_number)]
    y = [Int('y_{}'.format(i)) for i in range(ICs_number)]
    r = [Int('r_{}'.format(i)) for i in range(ICs_number)] # No direct casting for Bool, so I'll use Int.
    
    ''' Constraints '''
    constraints = [] # List that will contain all the constraints of the model.
    
    '''
    Note that we can no longer limit the domain of decision variable directly into the 
    declaration like we did with Minizinc. Now we have to explicitly constrain them.
    '''
    
    # 1. Domain constraints.
    height_domain = [And(lower_bound <= height, 
                         height <= upper_bound)]
    
    x_domain = [And(0 <= x[i], 
                    x[i] <= (width - min(IC_widths))
                    ) 
                for i in range(ICs_number)]
    
    y_domain = [And(0 <= y[i], 
                    y[i] <= (upper_bound - min(IC_heights))
                    ) 
                for i in range(ICs_number)]
    
    r_domain = [Or(r[i] == 0, r[i] == 1) for i in range(ICs_number)]
    
    constraints += (height_domain + x_domain + y_domain + r_domain) # Update constraints.
    
    # 2. All ICs shall fit on the silicon plate.
    bound_x = [x[i] + r[i] * IC_heights[i] + (1 - r[i]) * IC_widths[i] <= width for i in range(ICs_number)] # Fixed by the problem.
    bound_y = [y[i] + r[i] * IC_widths[i] + (1 - r[i]) * IC_heights[i] <= height for i in range(ICs_number)]
    
    constraints += (bound_x + bound_y) # Update constraints.
    
    # 3. All ICs shall not overlap. This is the main constraint.
    no_overlap = [Or(x[i] + r[i] * IC_heights[i] + (1 - r[i]) * IC_widths[i] <= x[j],
                     x[i] - r[j] * IC_heights[j] - (1 - r[j]) * IC_widths[j] >= x[j],
                     y[i] + r[i] * IC_widths[i] + (1 - r[i]) * IC_heights[i] <= y[j],
                     y[i] - r[j] * IC_widths[j] - (1 - r[j]) * IC_heights[j] >= y[j]) 
                  for i in range(ICs_number) for j in range(ICs_number) if i != j]
    
    constraints += no_overlap # Update constraints.
    
    # 4. A circuit shall not rotate if its height is greater than the width of the plate.
    no_rot = [Implies(IC_heights[i] > width, r[i] == 0) for i in range(ICs_number)]
    
    constraints += no_rot
    
    ''' Solver '''
    optimizer = Optimize() # Optimization, this is a COP.
    optimizer.add(constraints)

    optimizer.minimize(height)
    
    optimizer.set(timeout = int(TIME_LIMIT * 1e3)) # Setting max time.
    
    start = timer()
    optimizer.check()
    end = timer()
    
    elapsed_time = end - start # Elapsed time in seconds.
    
    if optimizer.check() == sat:
        return (int(optimizer.model().evaluate(height).as_string()), 
                [int(optimizer.model().evaluate(x[i]).as_string()) for i in range(ICs_number)], 
                [int(optimizer.model().evaluate(y[i]).as_string()) for i in range(ICs_number)],
                [int(optimizer.model().evaluate(r[i]).as_string()) for i in range(ICs_number)],
                elapsed_time)
    elif optimizer.reason_unknown() == 'timeout':
        return 'Solver timeout'
        
def main():
    """
    i = 11
    width, ICs_number, IC_widths, IC_heights = read_instance(ins + str(i) + '.txt') # Read the instance.
    solution = base_model(width, ICs_number, IC_widths, IC_heights) # Pass the instance to the model.
    print(solution)
    """

    for i in trange(1, 41):
        width, ICs_number, IC_widths, IC_heights = read_instance(ins + str(i) + '.txt') # Read the instance.
        solution = rotation_model(width, ICs_number, IC_widths, IC_heights) # Pass the instance to the model.
        if solution == 'Solver timeout' or solution == None:
            pass
        else:
            write_solution_rot(ins + str(i) + '.txt', outs + str(i) + '.txt', solution)
    
if __name__ == '__main__':
    main()