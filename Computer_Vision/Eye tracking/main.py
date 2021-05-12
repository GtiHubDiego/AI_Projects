import cv2
import cvzone
import numpy as np
import resources.keys as k
import time
import autopy

# Loading the model created for the eyes movement
from tensorflow.keras.models import load_model
# CNN Model created with a Dataset of pics of my own eyes
# We have 5 classes but we will be using only 2 (movement left, movement right)
new_model = load_model('model/50epochs_5classes.h5')

wScr, hScr = autopy.screen.size()
#print(wScr, hScr)
pTime = 0
keys = k.Keys()



#This function receive a frame (just eyes), and after doing the normalization and setting the correct dimensiones we pass
#the frame to our CNN model previously created so that we will be able to predict if we are looking to the
#right , to the left or to other side.
def readingEye(frame):
    eye_file = frame
    eye_file = eye_file / 255
    eye_file = np.expand_dims(eye_file, axis=0)
    prediction_class = new_model.predict_classes(eye_file)
    prediction = new_model.predict(eye_file)

    # { Other eye position: 0, Right blink: 1, Left blink: 2, Eyes moving right: 3, Eyes moving left: 4}

    # We are just using 2 classes for this project
    # if the prediction is good enough we will be moving the Mouse on the direction selected and
    # we will be pressing a keyboard key (virtually)
    if np.amax(prediction) > 0.95:
        # RIGHT
        if prediction_class[0] == 3:
            keys.directKey("r")
            x = autopy.mouse.location()[0]
            y = autopy.mouse.location()[1]
            if (x + 30) < wScr:
                autopy.mouse.move(x + 15, y)
        # LEFT
        elif prediction_class[0] == 4:
            keys.directKey("l")
            x = autopy.mouse.location()[0]
            y = autopy.mouse.location()[1]
            if (x-30) > 0:
                autopy.mouse.move(x - 15, y)


#We start the web cam
cap = cv2.VideoCapture(0)
#We instance FaceMeshDetector
detector = cvzone.FaceMeshDetector(maxFaces=1)
#We set eyes_on flag to True so that we can use the eyes movement ( we could disable and enable it pressing the 'e' key)
eyes_on = True

while (True):
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    image_new = img.copy()
    img, faces = detector.findFaceMesh(img)

    #left eye landmarks
    leye = [130,30,29,28,27,56,190,243,112,26,22,23,24,110,25,33,246,161,160,159,158,157,173,133,155,154,153,145,144,163, 7, 33]
    #right eye landmarks
    reye = [362, 398, 384,385,386,387,388,466,263,249,390,373,374,380,381,382,463,414,286,258,259,257,260,467,359,255,339,254,253,252,256,341]

    if eyes_on:
        # Drawing eyes on blue colour
        for landmark in leye:
            cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)

        for landmark in reye:
            cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)


    # we get the min and max position of the eyes (left and right) on any frame so that we can have a
    # windows of the eyes, even if we move
    #130 left eye landmark
    x_min, y_min = faces[0][130]
    cv2.circle(img, (x_min, y_min), 2, (255, 50, 0), cv2.FILLED)
    # 359 right eye landmark
    x_max, y_max = faces[0][359]
    cv2.circle(img, (x_max, y_max), 2, (255, 50, 0), cv2.FILLED)

    #We create a new image where we have just the eyes so that we can pass it to the CNN model
    image_new = image_new[y_min - 20:y_max + 20, x_min - 10:x_max + 10]

    #(120,40) is the size for the training we used on the CNN created previosuly
    # **It would be better for a CNN to use squared images
    image_new = cv2.resize(image_new, (120, 40))
    cv2.imshow('just eyes', image_new)
    if eyes_on:
     eye_direction = readingEye(image_new)


    #  Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    print(fps)

    # show the image with the face detections + facial landmarks
    cv2.imshow('eyes', img)

    k = cv2.waitKey(1) & 0xFF

    # click the 'e' key on the keyboard if you want to see or hide the eyes track points
    # and be able or not to use the eyes movement
    if k == ord("e"):
        eyes_on = not eyes_on
        face_on = False

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
