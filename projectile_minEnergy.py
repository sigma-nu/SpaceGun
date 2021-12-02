from projectile_main import *

import math
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import sys
import numpy as np
import re
import time

#####################################################################
###  A script to determine the ballistic trajectories
###  of projectiles with atmospheric resistance.
###
###  Iterates through a range of angles and velocities to find
###  minimum requirements for specific TSO.
###
###  Author: Steven Norfolk
#####################################################################

# Define functions:
def calculate_kinEnergy(m, v):
    return 0.5*m*v**2

def calculate_remainingMass(m, t_v, Isp): # Rocket equation
    return m*math.exp(-(math.sqrt((G*mass_earth)/(TSO+radius_earth))-t_v)/(Isp*9.81))

###################### INITIALIZING DATA LISTS ######################
min_velocity = []
min_energy = []
t_vel_list = []
angles = []
mass_remaining = []

############################### INPUT ###############################
# Input parameters:
launch_height = 0  # INITIAL HEIGHT ABOVE SEA-LEVEL IN M
mass = 2000  # PROJECTILE MASS IN KG
cd = 0.2  # PROJECTILE DRAG COEFFICIENT

TSO = 50*10**3  # TARGET STABLE ORBIT
Isp = 400  # ROCKET SPECIFIC IMPULSE

# Atmospheric drag?
set_drag = True  # FLAG TO TURN OFF ATMOSPHERIC DRAG

############################# MAKE FILE #############################
file_name = 'MinVel_' + str(int(TSO/1000)) + 'km_' + str(mass) + 'kg.txt'
print(file_name)
file = open(file_name,'w')

for angle in range(10,91,10):
    angles.append(angle)
    launch_velocity = 0
    print('Angle =',angle)
    for i in range(3):
        vel_step = 1000/(10**i) # Changes the step size each round so accuracy increases
        print('Velocity step =',vel_step)
        max_height = 0
        while max_height < TSO:
            launch_velocity += vel_step
            ######################### RE-INITIALIZATION #########################
            launch_angle = angle

            t, x, y, launch_angle, area, x_vel, y_vel, x_acc, y_acc, h, end_time, timestep = initiate(launch_angle, launch_velocity, launch_height, mass, cd, set_drag)

            h_list = [] # Reset h_list each time

            ########################### SIMULATION ##############################
            while h >= 0 and t <= end_time:
                # Update motion:
                x, y, x_vel, y_vel, x_acc, y_acc = update(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag, timestep)

                # Calculate parameters:
                h, r_vel, t_vel, velocity, r_acc, t_acc, acceleration, rho, fd = calculate_data(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag)

                # Make list:
                h_list.append(h)

                # Advance time:
                t += timestep
            max_height = max(h_list) # Find maximum height reached this run
            print('Velocity =', launch_velocity, '\t Max height =', max_height)
        launch_velocity -= vel_step # Reset to just below min vel to TSO
    launch_velocity += vel_step # Retain correct min vel
    print('MINIMUM VELOCITY =', launch_velocity, '\n')

    kin_energy = calculate_kinEnergy(mass, launch_velocity)
    remaining_mass = calculate_remainingMass(mass, t_vel, Isp)

    min_energy.append(kin_energy)
    mass_remaining.append(remaining_mass)
    min_velocity.append(launch_velocity)
    t_vel_list.append(t_vel)

    data_line = str(angle) + '\t' + str(velocity) + '\t' + str(t_vel) + '\t' + str(kin_energy) + '\t' + str(remaining_mass) + '\n'
    file.write(data_line)

############################## PLOT #################################
plt.plot(angles,min_velocity)
plt.title('Minimum velocity required to reach TSO')
plt.xlabel(r'Launch angle, $\theta$ [$\degree$]')
plt.ylabel('Initial velocity, $v_i$ [$m/s$]')
plt.show()

plt.plot(angles,min_energy)
plt.title('Minimum energy required to reach TSO')
plt.xlabel(r'Launch angle, $\theta$ [$\degree$]')
plt.ylabel('Energy at launch, $E_i$ [$J$]')
plt.show()

plt.plot(angles,t_vel_list)
plt.title('Tangential velocity at TSO')
plt.xlabel(r'Launch angle, $\theta$ [$\degree$]')
plt.ylabel('Tangential velocity, $v_t$ [$m/s$]')
plt.show()

plt.plot(angles,mass_remaining)
plt.title('Mass of payload remaining in circularised orbit')
plt.xlabel(r'Launch angle, $\theta$ [$\degree$]')
plt.ylabel('Final mass, $m_f$ [$kg$]')
plt.show()
