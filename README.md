# Very large scale integration design in CP and SMT
The repository contains the project realized for the *Combinatorial Decision Making and Optimization - Mod. 1* course of the Master's degree in Artificial Intelligence, at Alma Mater Studiorum, University of Bologna.

The projects is realized by me.

## Repository structure and contents
To execute the models just change all the addresses in cp_eggsecutor.py for CP and in each model for SMT.
.
├── data
│   └── instances                                                 # Folder that contains all the instances as text files
│   └── CDMO_Project_2021                                         # PDF that describes the assignment of the project
├── CP                             
│   ├── in                                                        # Folder that contains all the instances as data files
│   ├── out                                                       # Folder that contains some solutions as text files
│   ├── out_img                                                   # Folder that contains some solutions as images files
│   ├── src
│   │   ├── 01_base_model.mzn        
│   │   ├── 02_base_model_with_implied_constraint.mzn       
│   │   ├── 03_global_constraint_model.mzn        
│   │   ├── 04_global_model_symmetries.mzn
│   │   ├── 06_global_constraint_rotations.mzn        
│   │   ├── 06_global_constraint_rotations_symmetries.mzn  
│   │   └── strip_packing_problem.mzp                             # Project file
│   ├── utils
│   │   ├── instances-converter_txt-to-dzn.py        
│   │   ├── plotter.py                                            # Routine to plot time-histograms  
│   │   └── solution-visualizer.py                                # Routine to visualize solutions
│   ├── cp_eggsecutor.py                                          # Routine to run all the instances
│   ├── report.pdf  
│   └── stats.xlsx                                                # Statistics to evaluate models
├── SMT                             
│   ├── out                                                       # Folder that contains some solutions as text files
│   ├── src
│   │   ├── 01_base_model.py        
│   │   ├── 02_base_model_with_symmetry-breaking.py       
│   │   ├── 03_rotation_model.py        
│   │   └── 04_rotation_model_with_symmetry-breaking.py
│   ├── utils
│   │   ├── instances_reader.py        
│   │   ├── plotter.py                                            # Routine to plot time-histograms  
│   │   └── solution-visualizer.py                                # Routine to visualize solutions
│   ├── report.pdf  
│   └── stats.xlsx                                                # Statistics to evaluate models
├── LICENSE
└── README.md

## Main libraries
* [Z3Py](https://github.com/Z3Prover/z3) 4.8.12;
* [tqdm](https://github.com/tqdm/tqdm) 4.62.3;
* [Numpy](https://numpy.org/) 1.21.

Further details can be found in the report.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for further details.
