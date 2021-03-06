#! /bin/bash
source /opt/ros/kinetic/setup.bash
source ~/robot_ws/devel/setup.bash

# Start roscore and wait till its finished
roscore -p 11311 &
sleep 5

# Start realsense
roslaunch robot_urdf rviz_model.launch &  # MAKE SURE TO CHANGE SENSOR POSITION AND ANGLE!!!
#roslaunch pose_ekf pose_ekf.launch &
roslaunch depth_to_laser depth_to_laser.launch & # MAKE SURE TO AGJUST SAMPLE OF DEPTH BASED ON HIEGHT OF CAM
roslaunch merge_laser d435_mod.launch &
sleep 5
roslaunch merge_laser merge_laser.launch &
#sleep 3

#roslaunch mapping mapping.launch &

#roslaunch mapping map_server.launch & # Change file directories for your computer
#roslaunch localization amcl.launch &

# LIMIT DATA
rosrun topic_tools throttle messages /map 0.5 &
rosrun topic_tools throttle messages /scan_multi 1.0 &
rosrun topic_tools throttle messages /particlecloud 1.0