from projectile_main import *

import math
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import sys
import numpy as np
import re

'''
A script to determine the ballistic trajectories of projectiles with atmospheric resistance.
This script runs a single simulation run.
Calls on projectile_new_main.py

Author: Steven Norfolk
'''

############################### INPUT ###############################
# Input parameters:
launch_height = 0  # INITIAL HEIGHT ABOVE SEA-LEVEL IN M
launch_angle = 30  # INITIAL LAUNCH ANGLE IN DEGREES
launch_velocity = 8000  # INITIAL LAUNCH VELOCITY IN M/S
mass = 500  # PROJECTILE MASS IN KG
cd = 0.12  # PROJECTILE DRAG COEFFICIENT

# Atmospheric drag?
set_drag = True  # FLAG TO TURN OFF ATMOSPHERIC DRAG

# Plot figures?
plot_trajectory = True  # FLAGS TO PLOT FIGURES
plot_velocity = True
plot_acc = True
plot_atmosphere = False

########################## INITIALIZATION ###########################
# Continuous parameter list initialization:
t_list = []
h_list = []
if plot_trajectory == True:
    x_list = []
    y_list = []
if plot_velocity == True:
    r_vel_list = []
    t_vel_list = []
    velocity_list = []
if plot_acc == True:
    r_acc_list = []
    t_acc_list = []
    acceleration_list = []
if plot_atmosphere == True:
    rho_list = []
    if set_drag == True:
        fd_list = []

# Initial value calculations:
t, x, y, launch_angle, area, x_vel, y_vel, x_acc, y_acc, h, end_time, timestep = initiate(launch_angle, launch_velocity, launch_height, mass, cd, set_drag)

########################### SIMULATION ##############################
while h >= 0 and t <= end_time+timestep:
    # Update motion:
    x, y, x_vel, y_vel, x_acc, y_acc = update(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag, timestep)

    # Calculate data:
    h, r_vel, t_vel, velocity, r_acc, t_acc, acceleration, rho, fd = calculate_data(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag)

    # Append data to lists:
    t_list.append(t)
    h_list.append(h)
    if plot_trajectory == True:
        x_list.append(x)
        y_list.append(y)
    if plot_velocity == True:
        r_vel_list.append(r_vel)
        t_vel_list.append(t_vel)
        velocity_list.append(velocity)
    if plot_acc == True:
        r_acc_list.append(r_acc)
        t_acc_list.append(t_acc)
        acceleration_list.append(acceleration)
    if plot_atmosphere == True:
        rho_list.append(rho)
        if set_drag == True:
            fd_list.append(fd)

    t += timestep

########################### CONVERT TO KM ###########################
radius_earth = radius_earth/1000
h_list = [h/1000 for h in h_list]
if plot_trajectory == True:
    x_list = [x/1000 for x in x_list]
    y_list = [y/1000 for y in y_list]
if plot_velocity == True:
    r_vel_list = [v/1000 for v in r_vel_list]
    t_vel_list = [v/1000 for v in t_vel_list]
    velocity_list = [v/1000 for v in velocity_list]
if plot_acc == True:
    r_acc_list = [a/1000 for a in r_acc_list]
    t_acc_list = [a/1000 for a in t_acc_list]
    acceleration_list = [a/1000 for a in acceleration_list]

############################## PLOT #################################
if plot_trajectory == True:
    # Projectile motion graph
    earth = plt.Circle((0,-radius_earth), radius_earth, color='skyblue')
    ax = plt.gca()
    ax.cla()
    ax.add_artist(earth)
    plt.plot(x_list,y_list)
    plt.title('Projectile motion')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axes().set_aspect('equal')
    plt.show()

    # Height against time
    plt.plot(t_list,h_list)
    plt.title('Height above sea-level')
    plt.xlabel('t')
    plt.ylabel('h')
    plt.show()

if plot_velocity == True:
    # Radial velocity against time
    plt.plot(t_list,r_vel_list)
    plt.title('Radial velocity against time')
    plt.xlabel('t')
    plt.ylabel('r_vel')
    plt.show()

    # Tangential velocity against time
    plt.plot(t_list,t_vel_list)
    plt.title('Tangential velocity against time')
    plt.xlabel('t')
    plt.ylabel('t_vel')
    plt.show()

    # velocity with time
    plt.plot(t_list,velocity_list)
    plt.title('velocity')
    plt.xlabel('t')
    plt.ylabel('vel')
    plt.show()

if plot_acc == True:
    # Radial acceleration against time
    plt.plot(t_list,r_acc_list)
    plt.title('Radial acceleration against time')
    plt.xlabel('t')
    plt.ylabel('r_acc')
    plt.show()

    # Tangential acceleration against time
    plt.plot(t_list,t_acc_list)
    plt.title('Tangential acceleration against time')
    plt.xlabel('t')
    plt.ylabel('t_acc')
    plt.show()

    # acceleration with time
    plt.plot(t_list,acceleration_list)
    plt.title('Acceleration')
    plt.xlabel('t')
    plt.ylabel('acc')
    plt.show()

if plot_atmosphere == True:
    # Atmospheric density graph
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(h_list,rho_list)
    plt.title('Atmospheric density')
    plt.xlabel('Height, $h$ [$km$]')
    plt.ylabel(r'Density, $\rho$ [$kg/m^3$]')
    plt.minorticks_on()
    ax.grid(which='minor', alpha=0.3, linestyle = ':')
    ax.grid(which='major', alpha=0.6)
    plt.show()

    # Air density against time
    plt.plot(t_list,rho_list)
    plt.title('Air density with time')
    plt.xlabel('t')
    plt.ylabel('rho')
    plt.show()

    if set_drag == True:
        # Drag force with time
        plt.plot(t_list,fd_list)
        plt.title('Drag force')
        plt.xlabel('t')
        plt.ylabel('fd')
        plt.show()
