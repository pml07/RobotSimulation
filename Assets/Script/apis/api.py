import requests
from config import ROS_API_BASE_URL

ROS_API_URL = ROS_API_BASE_URL + "/api/v1/"

def login(data):
  url = ROS_API_URL + 'auth/login'
  r = requests.post(url, json = data)
  return r.json()['access_token']

def device_add_to_db(data, token):
  url = ROS_API_URL + 'device'
  r = requests.post(url, json = data, headers={"Content-Type":"application/json", "Authorization": f"Bearer {token}"})
  return r.json()['id']

def device_update_action_to_db(id, data, token):
  url = ROS_API_URL + 'device/'+str(id)+'/action'
  r = requests.patch(url, json = data, headers={"Content-Type":"application/json", "Authorization": f"Bearer {token}"})
  return r.json()