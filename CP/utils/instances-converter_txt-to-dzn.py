'''
Alex Costanzino
MSc student in Artificial Intelligence
@ Alma Mater Studiorum, University of Bologna
September, 2021
'''

import os

instances_path = 'C:/Users/AlexC/OneDrive/Desktop/cdmo-m1_project/data/instances/'
converted_instances_path = 'C:/Users/AlexC/OneDrive/Desktop/cdmo-m1_project/cp/in/'

# Initialize a dict to rapidly change the names in case of necessity.
parameters_names = {'width': 'width',
                    'ICs_number': 'ICs_number',
                    'IC_widths': 'IC_widths',
                    'IC_heights': 'IC_heights'}

def extract_IC_dimensions(lines: str):
    widths = []
    heights = []
    
    for line in lines:
        dimensions = line.split(" ") # Split line according to the whitespace.
        
        # In each line we have width and height of each IC.
        widths.append(int(dimensions[0]))
        heights.append(int(dimensions[1]))
        
    return widths, heights

def convert_txt_to_dzn(instance: str):
    lines = instance.split("\n") # Split instances according to new line.
    
    # If the last element of the line is empty, remove it.
    while lines[-1] == "":
        lines = lines[:-1]
        
    converted_lines = []
    
    # Lenght of the silicon plate.
    converted_lines.append(parameters_names["width"] + " = " + lines[0] + ";")
    
    # Number of ICs on the silicon plate.
    converted_lines.append(parameters_names["ICs_number"] + " = " + lines[1] + ";")
    
    # Opening of the width and height of each IC.
    width_line = parameters_names["IC_widths"] + " = ["
    height_line = parameters_names["IC_heights"] + " = ["
    
    # From the second line and on.
    widths, heights = extract_IC_dimensions(lines[2:])
    
    for i in range(len(widths) - 1):
        width_line += str(widths[i]) + ", "
        height_line += str(heights[i]) + ", "
    
    # Closure of the width and height of each IC.
    width_line += str(widths[-1]) + "];"
    height_line += str(heights[-1]) + "];"
    
    converted_lines.append(width_line)
    converted_lines.append(height_line)
    
    return converted_lines

def main():
    for subdir, dirs, files in os.walk(instances_path):
        for file in files:
            instance = open(os.path.join(subdir, file), 'r').read()
            converted_lines = convert_txt_to_dzn(instance)
            converted_instance = '\n'.join(converted_lines)
            
            # Sanity check on the converted instances path. If not present it will be created.
            if not os.path.exists(converted_instances_path):
                os.makedirs(converted_instances_path)
                
            instance_file = open(converted_instances_path + file.split(".txt")[0] + ".dzn", "x")
            instance_file.write(converted_instance)
            instance_file.close()
            
if __name__ == '__main__':
    main()