import numpy as np
import cv2


# Giving name to the window with Track Bars
# And specifying that window is resizable
cv2.namedWindow('Track Bars', cv2.WINDOW_NORMAL)


# Preparing Track Bars
# Defining empty function
def do_nothing(x):
    pass

# Defining Track Bars for convenient process of choosing colours
# For minimum range
cv2.createTrackbar('min_red', 'Track Bars', 0, 255, do_nothing)
cv2.createTrackbar('min_blue', 'Track Bars', 0, 255, do_nothing)
cv2.createTrackbar('min_green', 'Track Bars', 0, 255, do_nothing)


# For maximum range
cv2.createTrackbar('max_red', 'Track Bars', 0, 255, do_nothing)
cv2.createTrackbar('max_blue', 'Track Bars', 0, 255, do_nothing)
cv2.createTrackbar('max_green', 'Track Bars', 0, 255, do_nothing)


#Setting Default values (Blue)

cv2.setTrackbarPos('min_red', 'Track Bars', 94)
cv2.setTrackbarPos('min_green', 'Track Bars', 80)
cv2.setTrackbarPos('min_blue', 'Track Bars', 2)


cv2.setTrackbarPos('max_red', 'Track Bars', 120)
cv2.setTrackbarPos('max_green', 'Track Bars',255)
cv2.setTrackbarPos('max_blue', 'Track Bars', 255)


# Capturing video through webcam
webcam = cv2.VideoCapture(0)

# Start a while loop
while (1):

    # Defining variables for saving values of the Track Bars
    # For minimum range
    min_blue = cv2.getTrackbarPos('min_blue', 'Track Bars')
    min_green = cv2.getTrackbarPos('min_green', 'Track Bars')
    min_red = cv2.getTrackbarPos('min_red', 'Track Bars')

    # For maximum range
    max_blue = cv2.getTrackbarPos('max_blue', 'Track Bars')
    max_green = cv2.getTrackbarPos('max_green', 'Track Bars')
    max_red = cv2.getTrackbarPos('max_red', 'Track Bars')

    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    # red_lower = np.array([136, 87, 111], np.uint8)
    #red_upper = np.array([180, 255, 255], np.uint8)

    colour_lower = np.array([min_red, min_green, min_blue], np.uint8)
    colour_upper = np.array([max_red, max_green, max_blue], np.uint8)
    colour_mask = cv2.inRange(hsvFrame, colour_lower, colour_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular colour
    kernal = np.ones((5, 5), "uint8")

    # For selected colour
    colour_mask = cv2.dilate(colour_mask, kernal)
    res_colour = cv2.bitwise_and(imageFrame, imageFrame,
                              mask=colour_mask)


    # Creating contour to track  color
    contours, hierarchy = cv2.findContours(colour_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(imageFrame, "Colour found", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (20, 55, 40, ),2)



    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
