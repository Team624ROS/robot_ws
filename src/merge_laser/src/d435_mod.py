#!/usr/bin/env python

import math
import rospy
import tf
from sensor_msgs.msg import LaserScan

class Laser:
    def __init__(self):
        rospy.init_node('d435_mod')
        self.laser_pub = rospy.Publisher("/d435/scan", LaserScan, queue_size=50)
        self.got_data_d = False
        self.got_data_r = False

    def d435_callback(self,msg): 
        # Raw encoder data in ticks
        self.d435_data = msg
        self.got_data_d = True

    def rplidar_callback(self,msg): 
        # Raw encoder data in ticks
        self.rplidar_data = msg
        self.got_data_r = True
    
    
    def main(self):

        d435_sub = rospy.Subscriber('/d435/raw/scan', LaserScan, self.d435_callback)
        rplidar_sub = rospy.Subscriber('/rplidar/scan', LaserScan, self.rplidar_callback)
        hz_rate = 30

        current_time = rospy.Time.now()

        r = rospy.Rate(hz_rate)

        while not rospy.is_shutdown():

            current_time = rospy.Time.now()

            # next, we'll publish the laserscan message over ROS
            if self.got_data_d and self.got_data_r:
                laser = LaserScan()
                
                laser.header = self.d435_data.header
                laser.angle_min = self.d435_data.angle_min
                laser.angle_max = self.d435_data.angle_max
                laser.angle_increment = self.d435_data.angle_increment
                laser.time_increment = self.d435_data.time_increment
                laser.scan_time = self.d435_data.scan_time
                laser.range_min = self.d435_data.range_min
                laser.range_max = self.d435_data.range_max
                laser.ranges = self.d435_data.ranges
                laser.intensities = self.rplidar_data.intensities
                # publish the message
                self.laser_pub.publish(laser)

            r.sleep()

laser_mod = Laser()
laser_mod.main()