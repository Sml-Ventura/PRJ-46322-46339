#!/usr/bin/env python
import json
import rospy
import math

from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix
from time import time
from datetime import datetime
from send_to_database import send_to_db

AIS_timestamp = time()
battery_timestamp = time()
energy_consumption_timestamp = time()
fix_timestamp = time()
humidity_timestamp = time()
hdg_timestamp = time()
pitch_timestamp = time()
roll_timestamp = time()
signal_quality_timestamp = time()
AIS_threshold = 5
battery_threshold = 5
energy_consumption_threshold = 5
fix_threshold = 5
humidity_threshold = 5
hdg_threshold = 5
pitch_threshold = 5
roll_threshold = 5
signal_quality_threshold = 5

prev_GPS = (-1,-1)
curr_GPS = (-1,-1)
prev_A = -1
curr_A = -1

mission_num = -1
data_dict = {"reg_time": None, "hdg": None, "pitch": None, "roll": None, "voltage": None, "current": None, "fix": None, "signal_quality": None, "AIS": None, "humidity": None}


def AIS_callback(data):
    global data_dict
    global AIS_timestamp
    rospy.loginfo(rospy.get_caller_id() + "AIS: %s", data.data)
    if time() - AIS_timestamp >= AIS_threshold:
        AIS_timestamp = time()
        data_dict["AIS"] = data.data
        print(data_dict)


def battery_callback(data):
    global data_dict
    global battery_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Battery Voltage: %3d", data.data)
    if time() - battery_timestamp >= battery_threshold:
        battery_timestamp = time()
        data_dict["voltage"] = data.data
        print(data_dict)


def energy_comsumption_callback(data):
    global data_dict
    global energy_consumption_timestamp
    global prev_A
    global curr_A
    prev_A = curr_A
    rospy.loginfo(rospy.get_caller_id() + "Battery Current: %4d", data.data)
    curr_A = data.data
    if time() - energy_consumption_timestamp >= energy_consumption_threshold:
        energy_consumption_timestamp = time()
        data_dict["current"] = data.data
        print(data_dict)


def fix_callback(data):
    global data_dict
    global fix_timestamp
    global prev_GPS
    global curr_GPS
    prev_GPS = curr_GPS
    rospy.loginfo(rospy.get_caller_id() + "Latitude: %9.6f", data.latitude)
    rospy.loginfo(rospy.get_caller_id() + "Longitude: %9.6f", data.longitude)
    curr_GPS = (data.latitude, data.longitude)
    if time() - fix_timestamp >= fix_threshold:
        fix_timestamp = time()
        data_dict["fix"] = (data.latitude, data.longitude)
        print(data_dict)


def humidity_sensor_callback(data):
    global data_dict
    global humidity_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Hull water (%): %3d", data.data)
    if time() - humidity_timestamp >= humidity_threshold:
        humidity_timestamp = time()
        data_dict["humidity"] = data.data
        print(data_dict)


def hdg_callback(data):
    global data_dict
    global hdg_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Heading: %3d", data.data)
    if time() - hdg_timestamp >= hdg_threshold:
        hdg_timestamp = time()
        data_dict["hdg"] = data.data
        print(data_dict)


def pitch_callback(data):
    global data_dict
    global pitch_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Pitch: %9.6f", data.data)
    if time() - pitch_timestamp >= pitch_threshold:
        pitch_timestamp = time()
        data_dict["pitch"] = data.data
        print(data_dict)


def roll_callback(data):
    global data_dict
    global roll_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Roll: %9.6f", data.data)
    if time() - roll_timestamp >= roll_threshold:
        roll_timestamp = time()
        data_dict["roll"] = data.data
        print(data_dict)


def signal_quality_callback(data):
    global data_dict
    global signal_quality_timestamp
    rospy.loginfo(rospy.get_caller_id() + "Signal quality: %s", data.data)
    if time() - signal_quality_timestamp >= signal_quality_threshold:
        signal_quality_timestamp = time()
        data_dict["signal_quality"] = data.data
        data_dict["reg_time"] = (datetime.fromtimestamp(time())).strftime("%Y/%m/%d, %H:%M:%S")
        send_to_db(data_dict, False)


def upload_callback(data):
    global data_dict
    global mission_num
    rospy.loginfo(rospy.get_caller_id() + "Upload data to cloud? %d", data.data)
    check_boat_status()
    if data.data != "":
        codename = data.data.split(";")[0]
        description = data.data.split(";")[1]
        print(data_dict)
        mission_num = send_to_db(data_dict, True, mission_num, codename, description)
        data_dict = {}


def check_boat_status():
    global prev_A
    global curr_A
    global prev_GPS
    global curr_GPS

    if math.sqrt((curr_GPS[0] - prev_GPS[0])**2 + (curr_GPS[1] - prev_GPS[1])**2) > 0.00002:
        change_scenario("scenario1")
    elif curr_A <= 2 and math.sqrt((curr_GPS[0] - prev_GPS[0])**2 + (curr_GPS[1] - prev_GPS[1])**2) <= 0.00002:
        change_scenario("scenario2")
    elif abs(curr_A - prev_A) > 5:
        change_scenario("scenario3")
    elif curr_A <= 2 and math.sqrt((curr_GPS[0] - prev_GPS[0])**2 + (curr_GPS[1] - prev_GPS[1])**2) > 0.00002:
        change_scenario("scenario4")


def change_scenario(scenario):
    global AIS_threshold
    global battery_threshold
    global energy_consumption_threshold
    global fix_threshold
    global humidity_threshold
    global hdg_threshold
    global pitch_threshold
    global roll_threshold
    global signal_quality_threshold
    scenario_path = "scenarios/" + scenario + ".json"
    with open(scenario_path) as json_file:
        json_data = json.load(json_file)
        info = json_data["information"]
        AIS_threshold = info["AIS"]
        battery_threshold = info["battery"]
        energy_consumption_threshold = info["energy_consumption"]
        fix_threshold = info["fix"]
        humidity_threshold = info["humidity"]
        hdg_threshold = info["hdg"]
        pitch_threshold = info["pitch"]
        roll_threshold = info["roll"]
        signal_quality_threshold = info["signal_quality"]


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
    #         ("signal_quality", String),
    #         ("upload", String)]

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
    file_path = "scenario1.json"
    with open(file_path) as json_file:
        json_data = json.load(json_file)
        info = json_data["information"]
        AIS_threshold = info["AIS"]
        battery_threshold = info["battery"]
        energy_consumption_threshold = info["energy_consumption"]
        fix_threshold = info["fix"]
        humidity_threshold = info["humidity"]
        hdg_threshold = info["hdg"]
        pitch_threshold = info["pitch"]
        roll_threshold = info["roll"]
        signal_quality_threshold = info["signal_quality"]

    listener()
