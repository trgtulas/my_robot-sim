#!/usr/bin/env python

import rospy 

from messages.srv       import to_goal
from messages.srv       import to_goalRequest
from messages.srv       import to_goalResponse
from nav_msgs.msg       import Odometry
from geometry_msgs.msg  import Point
from geometry_msgs.msg  import PoseStamped



def goal_callback(msg):
    target_pose = msg.pose.position
    rospy.loginfo("target_pose x = %f y = %f z = %f", target_pose.x, target_pose.y, target_pose.z)

def to_goal_client():
    rospy.wait_for_service('to_goal')
    try:
        to_the_goal = rospy.ServiceProxy('to_goal', to_goal)
        resp1= to_the_goal()
        return resp1.arrived
    except rospy.ServiceException as e:
        print("service failed: %s", e)

if __name__ == "__main__":
    rospy.init_node('client_node')
    print("Check if goal is reached")
    s = to_goal_client()
    if(s):
        print("Goal is reached")
    rospy.spin()