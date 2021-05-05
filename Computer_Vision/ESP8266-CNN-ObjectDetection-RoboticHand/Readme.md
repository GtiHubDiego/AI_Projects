
In this cool project we are using Deep Learning to move a robotic hand using an ES8266 Wifi microchip.

Moving our hand (Fist, palm) displayed on a webcam, we will be able to move a robotic hand which is not connected directly to our computer.

We will be implementing a window where we can display a webcam or any IP cam. This window will have a ROI where we will put our hand with different gestures. For simplicity we will start with a Palm and a Fist.
When an object is detected on our ROI area, our python program will predict using our CNN model what kind of gesture is. 
When our prediction is good enough, our Python program will create a POST request which will be sent  to a Rest service previously created  on the ESP8266 web server.
Depending on the gesture, the ESP will send the order to a Servo so that it can move. The servo is connected to a Robotic hand, so if our gesture is a fist, the robotic hand will be closing and when the gesture is a palm, the robotic hand will be opening.

There are several steps to build this project :

1) DataSet:  We create our own dataset. 
	Using the same window we will use later for moving the robotic hand we will be able to record our hand gestures on files.
In RobotHandArduino.py we will use the  start_recording  flag, but we have to modify  part of the code, setting where we want to record the images and the name of them.  (name_file = "Recordings/fist_" + str(image_num) + '.png')
  	we can start the recording clicking on ‘s’ key

2) After that we will create a structure of directories of images (Test->Fist, Test->Palm, Train….) that we will use later on for training our model.

3) We create a CNN model (handModel.py) , we train the model using the previous dataset and we save the trained model.

4) RobotHandArduino.py will contain the necessary code for loading the CNN model, creating the webcam window, creating a ROI area, detect a new contorn over a background, predict if that contorn if one of our hand gesture and,  in an affirmative case, send a Post Request to our ESP8266 web server.


Arduino side: 

5) We will create a simple web server on our ESP8266  (ESP_web_server.ino) which will receive a post request to a Rest services previously created, 
that  will send a signal to the servomotor to move it, setting how many degrees will be moved, simulating the movement of a hand.



![robotHand](https://user-images.githubusercontent.com/38459325/117171858-89fda580-adcb-11eb-8645-2c7ab5dc4eee.gif)


