import cv2
import mediapipe as mp
import socket
import numpy as np
import math

### socket
UDP_IP = '127.0.0.1'
UDP_SEND_PORT = 5065
UDP_RECEIVE_PORT = 5066

send_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.bind((UDP_IP, UDP_RECEIVE_PORT))

angle1, a1_last, a1_f = 0, 0, 0
angle2, a2_last, a2_f = 0, 0, 0
angle3, a3_last, a3_f = 0, 0, 0
angle4, a4_last, a4_f = 0, 0, 0
angle5, a5_last, a5_f = 0, 0, 0
angle6, a6_last, a6_f = 0, 0 ,0

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


## mediapipe
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False, model_complexity=1)

mpDraw = mp.solutions.drawing_utils
poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 0), thickness=3)
poseConStyle = mpDraw.DrawingSpec(color=(255, 255, 255), thickness=5)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 影像寬度
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 影像高度



## save realtime video
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('0715_2.avi', fourcc, 15.0, (width, height))
while True:
  ret, img = cap.read()
  if not ret:
    break

  imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  result = pose.process(imgRGB)

  if result.pose_landmarks:
    mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
    joint = ''
    joint_list = []
    for data_point in result.pose_landmarks.landmark:
      point_list = []
      point_list.append(round(float(data_point.x), 3))
      point_list.append(round(float(data_point.y), 3))
      point_list.append(round(float(data_point.z), 3))
      point_list.append(round(float(data_point.visibility), 3))
      joint_list.append(point_list)
    send_1 = 0
    send_2 = 0
    send_3 = 0
    send_4 = 0
    send_5 = 0

    # 11: lshoulder / 12: rshoulder / 13: elbow / 15: wrist / 21: thumb / 17: pinky / 19: index / 23: hip
    # 肩膀->手肘
    arm = (joint_list[13][0]-joint_list[12][0], joint_list[13][1]-joint_list[12][1], joint_list[13][2]-joint_list[12][2])
    # 手肘->手腕
    forearm = (joint_list[15][0]-joint_list[13][0], joint_list[15][1]-joint_list[13][1], joint_list[15][2]-joint_list[13][2])
    # 左右肩
    shoulder = (joint_list[11][0]-joint_list[12][0], joint_list[11][1]-joint_list[12][1], joint_list[11][2]-joint_list[12][2])
    # 食指
    index = (joint_list[19][0]-joint_list[15][0], joint_list[19][1]-joint_list[15][1], joint_list[19][2]-joint_list[15][2])
    # 小指
    pinky = (joint_list[17][0]-joint_list[15][0], joint_list[17][1]-joint_list[15][1], joint_list[17][2]-joint_list[15][2])
    # 手肘->食指 
    elbow_index = (joint_list[19][0]-joint_list[13][0], joint_list[19][1]-joint_list[13][1], joint_list[19][2]-joint_list[13][2])
    # 手肘->拇指 
    elbow_thumb = (joint_list[21][0]-joint_list[13][0], joint_list[21][1]-joint_list[13][1], joint_list[21][2]-joint_list[13][2])
    # 肩膀->骨盆
    hip_shou = (joint_list[12][0]-joint_list[23][0], joint_list[12][1]-joint_list[23][1], joint_list[12][2]-joint_list[23][2])


    #### calculate angle
    if joint_list[12][3] > 0.8 and joint_list[13][3] > 0.8 and joint_list[15][3] > 0.8:
      index_pinky = cross(index, pinky)
      arm_fore = cross((-arm[0],-arm[1], -arm[2]), forearm)
      
      # J1角度
      J1 = round(math.degrees(angle((arm[0], 0, arm[2]), (1, 0, 0))), 3)
      # J1方向 
      dir_a1 = dotproduct((0, 0, arm[2]), (0, 0, 1))
      if dir_a1 != 0:
        dir_a1 /= abs(dir_a1)
        angle1 = J1*dir_a1
      else:
        angle1 = J1*dir_a1
      # J1: -165~+165
      if angle1 > 163:
        angle1 = 163
      elif angle1 < -163:
        angle1 = -163
      else:
        pass
      if abs(abs(angle1)-abs(a1_last)) <= 1:
        pass
      else:
        a1_f = angle1
        send_1 += 1
      a1_last = angle1

      # J2角度: -125 ~ +85->70
      J2 = round(math.degrees(angle((shoulder[0], shoulder[1], 0),(arm[0], arm[1], 0))), 1)
      # J2方向
      if joint_list[13][1] > joint_list[12][1]:
        angle2 = -J2
      elif joint_list[13][1] <= joint_list[12][1]:
        angle2 = J2

      if angle2 > 70:
        angle2 = 70
      elif angle2 < -60:
        angle2 = -60
      else:
        pass
      if abs(abs(angle2)-abs(a2_last)) <= 1:
        send_2 = 0
      else:
        a2_f = angle2
        send_2 += 1
      a2_last = angle2

      # J3角度: -55 ~ +185
      J3 = round(math.degrees(angle((arm[0], arm[1], 0), (forearm[0], forearm[1], 0))), 1)
      # J3方向
      if joint_list[15][1] < joint_list[13][1]:
        angle3 = J3 + 90
      elif joint_list[15][1] >= joint_list[13][1]:
        angle3 = -J3 + 90

      if angle3 > 180:
        angle3 = 180
      elif angle3 < -45:
        angle3 = -45
      else:
        pass
      if abs(abs(angle3)-abs(a3_last)) <= 1:
        send_3 = 0
      else:
        a3_f = angle3
        send_3 += 1
      a3_last = angle3
      
      # J4角度: -190 ~ +190
      J4 = round(math.degrees(angle(index_pinky, arm_fore)), 1)
      # J4方向
      if J4 == 0:
        angle4 = -J4
      elif J4 == 180:
        angle4 = J4
      else:  
        cross_hand_elb = cross(index_pinky, arm_fore)
        dir_a4 = dotproduct(cross_hand_elb, forearm)
        dir_a4 /= abs(dir_a4)
        angle4 = J4*dir_a4

      if angle4 > 90:
        angle4 = 90
      elif angle4 < -90:
        angle4 = -90
      else:
        pass
      if abs(abs(angle4)-abs(a4_last)) <= 1:
        pass
      else:
        a4_f = angle4
        send_4 += 1
      a4_last = angle4
      
      # J5角度: -115 ~ +115
      J5 = round(math.degrees(angle(forearm, index)),1)
      # J5方向
      if joint_list[19][1] >= joint_list[15][1]:
        angle5 = -J5
      elif joint_list[19][1] < joint_list[15][1]:
        angle5 = J5

      if angle5 > 110:
        angle5 = 110
      elif angle5 < -110:
        angle5 = -110
      else:
        pass
      if abs(abs(angle5)-abs(a5_last)) <= 1:
        pass
      else:
        a5_f = angle5
        send_5 += 1
      a5_last = angle5

      # J6
      angle6 = 0
      a6_f = angle6
      a6_last = angle6

    send_ = str(a1_f)+';'+str(a2_f)+';'+str(a3_f)+';'+str(a4_f)+';'+str(a5_f)+';'+str(a6_f)
    if send_2 and send_3 and send_5 > 0:
      send_socket.sendto((str(send_)).encode(), (UDP_IP,UDP_SEND_PORT))
      print('-----send:', send_)
      send_switch = 0
      # message, address = receive_socket.recvfrom(1024)
      # msg = message.decode().split(";")
      # jRot = [msg[0], msg[1], msg[2], msg[3], msg[4], msg[5]]
      # print("receive: ", jRot)
      with open('0715_2.txt', 'a') as file:
        file.write(send_)
        file.write('\n')

  out.write(img)
  cv2.imshow('Robot Arm', img)
    
  key = cv2.waitKey(1)
  if key == 27:  # esc
    cv2.destroyAllWindows()
    break

cap.release()
out.release()