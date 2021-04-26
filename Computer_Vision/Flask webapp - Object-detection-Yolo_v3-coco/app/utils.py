import matplotlib.pyplot as plt

import cv2
from app.yolo3 import yolo_v3_object_detection
import datetime

def objectClassifier(pathImage, filename):
    img = yolo_v3_object_detection(pathImage)

    cv2.imwrite('./static/predict/{}'.format(filename), img)
    plt.imshow(img)


def generate(vs):
    # grab global references to the output frame and lock variables
    #global outputFrame
    outputFrame = vs.read()
    # loop over frames from the output stream
    while True:
        # check if the output frame is available, otherwise skip
        # the iteration of the loop
        if outputFrame is None:
            continue
        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        # ensure the frame was successfully encoded
        if not flag:
            continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

        frame = vs.read()

        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        img = yolo_v3_object_detection(frame)
        outputFrame = img

