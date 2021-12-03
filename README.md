# Earth-to-orbit ballistic trajectories with atmospheric resistance

## Overview

Space guns are a theoretical technology that reduces the cost of getting bulk materials into space using giant cannons to replace the first stage of a rocket.

This script performs a simple simulation of an unpowered ballistic projectile within the Earths atmosphere. The simulation uses the Velocity Verlet method to simulate the projectiles motion and applies it with a simple atmosphere model [made available by NASA](https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html).

### Running the simulation

The repository contains several scripts that function in different ways to collect and display information:

- projectile_main.py: Contains the core simulation functions that are called by other scripts.
- projectile_single.py: Runs the simulation once with the parameters that are imbedded in the code. The code will need to be edited directly in order to change the simulation parameters at the moment.
- projectile_maxHeight: Iterates a parameter (such as launch velocity, launch angle, initial height, etc.) through a range of values to display how changing that parameter affects the maximum height the projectile reaches.
- projectile_dataGather: Provides the results from a series of simulation runs at once to observe how changing a parameter affects the trajectory.
- projectile_minEnergy: Iterates through a range of launch angles and increments the launch velocity until a target stable orbit (TSO) is reached. More data is then calculated to determine how the launch angle affects how much mass can be delivered to orbit in a single launch.

Developed for Unusual systems and in collaboration with Lancaster laboratories.
