#!/usr/bin/env python
import json

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix
from datetime import datetime

AIS_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
battery_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
energy_consumption_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
fix_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
humidity_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
hdg_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
pitch_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
roll_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
signal_quality_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
AIS_threshold = 5
battery_threshold = 5
energy_consumption_threshold = 5
fix_threshold = 5
humidity_threshold = 5
hdg_threshold = 5
pitch_threshold = 5
roll_threshold = 5
signal_quality_threshold = 5

data_dict = {}


def AIS_callback(data):
    global data_dict
    global AIS_timestamp
    rospy.loginfo(rospy.get_caller_id() + "AIS: %s", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - AIS_timestamp >= AIS_threshold:
        AIS_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["AIS"] = data.data
        print(data_dict)


def battery_callback(data):
    global data_dict
    global battery_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Battery Voltage: %3d", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - battery_timestamp >= battery_threshold:
        battery_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["voltage"] = data.data
        print(data_dict)


def energy_comsumption_callback(data):
    global data_dict
    global energy_consumption_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Battery Current: %4d", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - energy_consumption_timestamp >= energy_consumption_threshold:
        energy_consumption_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["current"] = data.data
        print(data_dict)


def fix_callback(data):
    global data_dict
    global fix_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Latitude: %9.6f", data.latitude)
    rospy.loginfo(rospy.get_caller_id() + "Longitude: %9.6f", data.longitude)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - fix_timestamp >= fix_threshold:
        fix_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["fix"] = (data.latitude, data.longitude)
        print(data_dict)


def humidity_sensor_callback(data):
    global data_dict
    global humidity_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Hull water (%): %3d", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - humidity_timestamp >= humidity_threshold:
        humidity_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["humidity"] = data.data
        print(data_dict)


def hdg_callback(data):
    global data_dict
    global hdg_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Heading: %3d", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - hdg_timestamp >= hdg_threshold:
        hdg_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["hdg"] = data.data
        print(data_dict)


def pitch_callback(data):
    global data_dict
    global pitch_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Pitch: %9.6f", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - pitch_timestamp >= pitch_threshold:
        pitch_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["pitch"] = data.data
        print(data_dict)


def roll_callback(data):
    global data_dict
    global roll_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Roll: %9.6f", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - roll_timestamp >= roll_threshold:
        roll_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["roll"] = data.data
        print(data_dict)


def signal_quality_callback(data):
    global data_dict
    global signal_quality_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Signal quality: %s", data.data)
    if (datetime.now() - datetime.fromtimestamp(0)).total_seconds() - signal_quality_timestamp >= signal_quality_threshold:
        signal_quality_timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds()
        data_dict["signal_quality"] = data.data
        print(data_dict)


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
    # file_path = "scenario1.json"
    # with open(file_path) as json_file:
    #     data = json.load(json_file)
    #     info = data["information"]
    #     AIS_threshold = info["AIS"]
    #     battery_threshold = info["battery"]
    #     energy_consumption_threshold = info["energy_consumption"]
    #     fix_threshold = info["fix"]
    #     humidity_threshold = info["humidity"]
    #     hdg_threshold = info["hdg"]
    #     pitch_threshold = info["pitch"]
    #     roll_threshold = info["roll"]
    #     signal_quality_threshold = info["signal_quality"]

    listener()
