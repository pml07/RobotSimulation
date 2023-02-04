import requests
from config import ROS_API_URL

BASE_URL = ROS_API_URL + "/api/v1/"

def login(data):
  url = BASE_URL + 'auth/login'
  r = requests.post(url, json = data)

  return r.json()['access_token']

def device_add(data, token):
  url = BASE_URL + 'device'
  r = requests.post(url, json = data, headers={"Content-Type":"application/json", "Authorization": f"Bearer {token}"})

  return r.json()['id']

def device_action(id, data, token):
  url = BASE_URL + 'device/'+str(id)+'/action'
  r = requests.patch(url, json = data, headers={"Content-Type":"application/json", "Authorization": f"Bearer {token}"})

  return r.json()