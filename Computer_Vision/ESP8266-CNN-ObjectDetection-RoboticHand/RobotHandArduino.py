# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 17:40:25 2021

@author: DiegoDiazGarciaDev
"""

import cv2
from tensorflow.keras.models import load_model
import requests
import threading
import numpy as np
from tensorflow.keras.preprocessing import image

#flag in case we are going to use our ESP8266 connected to the robot hand
ESP8266 = True

#We load the CNN model
new_model = load_model('./model/hand_100epochs.h5')

# This background will be a global variable that we update through a few functions
background = None

# Start with a halfway point between 0 and 1 of accumulated weight
accumulated_weight = 0.5


# Manually set up our ROI for grabbing the hand.
# Feel free to change these. I just chose the top right corner for filming.
roi_top = 20
roi_bottom = 300
roi_right = 300
roi_left = 600

#roi_top, roi_right, roi_bottom, roi_left = 110, 350, 325, 590


def calc_accum_avg(frame, accumulated_weight):
    '''
    Given a frame and a previous accumulated weight, computed the weighted average of the image passed in.
    '''
    
    # Grab the background
    global background
    
    # For first time, create the background from a copy of the frame.
    if background is None:
        background = frame.copy().astype("float")
        return None

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(frame, background, accumulated_weight)
    
    
    
    
def segment(frame, threshold=25):
    global background
    
    # Calculates the Absolute Differentce between the backgroud and the passed in frame
    diff = cv2.absdiff(background.astype("uint8"), frame)

    # Apply a threshold to the image so we can grab the foreground
    # We only need the threshold, so we will throw away the first item in the tuple with an underscore _
    _ , thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Grab the external contours form the image
    # Again, only grabbing what we need here and throwing away the rest
    
    #DDG he tenido que quitar el primer elemanto de retorno (image)
    contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If length of contours list is 0, then we didn't grab any contours!
    if len(contours) == 0:
        return None
    else:
        # Given the way we are using the program, the largest external contour should be the hand (largest by area)
        # This will be our segment
        hand_segment = max(contours, key=cv2.contourArea)
        
        # Return both the hand segment and the thresholded hand image

        return (thresholded, hand_segment)






lastPrediction = 99
def predicthand(thresholded, hand_segment):
    global lastPrediction
    
    #{'Fist': 0, 'Palm': 1, 'Swing': 2}

    hand_file = './data/Temp.png'
    hand_file = image.load_img(hand_file, target_size=(89, 100))
    hand_file = image.img_to_array(hand_file)
    hand_file = np.expand_dims(hand_file, axis=0)
    hand_file = hand_file/255
    
    prediction_class = new_model.predict_classes(hand_file)
    prediction = new_model.predict(hand_file)

    # {'Fist': 0, 'Palm': 1, 'Swing': 2}

    #Detecion the type of gesture of the hand and sending this info to arduino depending on that

    # we don't do anything unless we are pretty sure with our prediction (95%)
    if np.amax(prediction) > 0.95:

            if prediction_class[0] == 0:
                t = threading.Thread(target=send_info, args=(0,lastPrediction))
                t.start()
               # send_info(0)
                lastPrediction=0
                return "Fist"
            elif prediction_class[0] == 1:
                t = threading.Thread(target=send_info, args=(1,lastPrediction))
                t.start()
                #send_info(1)
                lastPrediction = 1
                return "Palm"
            else:
                return "Swing"
    
    else:
        
        return "No identify"




#Servo initilizer
if ESP8266:
    pload = {"degree1": 0}
    r = requests.post('http://192.168.0.161/moveServo', json=pload)
  
def send_info(currentPrediction,lastPrediction):
    if ESP8266:
        if lastPrediction != currentPrediction:

            if currentPrediction==0:
                #pload = {"degree1": 10, "degree2": 170}
                pload = {"degree1": 115}
                r = requests.post('http://192.168.0.161/moveServo', json=pload)

            elif currentPrediction == 1:
                #pload = {"degree1":20,"degree2":100}
                pload = {"degree1":65}
                r = requests.post('http://192.168.0.161/moveServo',json = pload)


            print(r.status_code)

url='http://192.168.0.162:8080/shot.jpg'
#cam = cv2.VideoCapture(url)


cam = cv2.VideoCapture(0)

# Intialize a frame count
num_frames = 0

# recording flag. Use True if you need create your own hand dataSet.
start_recording = False
image_num = 0

# keep looping, until interrupted
while True:
    # get the current frame
    #cam = cv2.VideoCapture(url)
    ret, frame = cam.read()

    # flip the frame so that it is not the mirror view
    frame = cv2.flip(frame, 1)

    # clone the frame
    frame_copy = frame.copy()

    # Grab the ROI from the frame
    roi = frame[roi_top:roi_bottom, roi_right:roi_left]

    # Apply grayscale and blur to ROI
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # For the first 30 frames we will calculate the average of the background.
    # We will tell the user while this is happening
    if num_frames < 60:
        calc_accum_avg(gray, accumulated_weight)
        if num_frames <= 59:
            cv2.putText(frame_copy, "WAIT! GETTING BACKGROUND AVG.", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv2.imshow("Finger Count",frame_copy)
            
    else:
        # now that we have the background, we can segment the hand.
        
        # segment the hand region
        hand = segment(gray)

        # First check if we were able to actually detect a hand
        if hand is not None:
            
            # unpack
            thresholded, hand_segment = hand

            # Draw contours around hand segment
            cv2.drawContours(frame_copy, [hand_segment + (roi_right, roi_top)], -1, (255, 0, 0),1)

            # Count the fingers
            cv2.imwrite('./data/Temp.png', thresholded)
            #resizeImage('Temp.png')
            fingers = predicthand(thresholded, hand_segment)

            # Display count
            cv2.putText(frame_copy, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # Also display the thresholded image
            cv2.imshow("Thesholded", thresholded)
            
            
            if start_recording == True:
                    name_file = "Recordings/fist_" + str(image_num) + '.png'
                    cv2.putText(frame_copy, "Recording....", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    cv2.putText(frame_copy, name_file, (200, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
                    #cv2.imshow("recoding",frame_copy)
                    if image_num<100:
                       # Mention the directory in which you wanna store the images followed by the image name
                        
                        cv2.imwrite(name_file, thresholded)
                        
                        #We are recording every 5 frames
                        if num_frames%5 == 0:
                            image_num = image_num+1
                            print("image_num :",image_num)
                    else:
                        start_recording =False
                        cv2.putText(frame_copy, " ", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                   

    # Draw ROI Rectangle on frame copy
    cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), 5)

    # increment the number of frames for tracking
    num_frames += 1

    # Display the frame with segmented hand
    cv2.imshow("Finger Count", frame_copy)

   

    # Close windows with Esc
    k = cv2.waitKey(1) & 0xFF
    
    if k == ord("s"):
        start_recording = True

    if k == 27:
        break

# Release the camera and destroy all the windows
cam.release()
cv2.destroyAllWindows()
