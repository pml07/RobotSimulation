import cv2

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 影像寬度
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 影像高度
fps = int(cap.get(cv2.CAP_PROP_FPS))  # fps

### save realtime video
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('1209_tpose.avi', fourcc, 5.0, (width, height))
while True:
  ret, img = cap.read()
  if not ret:
    break

  imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  out.write(img)
  cv2.imshow('Robot Arm', img)
    
  key = cv2.waitKey(1)
  if key == 27:  # esc
    cv2.destroyAllWindows()
    break

cap.release()
out.release()