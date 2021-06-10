from pymongo import MongoClient
from time import time
from datetime import datetime

def send_to_db(dados):
    local = check_connection()
    # fazer a verificacao para ver se tem internet ou nao
    timestamp = time()
    dt_object = datetime.fromtimestamp(timestamp)
    if local:
        pass
    else:
        # ligacao ao MongoDB
        client = MongoClient("mongodb+srv://admin:conchinha123@clusterisel.ksoyd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        mydb = client["BoatTelemetryDB"]
        # determinar o numero da missao
        mission_num = 1
        mycollection = mydb["Mission" + str(mission_num)]

        data_to_send = {"Timestamp": ""+str(dt_object), "GPS": dados["GPS"], "IMU": dados["IMU"],
              "AIS": dados["AIS"], "Corrente": dados["A"], "Voltagem": dados["V"], "Água no Casco": dados["agua"]}

        mycollection.insert_one(data_to_send)

def check_connection():
    pass