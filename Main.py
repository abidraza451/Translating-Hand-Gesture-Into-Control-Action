import cv2
import mediapipe as mp
import numpy as np
import time
import webbrowser
import subprocess
import math
from pynput.keyboard import Controller
from VirtualKeyboard import keyprint
# checking hand Orientation 
def checkOrientation(landmarks_list1):
    if landmarks_list1[3][0] > landmarks_list1[17][0]:
        """ when x-coordinate of 3rd index(thumb)is greater than 17th index(pinky)"""
        if (landmarks_list1[0][1] > landmarks_list1[12][1]):
            """Upside orientate """
            return ("left","upside")
        else:
            """else it will be right hand properties which is upside down"""
            return ("right","downside")
    else:
        if (landmarks_list1[0][1] > landmarks_list1[12][1]):
            """#upright left hand 1"""
            return ("right","upside")
        else:
            """#upside down right hand 1"""
            return ("left","downside") 

# checking thumb Orientation  
def thumb(fing,coordinate,side,orient):
    axis =0
    if orient == "upside":
        upper = 0
        lower = 1
    else:
        upper = 1
        lower = 0
    tip = coordinate[fing[upper]][axis]
    base = coordinate[fing[lower]][axis]
    if side == "left":
        if tip > base:
            return 0
        return 1
    else:
        if tip < base:
            return 0
        return 1

# checking fingers Orientation
def checkUp(fing , coordinate,orient):
    axis = 1
    if orient == "upside":
        upper = 0
        lower = 1
    else:
        upper = 1
        lower = 0

    tip = coordinate[fing[upper]] [axis]
    base = coordinate[fing[lower]][axis]
    if tip > base:
        return 1
    return 0

    status_right[idx] = checkUp(val, coordinatelist, orient=handle[1])

# checking calling command is available or not in our list of command
def check_availableCommand(val):
    if val in command_function_identification.values():
        return True
    return False

# assigning a key to each command 
def get_key(val, my_command):
    for key, value in my_command.items():
        if val == value:
            return key

# fire up the function that is associated with command
def fire_function(val):
    comm = get_key(val, command_function_identification)
    comm()
   

# defining commands
def command1():
    print("Opening YouTube")
    webbrowser.open('http://www.youtube.com')

def command2():
    print("Opening Notepad")
    subprocess.Popen("C:\\Windows\\notepad.exe")

def command3():
    print("Opening Calculator")
    subprocess.Popen("calc.exe")

def command4():
    print("Running virtual keyboard")
    keyprint()

    

# command dictionary
command_function_identification = {
    command1: [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    command2: [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    command3: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    command4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
}

coordinate = {val: (0, 0) for val in range(0, 21)}
finger_val = [(4, 2), (8, 6), (12, 10), (16, 14), (20, 18)]
coordinatelist = {val: (0, 0) for val in range(0, 21)}
command_call = [[0], [0]]

keyboard_visible = False



cap = cv2.VideoCapture(0)
cap.set(3,1280)


mphands = mp.solutions.hands
hands = mphands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

while cap.isOpened():
    status_left = [0 for _ in finger_val]
    status_right = [0 for _ in finger_val]
    success, img = cap.read()
    height, width, channel = img.shape
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mphands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                coordinatelist[id] = (cx, cy)
            handle = checkOrientation(coordinatelist)

            if handle[0] == 'right':
                for idx, val in enumerate(finger_val):
                    if idx == 0:
                        status_right[idx] = thumb(val, coordinatelist, side="right", orient=handle[1])
                    else:
                        status_right[idx] = checkUp(val, coordinatelist, orient=handle[1])
            elif handle[0] == 'left':
                for idx, val in enumerate(finger_val):
                    if idx == 0:
                        status_left[idx] = thumb(val, coordinatelist, side="left", orient=handle[1])
                    else:
                        status_left[idx] = checkUp(val, coordinatelist, orient=handle[1])
                status_left.reverse()

            cv2.putText(img, f'{handle}', coordinatelist[0], cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

    cv2.putText(img, "Command " + str(status_left + status_right), (0, 400), cv2.FONT_HERSHEY_PLAIN, 1.4, (255, 0, 0), 2)

    combicommand = status_left + status_right

    # accessing Command
    if combicommand != command_call[1]:
        command_call[1] = combicommand

        if command_call[0] != command_call[1]:
            print("both", command_call[0], command_call[1])

            if check_availableCommand(command_call[0]):
                fire_function(command_call[0])
            else:
                print("On this sign, we don't have an action")

            command_call[0] = command_call[1]
            command_call[1] = command_call[0]
       

    cv2.imshow('I1', img) 
    if cv2.waitKey(1) == ord('s'):
        cv2.destroyWindow('I1')
        break
