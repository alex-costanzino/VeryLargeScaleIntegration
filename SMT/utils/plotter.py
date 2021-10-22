'''
Alex Costanzino
MSc student in Artificial Intelligence
@ Alma Mater Studiorum, University of Bologna
September, 2021
'''

import os
import re
import seaborn as sns

import matplotlib.pyplot as plt
plt.figure(figsize = (16, 12), dpi = 192)

solution_path = 'C:/Users/AlexC/OneDrive/Desktop/cdmo-m1_project/SMT/out/'

def main():
    '''
    Create a bar-plot of execution time of the instances.
    '''
    tm = {}
    for subdir, dirs, files in os.walk(solution_path):
        for file in files:
            solution = open(os.path.join(subdir, file), 'r').read()
            lines = solution.split() # Split instances according to new line.
            
            tm[re.findall('\d+', file)[0]] = lines[-1] # Extract number of instance as key for the dict.
    
    # Transform the dict keys and values in numbers.
    x = [int(i) for i in tm.keys()]
    y = [float(i) for i in tm.values()]
    tm_ = dict(zip(x,y))
    
    # Sort the list in ascending number of istance.
    x_t = []
    y_t = []
    
    for k in sorted(tm_.keys()):
        x_t.append(k)
        y_t.append(tm_[k])

    print(x_t)
    print(y_t)
    
    # Number of instances to scale the plot.
    solved_instances = 40
    
    sns.set_theme(style = 'whitegrid')
    bar = sns.barplot(x_t[:solved_instances], y_t[:solved_instances], palette = 'tab10')
    bar.set(xlabel = 'Instance No. [#]', ylabel = 'Time [log(s)]')
    plt.axhline(y = 300, color = 'dimgray', linestyle = 'dashed') # Time limit.
    
    plt.title('Rotation model')
    plt.yscale('log') # For better comparison.
    
if __name__ == '__main__':
    main()