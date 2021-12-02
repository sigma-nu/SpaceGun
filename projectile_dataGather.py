from projectile_new_main import *

import math
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import sys
import numpy as np
import re
import os

#####################################################################
###  A script to determine the ballistic trajectories
###  of projectiles with atmospheric resistance.
###
###  Determines how the max height of projectile changes with variables.
###
###  Author: Steven Norfolk
#####################################################################

############################### INPUT ###############################
# Input parameters:
heights     = [    0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
angles      = [   10,   20,   30,   40,   50,   60,   70,   80,   90]
velocities  = [ 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,10000]
masses      = [   10,   50,  100,  200,  300,  500, 1000, 2000, 4000]

variable_list = velocities  # CHANGE THIS TO CHOOSE WHICH VARIABLE IS MEASURED
title = 'velocity_'

for variable in variable_list:
    ############################ CREATE FILE ############################

    file_name = title + str(variable) + '.txt'
    print(file_name)
    file = open(file_name,'w')

    ############################### INPUT ###############################
    # Input parameters:
    launch_height = 0  # SETS INITIAL HEIGHT ABOVE SEA-LEVEL
    launch_angle = 30  # INITIAL LAUNCH ANGLE IN DEGREES
    launch_velocity = variable  # INITIAL LAUNCH VELOCITY IN M/S
    mass = 500  # PROJECTILE MASS IN KG
    cd = 0.2  # PROJECTILE DRAG COEFFICIENT

    # Atmospheric drag?
    set_drag = True   # FLAG TO TURN OFF ATMOSPHERIC DRAG

    ########################## INITIALIZATION ###########################
    # Initial value calculations:
    t, x, y, launch_angle, area, x_vel, y_vel, x_acc, y_acc, h, end_time, timestep = initiate(launch_angle, launch_velocity, launch_height, mass, cd, set_drag)

    ############################ SIMULATION #############################
    while h >= 0 and t <= end_time:
        # Update motion:
        x, y, x_vel, y_vel, x_acc, y_acc = update(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag, timestep)

        # Calculate parameters:
        h, r_vel, t_vel, velocity, r_acc, t_acc, acceleration, rho, fd = calculate_data(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag)

        # Save to file:
        # .txt file will have the form: (1)Time (2)x pos. (3)y pos. (4)r vel. (5)t vel. (6)r acc. (7)t acc. (8)height above sea-level
        t_str = format(t,'.5f') # Reformat t for data file
        data_line = t_str + '\t' + str(x) + '\t' + str(y) + '\t' + str(r_vel) + '\t' + str(t_vel) + '\t' + str(r_acc) + '\t' + str(t_acc) + '\t' + str(h) + '\n'
        file.write(data_line)

        t += timestep
