#! /bin/bash
source /opt/ros/kinetic/setup.bash
source ~/robot_ws/devel/setup.bash

# Start roscore and wait till its finished
roscore -p 11311 &
sleep 1

#roslaunch mapping mapping_sim.launch

roslaunch mapping map_server_sim.launch & # Change file directories for your computer
roslaunch localization amcl_sim.launch