import os
from dotenv import load_dotenv

load_dotenv('.env')
### socket
UDP_IP = os.getenv('UDP_IP','127.0.0.1')
UDP_SEND_PORT = os.getenv('UDP_SEND_PORT', 5060)
UDP_RECEIVE_PORT = os.getenv('UDP_RECEIVE_PORT', 5061)
ROS_API_BASE_URL = os.getenv('ROS_API_BASE_URL','http://localhost')
IMPORT_FILE_NAME = os.getenv('IMPORT_FILE_NAME','../Data/angle_0.json')

USER_DATA = {
  "email": os.getenv('USER_EMAIL', 'user'),
  "password": os.getenv('USER_PASSWORD', 'user')
}
DEVICE_DATA = {
  "name": os.getenv('DEVICE_NAME','device_from_robotSim')
}
