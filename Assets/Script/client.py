import socket
import json
from config import IMPORT_FILE_NAME, ROS_API_BASE_URL, UDP_IP, UDP_RECEIVE_PORT, UDP_SEND_PORT, USER_DATA, DEVICE_DATA
from apis.api import login, device_add_to_db, device_update_action_to_db
from libs.CaptureVideo import CaptureVideo

ROS_API_URL = ROS_API_BASE_URL + "/api/v1/"

# send
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# receive
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.bind((UDP_IP, UDP_RECEIVE_PORT))

def device_update_action(device_id, data, token):
    rot1 = data["rot1"]
    rot2 = data["rot2"]
    rot3 = data["rot3"]
    rot4 = data["rot4"]
    rot5 = data["rot5"]
    rot6 = data["rot6"]
    send_ = str(rot1) + ',' + str(rot2) + ',' + str(rot3) + ',' + str(rot4) + ',' + str(rot5) + ',' + str(rot6)
    print(send_)
    send_socket.sendto((str(send_)).encode(), (UDP_IP, UDP_SEND_PORT))
    device_update_action_to_db(device_id, (str(send_)).encode(), token)
    # receive the position of joints
    message, address = receive_socket.recvfrom(1024)
    joint_positions = message.decode().split(";")
    print(joint_positions[0], joint_positions[1], joint_positions[2], joint_positions[3], joint_positions[4], joint_positions[5])  

    print('Finish!')

if __name__ == "__main__":
    token=login(USER_DATA)
    device_id=device_add_to_db(DEVICE_DATA,token)
    if IMPORT_FILE_NAME:
        with open(IMPORT_FILE_NAME) as json_file:
            all_data = json.load(json_file)
            for data in all_data:
                device_update_action(device_id, data, token)
    else:
        cap_video = CaptureVideo()
        while True:
            data = cap_video.run_cap_video()
            if not data:
                break
            else:
                device_update_action(device_id, data, token)
