from projectile_new_main import *

import math
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import sys
import numpy as np
import re

#####################################################################
###  A script to determine the ballistic trajectories of projectiles
###  with atmospheric resistance.
###
###  Iterates through a variable (launch velocity, angle, etc.) to
###  see how it impacts the maximum height of the projectile.
###
###  Author: Steven Norfolk
#####################################################################

###################### INITIALIZING DATA LISTS ######################
variables = []
max_height = []
h_list = []

############################### INPUT ###############################
variables = range(0, 16001, 200) # SET VARIABLE RANGE

for variable in variables:
    print('Variable =',variable)

    # Standard launch parameters:
    launch_height = 0  # INITIAL HEIGHT ABOVE SEA-LEVEL IN M
    launch_angle = 30  # INITIAL LAUNCH ANGLE IN DEGREES
    launch_velocity = 8000  # INITIAL LAUNCH VELOCITY IN M/S
    mass = 500  # PROJECTILE MASS IN KG
    cd = 0.12  # PROJECTILE DRAG COEFFICIENT

    launch_height = variable  # SET WHICH VARIABLE TO CHANGE AND ITERATE OVER

    # Atmospheric drag?
    set_drag = True  # FLAG TO TURN OFF ATMOSPHERIC DRAG

    ########################## INITIALIZATION ###########################
    t, x, y, launch_angle, area, x_vel, y_vel, x_acc, y_acc, h, end_time, timestep = initiate(launch_angle, launch_velocity, launch_height, mass, cd, set_drag)

    ########################### SIMULATION ##############################
    while h >= 0 and t <= end_time:
        # Update motion:
        x, y, x_vel, y_vel, x_acc, y_acc = update(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag, timestep)

        # Calculate data:
        h, r_vel, t_vel, velocity, r_acc, t_acc, acceleration, rho, fd = calculate_data(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag)

        h_list.append(h)

        t += timestep
    max_height.append(max(h_list))

############################## PLOT #################################
# Height against time
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.plot(variables,max_height)
plt.title('Maximum height above sea-level')
plt.xlabel(r'Initial height, $h_0$ [$m$]')
plt.ylabel('Max height [$m$]')
plt.minorticks_on()
ax.grid(which='minor', alpha=0.3, linestyle = ':')
ax.grid(which='major', alpha=0.6)
plt.show()
