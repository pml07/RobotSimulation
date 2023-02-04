import os
from dotenv import load_dotenv

load_dotenv('.env')
### socket
UDP_IP = os.getenv('UDP_IP','127.0.0.1')
UDP_PORT = int(os.getenv('UDP_PORT',5055))
ROS_API_URL = os.getenv('ROS_API_URL','http://localhost')

USER_DATA = {
  "email": os.getenv('USER_EMAIL', 'user'),
  "password": os.getenv('USER_PASSWORD', 'user')
}
DEVICE_DATA = {
  "name": os.getenv('DEVICE_NAME','device_from_robotSim')
}
