### Eye tracking
In this project we will be able to move the mouse (left, right) using the movement of our eyes.

1) I have created a CNN model with my own dataset (pictures of my eyes looking to different direcctions) and I have trained it.
2) I have used cvzone-mediapipe libraries for face detection.
3) I will be taken frames from the camera on Real Time, first of all we will be detecting the face, and later on detecting just the eyes (ROI) so that we will be able to use that part of the frame to predict (on my CNN) the movement of the eyes.
4) I have used autopy library for mouse movements and Keys class for clicking a keyboard key (virtually), 
which we will open a world of possibilities such a play games just using the movement of your eyes.


Moving the mouse and pressing keys ('l' (left) and 'r' (right) ) :

![Eye_tracking_min](https://user-images.githubusercontent.com/38459325/117963896-3d611f80-b321-11eb-8152-5efcb3bd580a.gif)

Playing Bricks just using the eyes movements :

![bricks-eyes](https://user-images.githubusercontent.com/38459325/118247980-15e69000-b4a4-11eb-8994-9e22b26ba6ad.gif)

