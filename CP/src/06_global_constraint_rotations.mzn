/*
Alex Costanzino
MSc student in Artificial Intelligence
@ Alma Mater Studiorum, University of Bologna
October, 2021
*/

/* Global model with rotations */
include "diffn.mzn";
include "cumulative.mzn";

/* Parameters */
par int: width; % Width of the silicon plate.
par int: ICs_number; % Number of integrated circuits to place.

set of int: ICs = 1..ICs_number; % To index the ICs.

array[ICs] of par int: IC_widths; % Array of widths of ICs.
array[ICs] of par int: IC_heights; % Array of heights of ICs.

% It is useful to set a minimum and maximum height of the silicon plate in order to reduce the search space.
par int: upper_bound = sum(i in ICs)(IC_heights[i]); % Worst case, all ICs are piled.
par int: lower_bound = min(i in ICs)(IC_heights[i]);

/* Decision variables */
var lower_bound..upper_bound: height = max(i in ICs)
  (y[i] + rotation[i] * IC_widths[i] + (1 - rotation[i]) * IC_heights[i]); % Height of the silicon plate. 

% It is the maximum sum of position and height over each components, namely the most exterior wrt the plate. 
% In this manner the domain it's reduced to a discrete set of point, at most as the number of ICs.

% Arrays that contains the left bottom corners of each component.
array[ICs] of var 0..width-min(IC_widths): x;
array[ICs] of var 0..upper_bound-min(IC_heights): y;

% Of course they have to be positive and bounded by the dimension of the silicone plate, minus the minimum dimension of the component (worst case).
% Note that the domain restrictions of the variables are a sort of contraint.

% Array of booleans that contains the "state" (rotated or not) of each piece.
array[ICs] of var bool: rotation;

/* Constraints */

% (1) All ICs shall fit on the silicon plate.
constraint forall(i in ICs) (x[i] + rotation[i] * IC_heights[i] + (1 - rotation[i]) * IC_widths[i] <= width); % Fixed by the problem.
constraint forall(i in ICs) (y[i] + rotation[i] * IC_heights[i] + (1 - rotation[i]) * IC_widths[i] <= height);

% (2) Implied constraints.
constraint redundant_constraint(max(i in ICs) (x[i] + IC_widths[i]) <= width);
constraint redundant_constraint(max(i in ICs) (y[i] + IC_heights[i]) <= upper_bound);

% (3) All ICs shall not overlap. This is the main constraint.
constraint diffn(x, y, [(1 - rotation[i]) * IC_widths[i] | i in ICs], [rotation[i] * IC_heights[i] | i in ICs]);

% (4) Implied constraint from the diffn. They speed-up the search.
constraint redundant_constraint(cumulative(x, IC_widths, IC_heights, height));
constraint redundant_constraint(cumulative(y, IC_heights, IC_widths, width));

% (5) A circuit shall not rotate if its height is greater than the width of the plate.
constraint forall(i in ICs)(IC_heights[i] > width -> rotation[i] == false);

solve minimize height;

/* Output */
output ["\(width) \(height)"];
output ["\n"];
output ["\(ICs_number)"];
output ["\n"];
output ["\(IC_widths[i]) \(IC_heights[i]) \(x[i]) \(y[i]) \n" | i in ICs];