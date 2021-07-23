import json
from datetime import datetime
from time import time
from pymongo import MongoClient

timestamp = time()

dados1 = {'timestamp': (datetime.fromtimestamp(timestamp)).strftime("%Y/%m/%d, %H:%M:%S"), 'hdg': 358, 'signal_quality': '100', 'fix': (38.691498333333335, -9.298588333333333),
          'AIS': '', 'current': 32, 'voltage': 123, 'pitch': -8.58362102508545, 'roll': -0.0}
dados2 = {'timestamp': (datetime.fromtimestamp(timestamp+10)).strftime("%Y/%m/%d, %H:%M:%S"), 'hdg': 358, 'signal_quality': '100',
          'fix': (38.691498333333335, -9.298588333333333), 'AIS': '',
          'current': 32, 'voltage': 123, 'pitch': -8.520272254943848, 'roll': -0.0}
dados3 = {"Timestamp": (datetime.fromtimestamp(timestamp)).strftime("%Y/%m/%d, %H:%M:%S"), "GPS": (38.691498333333335, -9.298588333333333),
                    "IMU": (358, -8.520272254943848, -0.0),
                    "AIS": '', "Corrente": 32,
                    "Voltagem": 123,
                    "Water": 2}
dados4 = {"Timestamp": (datetime.fromtimestamp(timestamp)).strftime("%Y/%m/%d, %H:%M:%S"), "GPS": (38.6914983335, -9.2985883334),
                    "IMU": (358, -8.520272254943848, -0.0),
                    "AIS": '', "Corrente": 30,
                    "Voltagem": 125,
                    "Water": 3,
                    "Codename": "ENIDH",
                    "Description": "Descrição de teste, viagem realizada entre localização X e Y"}

file_path = "tmp/mission" + str(1) + ".json"

def update_json(new_data, file_name=file_path):
    with open(file_name, 'r+') as file:
        file_data = json.load(file)
        file_data["mission_details"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def create_json(file_name=file_path):
    with open(file_name, "w") as file:
        main_struct = {"mission_details": []}
        json.dump(main_struct, file)


def load_json(file_name=file_path):
    with open(file_name) as file:
        test = json.load(file)
        # print(test)
    return test


def upload_data(data_to_upload):
    # ligacao ao MongoDB
    client = MongoClient(
        "mongodb+srv://admin:conchinha123@clusterisel.ksoyd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    mydb = client["BoatTelemetryDB"]

    mycollection = mydb["Mission1"]

    mycollection.insert_one(data_to_upload)

create_json()
update_json(dados3)
update_json(dados4)
file_path = "tmp/mission1.json"
with open(file_path) as json_file:
    stored_data = json.load(json_file)
    stored_data = stored_data["mission_details"]
for entry in stored_data:
    print(entry)
    upload_data(entry)
