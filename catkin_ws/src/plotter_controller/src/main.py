#!/usr/bin/env python3

import math
import numpy as np

import rospy
import tf2_ros
import tf_conversions
import geometry_msgs.msg
import time
from sensor_msgs.msg import JointState
from std_msgs.msg import String

from arm_control import ArmControl

LIMIT_MIN_X = 80
LIMIT_MIN_Y = 80
LIMIT_MAX_X = 240
LIMIT_MAX_Y = 240
LIMIT_MIN_TH3 = -20
LIMIT_MAX_TH3 = 5
x, y = 100, 100
theta3 = -20

def callback(data):
    global x
    global y
    global theta3

    delta = 5
    pen_delta = 1
    rospy.loginfo(rospy.get_caller_id() + 'recieved "%s"', data.data)
    if data.data == "UP":
        y = min(y + delta, LIMIT_MAX_Y)
    if data.data == "DOWN":
        y = max(y - delta, LIMIT_MIN_Y)
    if data.data == "LEFT":
        x = max(x - delta, LIMIT_MIN_X)
    if data.data == "RIGHT":
        x = min(x + delta, LIMIT_MAX_X)
    if data.data == "PEN_UP":
        theta3 = max(theta3 - pen_delta, LIMIT_MIN_TH3)
    if data.data == "PEN_DOWN":
        theta3 = min(theta3 + pen_delta, LIMIT_MAX_TH3)
    if data.data == "RESET":
        x, y, theta3 = 100, 100, -20

def main():
    global x
    global y
    global theta3

    rospy.init_node('ik_solver')
    publisher_angles = rospy.Publisher('joint_state', JointState, queue_size=10)

    rospy.Subscriber('chatter', String, callback)
    rate = 100 #[hz]

    r = rospy.Rate(rate) #[hz] 
    theta1 = 0 #[rad]
    theta2 = 0  #[rad]
    t = 0 #[sec]

    arm = ArmControl(publisher_angles)

    while not rospy.is_shutdown():

        print(x, y)
        theta1, theta2 = arm.solve_ik_deg(x, y)

        print(theta1, theta2, theta3)
        arm.update_angles(theta1, theta2, theta3)

        t = t + (1/rate) #[sec]

        # rospy.loginfo(x)
        r.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

