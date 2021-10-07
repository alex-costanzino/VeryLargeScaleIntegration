'''
Alex Costanzino
MSc student in Artificial Intelligence
@ Alma Mater Studiorum, University of Bologna
September, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

my_dpi = 96
plt.figure(figsize = (800/my_dpi, 800/my_dpi), dpi = my_dpi)

def solution_extractor(solution):
    extracted_solution = {}
    
    lines = solution.split("\n")
    board_length, board_height = int(lines[0].split(" ")[0]), int(lines[0].split(" ")[1])
    
    circuits_number = int(lines[1])
    circuits_specs = []
    
    for i in range(2, len(lines) - 1):
        circuit = {}
        specs = lines[i].split(" ")
        circuit_width, circuit_height, posX, posY = int(specs[0]), int(specs[1]), int(specs[2]), int(specs[3])
        circuit["circuit_dim"] = [circuit_width, circuit_height]
        circuit["circuit_pos"] = [posX, posY]
        circuits_specs.append(circuit)
    
    extracted_solution["board_dim"] = [board_length, board_height]
    extracted_solution["circuits_num"] = circuits_number
    extracted_solution["circuits_specs"] = circuits_specs
    
    return extracted_solution

def draw_solution(extracted_solution, ins):
    rows, cols = tuple(extracted_solution["board_dim"])
    board = np.zeros((cols,rows), dtype = np.int32)
    
    circuit_index = 1
    
    for circuit_spec in extracted_solution["circuits_specs"]:
        posX, posY = tuple(circuit_spec["circuit_pos"])
        circuit_width, circuit_height = tuple(circuit_spec["circuit_dim"])
        
        for x in range(posX, posX + circuit_width):
            for y in range(posY, posY + circuit_height):
                board[cols - 1 - y, x] = circuit_index
        circuit_index += 1
        
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(0, extracted_solution["board_dim"][0] + 1, 1))
    ax.set_yticks(np.arange(0, extracted_solution["board_dim"][1] + 1, 1))
    
    ax.imshow(board, interpolation = 'nearest', extent = [0, rows, 0, cols])
    
    print(ins, board)
    
    plt.title('Instance No. ' + str(ins))
    plt.grid()
    plt.show()

def main():
    solutions_dir = 'C:/Users/AlexC/OneDrive/Desktop/cdmo-m1_project/CP/out/'

    for i in range(1,41):
        parsed_test_solution = solution_extractor(open(solutions_dir + "outs-" + str(i) + ".txt", "r").read())
        draw_solution(parsed_test_solution, ins = i)
        
if __name__ == '__main__':
    main()
