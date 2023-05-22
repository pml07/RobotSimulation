import numpy as np
import math
import os
import json
import sys
import asyncio
import websockets
from apis.api import login, device_add, device_get, device_patch
from dotenv import load_dotenv

load_dotenv('.env')
### websocket
HOST_IP = os.getenv('HOST_IP','127.0.0.1')
HOST_PORT = int(os.getenv('HOST_PORT',5065))
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

async def ws_echo_function(websocket):
    while True:
      await ws_send(websocket)
      try:
          await ws_recv(websocket)
      except websockets.ConnectionClosedOK:
          print("websockets ConnectionClosedOK error")
          pass

async def ws_send(websocket):
  try:
    response = device_get(DEVICE_ID, token)
    isActionChanged = False
    action_type = 'move' 
    if 'action' in response:
      action_type = response['action']

    if action_type == 'move' and 'joint_list' in response:
      response_joint_list = response['joint_list']
      response_angle = json.loads(response_joint_list.replace("'", "\""))['angle']
      global current_angle
      isActionChanged = compare2angleList(response_angle, current_angle)

      send_ = ';'.join(str(angle) for angle in response_angle)
      print(send_)

      current_angle = response_angle
    elif action_type == 'clear_alarm':
       print(action_type)
       send_ = 'clear_alarm'
       isActionChanged = True

    if isActionChanged:
      try:
        await websocket.send(str(send_))
        print("ws_sent")
      except websockets.ConnectionClosedOK:
        print("websockets ConnectionClosedOK error")
      await asyncio.sleep(0.1)

  except (KeyboardInterrupt, SystemExit):
    sys.exit()

async def ws_recv(websocket):
    try:
        message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
        print("reveive data:" + message)
        data = json.loads(message)
        alarm_code = data.get("alarm_code", None)
        if alarm_code != None:
           print(alarm_code)
           response = device_get(DEVICE_ID, token)
           device_patch(DEVICE_ID, {
              "name": response["name"],
              "brand": response["brand"],
              "ip": response["ip"],
              "port": response["port"],
              "alarm_message": alarm_code
              }, token)

        if "jointAngles" in data:
          jRot = data["jointAngles"]
          jPos = data["jointPos"]
          rpm = data["rpms"]
          torque = data["torqueValues"]
          print(jRot, jPos, rpm, torque)
    except asyncio.TimeoutError:
        print("No Data reveived")
    await asyncio.sleep(0.1)

async def ws_main():
    print("ws_main")
    async with websockets.serve(ws_echo_function, HOST_IP, HOST_PORT):
      await asyncio.Future() 

asyncio.run(ws_main())