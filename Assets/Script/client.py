import socket
import json
import time
import select

with open("../Data/angle_0.json") as json_file:
    data = json.load(json_file)


UDP_IP = '127.0.0.1'
UDP_SEND_PORT = 5060
UDP_RECEIVE_PORT = 5061

# send
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# receive
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.bind((UDP_IP, UDP_RECEIVE_PORT))


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
