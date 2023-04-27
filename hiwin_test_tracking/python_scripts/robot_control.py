import socket
import numpy as np
import math
import os
import json
import threading
import sys
from apis.api import login, device_add, device_get
from dotenv import load_dotenv

load_dotenv('.env')
### socket
UDP_IP = os.getenv('UDP_IP','127.0.0.1')
UDP_SEND_PORT = int(os.getenv('UDP_SEND_PORT',5065))
UDP_RECEIVE_PORT = int(os.getenv('UDP_RECEIVE_PORT',5066))
DEVICE_ID = os.getenv('DEVICE_ID', None)

user_data = {
  "email": os.getenv('USER_EMAIL', 'user'),
  "password": os.getenv('USER_PASSWORD', 'user')
}

device_data = {
  "name": os.getenv('DEVICE_NAME','device_from_robotSim')
}

token=login(user_data)
print(token)

if DEVICE_ID is None:
  DEVICE_ID=device_add(device_data,token)
  envFile = open(".env", "a")
  print(DEVICE_ID)
  envFile.writelines('DEVICE_ID='+str(DEVICE_ID))

send_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.bind((UDP_IP, UDP_RECEIVE_PORT))

current_angle = []
### angle
def dotproduct(v1, v2):
  result = sum((a*b) for a, b in zip(v1, v2))
  if result > 1:
    result = 1
  elif result < -1:
    result = -1
  return result

def cross(v1,v2):
  return np.cross(v1,v2)

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1)*length(v2)))

def compare2angleList(angle1, angle2):
  if len(angle1) != len(angle2):
    return True
  for i in range(len(angle1)):
    if angle1[i] != angle2[i]:
      return True
  return False

def receive_socket_thread_function():
    message, address = receive_socket.recvfrom(1024)
    msg = message.decode().split(";")
    jRot = [msg[0], msg[1], msg[2], msg[3], msg[4], msg[5]]
    jPos = [msg[6], msg[7], msg[8], msg[9], msg[10], msg[11]]
    rpm = [msg[12], msg[13], msg[14], msg[15], msg[16], msg[17]]
    torque = [msg[18], msg[19], msg[20], msg[21], msg[22], msg[23]]
    print(jRot, jPos, rpm, torque)
    print(address)

while True:
  try:
    response = device_get(DEVICE_ID, token)
    isAnyAngleChanged = False
    if 'joint_list' in response:
      response_joint_list = response['joint_list']
      response_angle = json.loads(response_joint_list)['angle']
      isAnyAngleChanged = compare2angleList(response_angle, current_angle)

      send_ = str(response_angle[0])+';'+str(response_angle[1])+';'+str(response_angle[2])+';'+str(response_angle[3])+';'+str(response_angle[4])+';'+str(response_angle[5])
      print(send_)

      current_angle = response_angle

      if isAnyAngleChanged:
        send_socket.sendto((str(send_)).encode(), (UDP_IP,UDP_SEND_PORT))
        print("thread created!")
        receive_socket_thread = threading.Thread(target=receive_socket_thread_function)
        receive_socket_thread.daemon = True 
        receive_socket_thread.start()
      
  except (KeyboardInterrupt, SystemExit):
    sys.exit()