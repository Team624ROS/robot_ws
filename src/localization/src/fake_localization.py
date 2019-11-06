#!/usr/bin/env python

import math
from math import sin, cos, pi
import rospy
# Needed for converting quaternion_from_euler
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import Float32
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


class Localization:
    def __init__(self):
        rospy.init_node('robot_localization')
        self.localization_pub = rospy.Publisher("base_pose_ground_truth", Odometry, queue_size=50)

        self.pose_data = 0
        self.twist_data = 0

    def pose_callback(self,msg): 
        self.pose_data = msg.data.pose

    def twist_callback(self,msg): 
        self.twist_data = msg.data.twist
    
    def main(self):

        sub = rospy.Subscriber('robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, self.pose_callback)
        sub = rospy.Subscriber('odom', Odometry, self.twist_callback)

        # Rate at which the program runs in (hz) how many times per second
        hz_rate = 15.0

        current_time = rospy.Time.now()

        r = rospy.Rate(hz_rate)
        while not rospy.is_shutdown():
            current_time = rospy.Time.now()

            # next, we'll publish the odometry message over ROS
            odom = Odometry()
            odom.header.stamp = current_time
            odom.header.frame_id = "fake_odom"

            if self.pose_data != 0:
                odom.pose = self.pose_data
                odom.twist = self.twist_data

            odom.child_frame_id = "base_link"

            # publish the message
            self.localization_pub.publish(odom)

            r.sleep()

robot_localization = Localization()
robot_localization.main()