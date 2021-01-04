#!/usr/bin/env python3

import numpy as np
import sys, select, termios, tty
import rospy
from std_msgs.msg import Float64MultiArray, Float64
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
global kp,kpi,kd
kp = 0.007
ki = 0.005
kd = 0.02
global set_velocity, current_velocity,error, prev_error
set_velocity = [0,0,0,0]
current_velocity = [0,0,0,0]
error = [0,0,0,0]
prev_error =[0,0,0,0]
p = [0,0,0,0]
i = [0,0,0,0]
d = [0,0,0,0]
finalvalue = [0,0,0,0]
sum_error = [0,0,0,0]
wheels_l = Float64MultiArray()
wheels_r = Float64MultiArray()

def callback1(joint):
	global wheel_lf, wheel_lr, wheel_rf, wheel_rr
	global set_velocity, current_velocity
	current_velocity = joint.velocity
	[wheel_lf,wheel_lr,wheel_rf,wheel_rr] = current_velocity
	PID(current_velocity,set_velocity)
#	print(set_velocity)

def callback(wheel):
	global set_velocity
	[set_wheel_lf,set_wheel_rf] = wheel.data
	set_wheel_rr = set_wheel_rf
	set_wheel_lr = set_wheel_lf
	set_velocity = [set_wheel_lf,set_wheel_lr,set_wheel_rf,set_wheel_rr]
#	print(set_velocity)
		
def PID(current_velocity, set_velocity):
	global wheels_l, wheels_r, prev_error, p, i, d, finalvalue, sum_error, error
	for j in range(4):
		error[j] = set_velocity[j] - current_velocity[j]
		p[j] = error[j]*kp
		sum_error[j] += error[j]*0.05
		d[j] = (error[j] - prev_error[j])*kd/0.05
		i[j] = sum_error[j]*ki
		finalvalue[j] = p[j] + i[j] + d[j]
	print(finalvalue)
	prev_error = error
	wheels_l.data = [finalvalue[0],finalvalue[1]]
	wheels_r.data = [finalvalue[2],finalvalue[3]]
	pubr.publish(wheels_r)
	publ.publish(wheels_l)
	pub.publish(wheel_lf)
if __name__ == "__main__":
	rospy.init_node("Teleop_feedback")
	rospy.Rate(2)
	joint = JointState() 
	pubr = rospy.Publisher('/MYROBOT/r_con_position_controller/command',Float64MultiArray,queue_size = 10)
	publ = rospy.Publisher('/MYROBOT/l_con_position_controller/command',Float64MultiArray,queue_size = 10)
	pub = rospy.Publisher('MYROBOT/PID',Float64,queue_size = 10)
	sub1 = rospy.Subscriber("set_velocity",Float64MultiArray,callback)
	sub2 = rospy.Subscriber("MYROBOT/joint_states",JointState,callback1)
	rospy.spin()
	
	
