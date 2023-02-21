import socket
import json
import os
import requests
from dotenv import load_dotenv

with open("../Data/angle_0.json") as json_file:
    data = json.load(json_file)

load_dotenv('.env')
UDP_IP = os.getenv('UDP_IP', '127.0.0.1')
UDP_SEND_PORT = os.getenv('UDP_SEND_PORT', 5060)
UDP_RECEIVE_PORT = os.getenv('UDP_RECEIVE_PORT', 5061)
ROS_API_BASE_URL = os.getenv('ROS_API_BASE_URL','http://localhost')
ROS_API_URL = ROS_API_BASE_URL + "/api/v1/"

# send
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# receive
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.bind((UDP_IP, UDP_RECEIVE_PORT))

def device_add(data, token):
    url = ROS_API_URL + 'device'
    r = requests.post(url, json = data, headers={"Content-Type":"application/json", "Authorization": f"Bearer {token}"})
    return r.json()['id']

def device_update_action(data):
    for line in data:
        rot1 = line["rot1"]
        rot2 = line["rot2"]
        rot3 = line["rot3"]
        rot4 = line["rot4"]
        rot5 = line["rot5"]
        rot6 = line["rot6"]
        send_ = str(rot1) + ',' + str(rot2) + ',' + str(rot3) + ',' + str(rot4) + ',' + str(rot5) + ',' + str(rot6)
        print(send_)
        send_socket.sendto((str(send_)).encode(), (UDP_IP, UDP_SEND_PORT))
        
        # receive the position of joints
        message, address = receive_socket.recvfrom(1024)
        joint_positions = message.decode().split(";")
        print(joint_positions[0], joint_positions[1], joint_positions[2], joint_positions[3], joint_positions[4], joint_positions[5])  

        print('Finish!')

if __name__ == "__main__":
    device_update_action(data)