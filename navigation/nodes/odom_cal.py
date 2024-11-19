#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math

class OdometryCalculator:
    def __init__(self):
        rospy.init_node('odometry_calculator', anonymous=True)
        self.sub = rospy.Subscriber('/odom', Odometry, self.callback)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.previous_time = rospy.Time.now()

    def callback(self, data):
        # Extract position
        self.x = data.pose.pose.position.x
        self.y = data.pose.pose.position.y
        
        # Extract orientation
        orientation_q = data.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, self.theta) = euler_from_quaternion(orientation_list)

        # Get the current time
        current_time = rospy.Time.now()

        # Calculate time delta
        dt = (current_time - self.previous_time).to_sec()

        # Calculate velocity
        vx = data.twist.twist.linear.x
        vy = data.twist.twist.linear.y
        vtheta = data.twist.twist.angular.z

        # Print the odometry data
        rospy.loginfo("Position: x = %f, y = %f, theta = %f", self.x, self.y, self.theta)
        rospy.loginfo("Velocity: vx = %f, vy = %f, vtheta = %f", vx, vy, vtheta)

        # Update previous time
        self.previous_time = current_time

if __name__ == '__main__':
    try:
        odometry_calculator = OdometryCalculator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
