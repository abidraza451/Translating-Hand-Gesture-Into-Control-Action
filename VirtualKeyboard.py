import cv2
import math
from time import sleep
from pynput.keyboard import Controller

from cvzone.HandTrackingModule import HandDetector
def keyprint():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)

    detector = HandDetector(detectionCon=0.8, maxHands=2)

    keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            ["space", "enter", "bspace","Caps"]  
            ]
    def change_keys(keys):
        if keys == [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                   ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                   ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                   ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
                   ["space", "enter", "bspace", "Caps"]
            ]:
            keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
                    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
                    ["space", "enter", "bspace", "Caps"]
                    ]
            return keys
        else:
            keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
                    ["space", "enter", "bspace", "Caps"]
                    ]
            return keys        

    keyboard = Controller()
    def drawAll(img, buttonList):
        for i, button in enumerate(buttonList):
            x, y = button.pos
            w, h = button.size
            if button.text in ["space", "enter", "bspace","Caps"]:
                font_scale = .56  
                boldness = 1
                color =(0, 0, 0)
            else:
                font_scale = 2.0  
                boldness = 3
                color =(255, 0, 0)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 4)  
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, boldness)
        return img


    class Button():
        def __init__(self, pos, text, size=[85, 85]):
            self.pos = pos
            self.size = size
            self.text = text

    def myexit():
        cv2.destroyWindow('I2')


    buttonList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


    while cap.isOpened():
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)
        img = drawAll(img, buttonList)

        cv2.rectangle(img, (1050, 50), (1250, 130), (255, 0, 255), 4)
        cv2.putText(img, "exit", (1050, 120), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

        if hands:
            hand1 = hands[0]
            lmList1 = hand1["lmList"]
            bbox1 = hand1["bbox"]
            centerPoint1 = hand1["center"]
            handType = hand1["type"]

            if lmList1:
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 25, y + 75), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

                        x1, y1 = lmList1[8][0], lmList1[8][1]  # Landmark 8
                        x2, y2 = lmList1[6][0], lmList1[6][1]  # Landmark 12

                        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                        top_left = (bbox1[0], bbox1[1])
                        bottom_left = (bbox1[0], bbox1[1] + bbox1[3])
                        distance = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)
                        percentage = (length * 100) / distance
                        print(percentage)

                        if 17 <= percentage < 20:
                            if button.text == "enter":
                                keyboard.press('\n')
                                sleep(0.40)
                                keyboard.release('\n')
                            elif button.text == "bspace":
                                keyboard.press('\b')
                                sleep(0.40)
                                keyboard.release('\b')
                            elif button.text == "space":  
                                keyboard.press(' ')
                                sleep(0.40)
                                keyboard.release(' ')    
                            elif button.text == "Caps":
                                keys = change_keys(keys)
                                buttonList = []
                                for i in range(len(keys)):
                                    for j, key in enumerate(keys[i]):
                                        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
                                sleep(0.40)      
                            else:
                                keyboard.press(button.text)
                                sleep(0.40)
                                keyboard.release(button.text)

                    elif 1050 < lmList1[8][0] < 1250 and 50 < lmList1[8][1] < 130:
                        cv2.rectangle(img, (1050, 50), (1250, 130), (255, 0, 255), cv2.FILLED)
                        cv2.putText(img, "exit", (1050, 120), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        x1, y1 = lmList1[8][0], lmList1[8][1]  # Landmark 8
                        x2, y2 = lmList1[6][0], lmList1[6][1]  # Landmark 12

                        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                        top_left = (bbox1[0], bbox1[1])
                        bottom_left = (bbox1[0], bbox1[1] + bbox1[3])
                        distance = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)
                        percentage = (length * 100) / distance
                        print(percentage)

                        if 17 <= percentage < 20: 
                            myexit()

        cv2.imshow('I2', img)
        if cv2.waitKey(1) & 0xFF == ord('r'):
            cv2.destroyWindow('I2')
            break
