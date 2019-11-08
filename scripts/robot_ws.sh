#! /bin/bash
source /opt/ros/kinetic/setup.bash
source ~/robot_ws/devel/setup.bash

# Start roscore and wait till its finished
roscore -p 11311 &
sleep 5
 
# Start realsense
roslaunch robot_urdf rviz_model.launch &
roslaunch pose_ekf pose_ekf.launch &
roslaunch depth_to_laser depth_to_laser.launch &
rosrun gmapping slam_gmapping scan:=scan