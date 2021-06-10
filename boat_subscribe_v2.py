#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix

def AIS_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "AIS: %s", data.data)

def battery_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Battery Voltage: %3d", data.data)

def energy_comsumption_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Battery Current: %4d", data.data)

def fix_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Latitude: %9.6f", data.latitude)
    rospy.loginfo(rospy.get_caller_id() + "Longitude: %9.6f", data.longitude)

def humidity_sensor_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Hull water (%): %3d", data.data)

def hdg_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Heading: %3d", data.data)

def pitch_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Pitch: %9.6f", data.data)

def roll_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Roll: %9.6f", data.data)

def signal_quality_callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Signal quality: %s", data.data)

def listener():
    data = [("AIS", String),
            ("battery", Int32),
            ("energy_comsumption", Int32),
            ("fix", NavSatFix),
            ("hdg", Int32),
            ("pitch", Float32),
            ("roll", Float32),
            ("signal_quality", String)]

    # data = [("AIS", String),
    #         ("battery", Int32),
    #         ("energy_comsumption", Float32)
    #         ("fix", NavSatFix),
    #         ("humidty_sensor", Int32),
    #         ("hdg", Int16),
    #         ("pitch", Float32),
    #         ("roll", Float32),
    #         ("signal_quality", String)]

    for i in range(len(data)):
        # tipo de node e a informacao que contem
        node = data[i][0]
        v_type = data[i][1]

        # anonymous=True implica que o rospy ira escolher
        # um nome unico para o node "listener" para que varios
        # listeners consigam correr simultaneamente
        rospy.init_node('listener', anonymous=True)

        callback_method = eval(str(node) + "_callback")

        rospy.Subscriber(node, v_type, callback_method)

    # impede que o python termine antes que o node seja parado
    rospy.spin()


if __name__ == '__main__':
    listener()
