import cv2
import mediapipe as mp
import socket
import time
import numpy as np
import math

# socket
UDP_IP = '127.0.0.1'
UDP_PORT = 5065
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# angle
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def cross(v1,v2):
  return np.cross(v1,v2)

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

# mediapipe
cap = cv2.VideoCapture(0)
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False, model_complexity=1)

mpDraw = mp.solutions.drawing_utils
poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 0), thickness=3)
poseConStyle = mpDraw.DrawingSpec(color=(255, 255, 255), thickness=5)

# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 影像寬度
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 影像高度
# fps = int(cap.get(cv2.CAP_PROP_FPS))  # fps

angle1 = 0
a1_last = 0
a1_f = 0
angle2 = 0
a2_last = 0
a2_f = 0
angle3 = 90  # Tpose
a3_last = 0
a3_f = 0
angle4 = 0
a4_last = 0
a4_f = 0
angle5 = 0
a5_last = 0
a5_f = 0
angle6 = 0
a6_last = 0
a6_f = 0

### save realtime video
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('1207_1_tpose.avi', fourcc, 5.0, (640, 480))
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
    send_switch = 0    
    
    # 11: lshoulder / 12: rshoulder / 13: elbow / 15: wrist / 21: thumb / 17: pinky / 19: index / 23: hip
    # 肩膀->手肘
    arm = (joint_list[13][0]-joint_list[11][0], joint_list[13][1]-joint_list[11][1], joint_list[13][2]-joint_list[11][2])
    # 手肘->手腕
    forearm = (joint_list[15][0]-joint_list[13][0], joint_list[15][1]-joint_list[13][1], joint_list[15][2]-joint_list[13][2])
    # 右左肩
    shoulder = (joint_list[11][0]-joint_list[12][0], joint_list[11][1]-joint_list[12][1], joint_list[11][2]-joint_list[12][2])
    # 食指
    index = (joint_list[19][0]-joint_list[15][0], joint_list[19][1]-joint_list[15][1], joint_list[19][2]-joint_list[15][2])
    # 小指
    pinky = (joint_list[17][0]-joint_list[15][0], joint_list[17][1]-joint_list[15][1], joint_list[17][2]-joint_list[15][2])
    # 手肘->食指 
    elb_ind = (joint_list[19][0]-joint_list[13][0], joint_list[19][1]-joint_list[13][1], joint_list[19][2]-joint_list[13][2])
    # 手肘->拇指 
    elb_thu = (joint_list[21][0]-joint_list[13][0], joint_list[21][1]-joint_list[13][1], joint_list[21][2]-joint_list[13][2])
    # 肩膀->骨盆
    hip_shou = (joint_list[11][0]-joint_list[23][0], joint_list[11][1]-joint_list[23][1], joint_list[11][2]-joint_list[23][2])
    
    x = (1,0,0)
    y = (0,0,1)
    z = (0,0,1)
    
    if joint_list[11][3] > 0.8 and joint_list[13][3] > 0.8 and joint_list[15][3] > 0.8:
      # J3角度
      J3 = round(math.degrees(angle(arm, forearm)),3)
      angle3 = J3 + 90
      # print(angle3)
      if 0 <= abs(angle3) <= 60:
        angle6 = 0
      elif 60 < abs(angle3) <= 120:
        # 食指小指平面法向量
        in_pin = cross(index, pinky)
        angle6 = round(math.degrees(angle((0,in_pin[1],in_pin[2]),z)),3)
      # 手腕J5
      angle5 = round(math.degrees(angle(forearm,index)),3)
      # J2角度
      angle2 = round(math.degrees(angle((shoulder[0],shoulder[1],0),(arm[0],arm[1],0))),3)
      # J2方向
      # print(angle2)
      in_pin = cross(index, pinky)
      angle4 = round(math.degrees(angle((0,in_pin[1],in_pin[2]),z)),3)
      arm_fore = cross((-arm[0],-arm[1],-arm[2]),forearm)
      # J4角度
      J4 = round(math.degrees(angle(in_pin,arm_fore)),3)
      # J4方向
      cross_hand_elb = cross(in_pin,arm_fore)
      dir_hand_elb = dotproduct(cross_hand_elb,(-forearm[0],-forearm[1],-forearm[2]))
      dir_hand_elb /= abs(dir_hand_elb)
      angle4 = J4*dir_hand_elb
      # J1角度
      J1 = round(math.degrees(angle((0,arm_fore[1],arm_fore[2]),(0,hip_shou[1],hip_shou[2]))),3)
      # J1方向
      cross_arm_fore = cross(arm_fore,(hip_shou[0],hip_shou[1],hip_shou[2]))
      dir_arm_fore = dotproduct(cross_arm_fore,arm)
      dir_arm_fore /= abs(dir_arm_fore)
      angle1 = J1*dir_arm_fore
      print(angle1)


# J1: -165~+165
    if angle1 > 165:
      angle1 = 165
    elif angle1 < -165:
      angle1 = -165
    if abs(abs(angle1)-abs(a1_last)) <= 0.5:
      pass
    else:
      a1_f = angle1
      send_switch +=1
    a1_last = angle1
# J2: -125~+85 ->70
    if angle2 > 70:
      angle2 = 70
    elif angle2 < -110:
      angle2 = -110
    if abs(abs(angle2)-abs(a2_last)) <= 0.5:
      pass
    else:
      a2_f = angle2
      send_switch +=1
    a2_last = angle2
# J3: -55~+185
    if angle3 > 185:
      angle3 = 185
    elif angle3 < -55:
      angle3 = -55
    if abs(abs(angle3)-abs(a3_last)) <= 0.5:
      pass
    else:
      a3_f = angle3
      send_switch +=1
    a3_last = angle3  
# J4: -190~+190
    if angle4 > 190:
      angle4 = 190
    elif angle4 < -190:
      angle4 = -190
    if abs(abs(angle4)-abs(a4_last)) <= 0.5:
      pass
    else:
      a4_f = angle4
      send_switch +=1
    a4_last = angle4
# J5: -115~+115
    if angle5 > 115:
      angle5 = 115
    elif angle5 < -115:
      angle5 = -115
    if abs(abs(angle5)-abs(a5_last)) <= 0.5:
      pass
    else:
      a5_f = angle5
      send_switch +=1
    a5_last = angle5
# J6: -360~+360
    if angle6 > 165:
      angle6 = 165
    elif angle6 < -165:
      angle6 = -165
    if abs(abs(angle6)-abs(a6_last)) <= 0.5:
      pass
    else:
      a6_f = angle6
      send_switch +=1
    a6_last = angle6

    send_ = str(a1_f)+'?'+str(a2_f)+'?'+str(a3_f)+'?'+str(a4_f)+'?'+str(a5_f)+'?'+str(a6_f)
    print(send_)
    if send_switch > 0:
      socket.sendto((str(send_)).encode(),(UDP_IP,UDP_PORT))
    time.sleep(0.1)

  out.write(img)
  cv2.imshow('Robot Arm', img)
    
  key = cv2.waitKey(1)
  if key == 27:  # esc
    cv2.destroyAllWindows()
    break

cap.release()
out.release()