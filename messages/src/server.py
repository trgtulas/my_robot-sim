#!/usr/bin/env python

from nav_msgs.msg   import Odometry
from geometry_msgs.msg  import PoseStamped
from geometry_msgs.msg import Point
from math           import isclose


from messages.srv   import to_goal
from messages.srv   import to_goalRequest
from messages.srv   import to_goalResponse
from actionlib_msgs.msg  import GoalStatusArray
import rospy

class RobotPosition:
    def __init__(self):
        self.current_pose = Point()
        self.arrived = False
        self.reached = GoalStatusArray()
        rospy.Subscriber('odom', Odometry, self.odom_callback)
        rospy.Subscriber('move_base/status', GoalStatusArray, self.status_callback)
        rospy.Service('to_goal', to_goal, self.handle_to_goal)
        rospy.loginfo("getting robot position...")

    def status_callback(self, msg):
        self.reached.status_list = msg.status_list
        
    def handle_to_goal(self, req):
        if (self.reached.status_list[0].status == 3):
            self.arrived = True
            rospy.loginfo("goal reached..")
            return to_goalResponse(self.arrived)
        else:
            rospy.loginfo("current pose: x = %f y = %f", self.current_pose.x, self.current_pose.y)

if __name__ == "__main__":
    rospy.init_node('server_node')
    RobotPosition()    
    rospy.spin()
