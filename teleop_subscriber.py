#!/usr/bin/env python3

import sys, select, termios, tty
import rospy
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist

pub = rospy.Publisher("set_velocity",Float64MultiArray, queue_size = 10)
wheel = Float64MultiArray() 
def fun(msg):
	wheel_l = msg.linear.x + msg.angular.z
	wheel_r = msg.linear.x - msg.angular.z
	wheel.data = [wheel_l,wheel_r]
	print(wheel)
	pub.publish(wheel)
	
rospy.init_node('bot')
sub = rospy.Subscriber("cmd_vel",Twist,fun)
rospy.spin()

