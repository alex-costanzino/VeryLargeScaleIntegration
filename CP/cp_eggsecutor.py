'''
Alex Costanzino
MSc student in Artificial Intelligence
@ Alma Mater Studiorum, University of Bologna
September, 2021
'''

from tqdm import trange
import subprocess

def raw_output_cleaner(raw_output):
    '''
    It is kind of a mess. It should be more robust, but I am going to cry if I work on this a little more :(
    '''
    splitted_output = raw_output[0]
    splitted_output = raw_output[0].split('\n') # Split according the newline.

    splitted_time = raw_output[1].split('\n') # Split according the newline.
    time = splitted_time[-2] # The time is in the last but one line, since there is a \n as last one.
    clean_time = []
    
    for char in time:
        if char in '0123456789.':
            clean_time.append(char)
        
    return [splitted_output[:-3], # I do not take the last two lines since they are just the Minizinc separators. 
            ''.join(map(str, clean_time))[:-1] # I do not take the last char since it is just the full stop.
            ]

def produce_txt(outputs, i: int):
    solution_path = 'C:/Users/AlexC/OneDrive/Desktop/cdmo-m1_project/CP/out'
    f = open(solution_path + '/outs-' + str(i) + '.txt', 'w')
    for line in outputs[0]:
        line_ = line.strip()
        f.write(line_)
        f.write('\n')
    f.write(outputs[1])
    f.close()

def main():
    model_path = 'C:\\Users\\AlexC\\OneDrive\\Desktop\\cdmo-m1_project\\CP\\src\\04_global_model_symmetries.mzn'
    instance_number = 40
    solver_name = 'Gecode'
    time_limit = 300 * 10**3 # In millisenconds.

    executor = 'minizinc'
    out_flag = '-v'
    solver = '--solver' + ' ' + solver_name
    limitator = '--solver-time-limit' + ' ' + str(time_limit)
    
    in_no = 1
    for instance in trange(1, instance_number + 1):
        instance_selector = 'in/ins-' + str(instance) + '.dzn'
        
        command = executor + ' ' + out_flag + ' ' + solver + ' ' + model_path + ' ' + instance_selector + ' ' + limitator
        
        process = subprocess.run(command, 
                                 capture_output = True, 
                                 shell = True, 
                                 universal_newlines = True)
        
        raw_outputs = [process.stdout, process.stderr]
        
        outputs = raw_output_cleaner(raw_outputs)
    
        print(outputs)
        
        produce_txt(outputs, in_no)
        
        in_no += 1
        
if __name__ == '__main__':
    main()