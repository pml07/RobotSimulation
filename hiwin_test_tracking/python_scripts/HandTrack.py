import cv2
import mediapipe as mp

import socket
import time

UDP_IP = '127.0.0.1'
UDP_PORT = 5065

socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def justremap(input, input_domain=(0,1), output_domain=(0,1)):
    return (input - input_domain[0])*(output_domain[1]-output_domain[0])/(input_domain[1]-input_domain[0]) + output_domain[0]

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self,image,draw=True):

        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self,image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([cx,cy])

               

        return lmlist
    
def main():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()

    while True:
        success,image = cap.read()
        if success:
            image = tracker.handsFinder(image)
            lmList = tracker.positionFinder(image)
        else:
            print("failed to capture")
            break

        if len(lmList) != 0:
            cv2.circle(image,lmList[8],5,(0,255,80), cv2.FILLED)

            if(lmList[8][0] > 0 and lmList[8][0] < 650 and lmList[8][1] > 0 and lmList[8][1] < 425):

                a_one =  round(justremap(lmList[8][0],(0,650),(-60,-30)),2)
                a_three = round(justremap(lmList[8][1],(0,425),(-10,-55)),2)

                send_ = str(a_one)+'?'+str(a_three)
                socket.sendto((str(send_)).encode(),(UDP_IP,UDP_PORT))

        cv2.imshow("Video",image)
        cv2.waitKey(1)
        time.sleep(0.085)
        
        

if __name__ == "__main__":
    
    main()