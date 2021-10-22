'''
Alex Costanzino
MSc student in Artificial Intelligence
@ Alma Mater Studiorum, University of Bologna
October, 2021
'''

def read_instance(instance_path: str) -> tuple:
    instance_file = open(instance_path, 'r') # Open the file.
    instance = instance_file.read() # Read the file, obtain a string.
    
    instance = instance.split('\n') # Split line according to new line.
    
    width = int(instance[0])
    ICs_number = int(instance[1])
    
    IC_widths = []
    IC_heights = []
    
    for i in range(2,len(instance)-1):
        temp_str = instance[i].split()
        IC_widths.append(int(temp_str[0]))
        IC_heights.append(int(temp_str[1]))
        
    instance_file.close()
    
    return width, ICs_number, IC_widths, IC_heights

def write_solution(instance_path: str, solution_path: str, solution: tuple):
    instance_file = open(instance_path, 'r') # Open the instance file.
    instance = instance_file.read() # Read the file, obtain a string.
    
    instance = instance.split('\n') # Split line according to new line.
    
    instance[0] += ' ' + str(solution[0]) # Put the minimize height next to the fixed width.
    
    # Add the x and y coordinate of each piece.
    for i in range(2, len(instance) - 1):
        instance[i] += ' ' + str(solution[1][i-2]) + ' ' + str(solution[2][i-2])
        
    instance[-1] = str(solution[3]) # Add elapsed time.
    
    instance_file.close() # Close the instance file.
    
    solution_file = open(solution_path, 'w') # Open (create) the solution file.
    
    solution_file.write('\n'.join(str(element) for element in instance)) # Write on it.
    
    solution_file.close() # Close the solution file
    
def write_solution_rot(instance_path: str, solution_path: str, solution: tuple):
    instance_file = open(instance_path, 'r') # Open the instance file.
    instance = instance_file.read() # Read the file, obtain a string.
    
    instance = instance.split('\n') # Split line according to new line.
    
    instance[0] += ' ' + str(solution[0]) # Put the minimize height next to the fixed width.
    
    # Add the x and y coordinate of each piece.
    for i in range(2, len(instance) - 1):
        instance[i] += ' ' + str(solution[1][i-2]) + ' ' + str(solution[2][i-2])
        
    instance[-1] = str(solution[3])
    instance.append(str(solution[4])) # Add elapsed time.
    
    instance_file.close() # Close the instance file.
    
    solution_file = open(solution_path, 'w') # Open (create) the solution file.
    
    solution_file.write('\n'.join(str(element) for element in instance)) # Write on it.
    
    solution_file.close() # Close the solution file