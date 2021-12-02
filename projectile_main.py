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
###  This is the main script that contains the functions for running
###  the simulation.
###
###  Author: Steven Norfolk
#####################################################################

# Constants:
radius_earth = 6371000
mass_earth = 5.972*10**24
G = 6.6743*10**-11
g = 9.81
rho_0 = 1.225
molar_mass = 0.0289644
R = 8.3144598
T_0 = 288

# Vector manipulation:
def calculate_normal(x_comp, y_comp):
    magnitude = math.sqrt(x_comp**2+y_comp**2)
    x_norm = x_comp/magnitude
    y_norm = y_comp/magnitude
    return x_norm, y_norm

def transform_coordinateSystem(x_comp, y_comp, theta):
    xi = x_comp*math.cos(theta) + y_comp*math.sin(theta)
    yi = x_comp*math.sin(theta) - y_comp*math.cos(theta)
    return xi,yi

# Define functions:
def calculate_gravitationalAcc(x, y):
    r = calculate_radialHeight(x, y)
    rx_norm, ry_norm = calculate_normal(x,y+radius_earth)
    ag = -(G*mass_earth)/r**2
    ag_x = ag*rx_norm
    ag_y = ag*ry_norm
    return ag_x, ag_y

def calculate_airDensity(x, y): # https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html
    h = calculate_surfaceHeight(x, y)
    if h > 25000: # Upper atmosphere
        T = -131.21 + 0.00299*h
        p = 2.488*((T+273.1)/216.6)**-11.388
        rho = p/(0.2869*(T+273.1))
        return rho
    if h > 11000: # Mid atmosphere
        T = -56.46
        p = 22.65*math.exp(1.73-0.000157*h)
        rho = p/(0.2869*(T+273.1))
        return rho
    else: # Lower atmosphere
        T = 15.04-0.00649*h
        p = 101.29*((T+273.1)/288.08)**5.256
        rho = p/(0.2869*(T+273.1))
        return rho

def calculate_dragForce(x, y, x_vel, y_vel, area, cd):
    rho = calculate_airDensity(x, y)
    velocity = math.sqrt(x_vel**2+y_vel**2)
    fd = 0.5*rho*cd*area*(velocity**2)
    return fd

def calculate_dragAcc(x, y, x_vel, y_vel, area, mass, cd):
    x_vNorm, y_vNorm = calculate_normal(x_vel, y_vel)
    fd = calculate_dragForce(x, y, x_vel, y_vel, area, cd)
    x_accD = -fd*x_vNorm/mass
    y_accD = -fd*y_vNorm/mass
    return x_accD, y_accD

def calculate_acceleration(x, y, x_vel, y_vel, area, mass, cd, set_drag):
    x_accD, y_accD = [0,0]
    if set_drag == True:
        x_accD, y_accD = calculate_dragAcc(x, y, x_vel, y_vel, area, mass, cd)
    x_accG, y_accG = calculate_gravitationalAcc(x, y)
    x_acc = x_accD + x_accG
    y_acc = y_accD + y_accG
    return x_acc, y_acc

def calculate_radialHeight(x, y):
    r = math.sqrt(x**2+(y+radius_earth)**2)
    return r

def calculate_surfaceHeight(x, y):
    r = math.sqrt(x**2+(y+radius_earth)**2)
    h = r-radius_earth
    return h

######################## SIMULATION FUNCTIONS #######################
def initiate(launch_angle, launch_velocity, launch_height, mass, cd, set_drag):
    # Parameters are initiated here so that they can be easily and consistently imported into other scripts:
    t = 0
    x = 0
    y = launch_height
    launch_angle = (math.pi/180)*launch_angle
    area = (math.pi/4)*((4*mass)/(math.pi*1000*5))**(2/3)
    # Initial value calculations:
    x_vel = launch_velocity*math.cos(launch_angle) + 400 # Add Earths rotational velocity near the equator
    y_vel = launch_velocity*math.sin(launch_angle)
    x_acc, y_acc = calculate_acceleration(x, y, x_vel, y_vel, area, mass, cd, set_drag)
    h = calculate_surfaceHeight(x,y)
    # Time parameters:
    end_time = 30000
    timestep = 0.01
    return t, x, y, launch_angle, area, x_vel, y_vel, x_acc, y_acc, h, end_time, timestep

def update(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag, timestep): # Velocity Verlet method
    # Position update:
    x += x_vel*timestep + 0.5*x_acc*timestep**2
    y += y_vel*timestep + 0.5*y_acc*timestep**2
    # Acceleration update:
    x_acc_new, y_acc_new = calculate_acceleration(x, y, x_vel, y_vel, area, mass, cd, set_drag)
    # Velocity update:
    x_vel += 0.5*(x_acc + x_acc_new)*timestep
    y_vel += 0.5*(y_acc + y_acc_new)*timestep
    return x, y, x_vel, y_vel, x_acc_new, y_acc_new

def calculate_data(x, y, x_vel, y_vel, x_acc, y_acc, area, mass, cd, set_drag):
    # Transformative calculations:
    h = calculate_surfaceHeight(x, y)
    theta = math.atan2(y+radius_earth, x)
    # Radial and transverse velocity:
    r_vel, t_vel = transform_coordinateSystem(x_vel, y_vel, theta)
    velocity = math.sqrt(r_vel**2+t_vel**2)
    # Radial and transverse acceleration:
    r_acc, t_acc = transform_coordinateSystem(x_acc, y_acc, theta)
    acceleration = math.sqrt(r_acc**2+t_acc**2)
    # Atmospheric calculations
    rho = calculate_airDensity(x, y)
    fd = calculate_dragForce(x, y, x_vel, y_vel, area, cd)
    return h, r_vel, t_vel, velocity, r_acc, t_acc, acceleration, rho, fd
