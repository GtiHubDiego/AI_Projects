import matplotlib.pyplot as plt

import cv2
from app.yolo3 import yolo_v3_object_detection

def objectClassifier(pathImage, filename):
    img = yolo_v3_object_detection(pathImage)

    cv2.imwrite('./static/predict/{}'.format(filename), img)
    plt.imshow(img)




