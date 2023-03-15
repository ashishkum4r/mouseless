import mediapipe as mp
import cv2
import numpy as np
import pyautogui
pyautogui.FAILSAFE = False

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
        return image, self.results.multi_hand_landmarks

    def positionFinder(self,image, handNo=0, draw=False):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            if draw:
                cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)
        return lmlist

def draw_rect(lmlist):
    upper_pt = min(lmlist[0][2], lmlist[1][2], lmlist[2][2], lmlist[3][2], lmlist[4][2], lmlist[5][2], lmlist[6][2], lmlist[7][2], lmlist[8][2], lmlist[9][2], lmlist[10][2], lmlist[11][2], lmlist[12][2], lmlist[13][2], lmlist[14][2], lmlist[15][2], lmlist[16][2], lmlist[17][2], lmlist[18][2], lmlist[19][2], lmlist[20][2])
    right_pt = max(lmlist[0][1], lmlist[1][1], lmlist[2][1], lmlist[3][1], lmlist[4][1], lmlist[5][1], lmlist[6][1], lmlist[7][1], lmlist[8][1], lmlist[9][1], lmlist[10][1], lmlist[11][1], lmlist[12][1], lmlist[13][1], lmlist[14][1], lmlist[15][1], lmlist[16][1], lmlist[17][1], lmlist[18][1], lmlist[19][1], lmlist[20][1])
    left_pt = min(lmlist[0][1], lmlist[1][1], lmlist[2][1], lmlist[3][1], lmlist[4][1], lmlist[5][1], lmlist[6][1], lmlist[7][1], lmlist[8][1], lmlist[9][1], lmlist[10][1], lmlist[11][1], lmlist[12][1], lmlist[13][1], lmlist[14][1], lmlist[15][1], lmlist[16][1], lmlist[17][1], lmlist[18][1], lmlist[19][1], lmlist[20][1])
    lower_pt = max(lmlist[0][2], lmlist[1][2], lmlist[2][2], lmlist[3][2], lmlist[4][2], lmlist[5][2], lmlist[6][2], lmlist[7][2], lmlist[8][2], lmlist[9][2], lmlist[10][2], lmlist[11][2], lmlist[12][2], lmlist[13][2], lmlist[14][2], lmlist[15][2], lmlist[16][2], lmlist[17][2], lmlist[18][2], lmlist[19][2], lmlist[20][2])
    return upper_pt, right_pt, left_pt, lower_pt

def rect_to_cam(x, y):
    x = x-80
    y = y-60
    # if x<320:
    #     x = x - 80
    # elif x>320:
    #     x = x + 80
    # if y<180:
    #     y = y - 60
    # elif y > 180:
    #     y = y + 180
    return x, y
def main():
    right_c = 0
    left_c = 0
    cap = cv2.VideoCapture(0)
    tracker = handTracker()
    width_cam = cap.get(cv2.CAP_PROP_FRAME_WIDTH)#640
    height_cam = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#480
    width_screen, height_screen = pyautogui.size()
    # cv2.createTrackbar('s', 'Video', 15, 255, nothing)
    p_x = 0
    p_y = 0

    while cap.isOpened():
        success,image = cap.read()
        image = cv2.flip(image, 1)
        cv2.rectangle(image, pt1=(80, 60), pt2=(560, 300), color=(255, 0, 0), thickness=1)
        image, multi_hand_landmarks = tracker.handsFinder(image)
        # print(multi_hand_landmarks)
        lmList = tracker.positionFinder(image)

        if len(lmList) != 0:
            upper_pt, right_pt, left_pt, lower_pt = draw_rect(lmList)
            if(-upper_pt+lower_pt>220):
                cv2.putText(image, 'Move Your Backwards', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 9, cv2.LINE_AA)
                # print('entered')
                # cv2.circle(image, (25, 25), 15, (255, 255, 255), cv2.FILLED)
            cv2.rectangle(image, pt1=(left_pt - 20, upper_pt - 20), pt2=(right_pt + 20, lower_pt + 20), color=(255, 0, 0), thickness=1)

            if(True):
                if(lmList[8][2]>lmList[5][2] and lmList[12][2]>lmList[9][2] and lmList[16][2]>lmList[13][2] and lmList[20][2]>lmList[17][2]):
                    pyautogui.scroll(300)
                    print('scroll_down')
                    left_c = 0
                    right_c = 0

                elif (lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[9][2] and lmList[16][2] > lmList[13][2] and lmList[20][2] > lmList[17][2] ):
                    x, y = rect_to_cam(lmList[8][1], lmList[8][2])
                    cv2.circle(image, (lmList[8][1], lmList[8][2]), 15, (255, 0, 255), cv2.FILLED)
                    x = x * 1920 / 460
                    y = y * 1080 / 220
                    # x = np.interp(lmList[8][1] - 80, (0, 480), (0, width_screen))
                    # y = np.interp(lmList[8][2] - 80, (0, 240), (0, height_screen))
                    print('move')
                    pyautogui.moveTo(x, y)
                    left_c = 0
                    right_c = 0

                elif (lmList[8][2] < lmList[5][2] and lmList[12][2] < lmList[9][2] and lmList[16][2] > lmList[13][2] and lmList[20][2] > lmList[17][2] and right_c!=1):
                    pyautogui.click(button='right')
                    print('right_c')
                    right_c = 1
                    left_c = 0


                elif (lmList[8][2] < lmList[5][2] and lmList[12][2] < lmList[9][2] and lmList[16][2] < lmList[13][2] and lmList[20][2] > lmList[17][2] and left_c!=1):
                    pyautogui.click(button='left')
                    print('left_c')
                    left_c = 1
                    right_c = 0


                elif (lmList[8][2] < lmList[5][2] and lmList[12][2] < lmList[9][2] and lmList[16][2] < lmList[13][2] and lmList[20][2] < lmList[17][2]):
                    pyautogui.scroll(-300)
                    print('scroll_up')
                    left_c = 0
                    right_c = 0

            #     if(lmList[12][2]>lmList[10][2] and lmList[16][2]>lmList[14][2] and lmList[20][2]>lmList[18][2]):
            #         index_fingure_up = 1
            #         # print('index fingure up')
            #         # pyautogui.click()
            #         x = np.interp(lmList[8][1] - 80, (0, 400), (0, width_screen))
            #         y = np.interp(lmList[8][2] - 80, (0, 280), (0, height_screen))
            #         c_x = p_x + (x-p_x)/100000
            #         c_y = p_y + (y-p_y)/100000
            #         pyautogui.moveTo(c_x, c_y)
            #         p_x = x
            #         p_y = y
            #         cv2.circle(image, (lmList[8][1], lmList[8][2]), 15, (255, 0, 255), cv2.FILLED)
            # if (lmList[12][1] - lmList[20][1] <= 20 and lmList[12][2] - lmList[20][2] <= 20 and lmList[4][1] - lmList[16][1] <= 0 and lmList[4][2] - lmList[16][2] <= 20):
            #     pyautogui.click(button='right')
            # elif (lmList[12][2] - lmList[16][2] <= 30 and lmList[12][1] - lmList[16][1] <= 30 and lmList[4][1] - lmList[20][1] <= 15 and lmList[4][2] - lmList[20][2] <= 15):
            #     pyautogui.click(button='left')
            # elif (lmList[4][1] - lmList[17][1] <= 10 and lmList[4][2] - lmList[17][2] <= 10):
            #     pyautogui.scroll(-300)
            # elif (lmList[4][1] - lmList[8][1] <= 10 and lmList[4][2] - lmList[8][2] <= 10):
            #     pyautogui.scroll(300)

        cv2.imshow("Video",image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

