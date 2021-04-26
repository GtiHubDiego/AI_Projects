from flask import render_template, request,Response
import os
from PIL import Image
from app.utils import objectClassifier, generate
from imutils.video import VideoStream
import time

UPLOAD_FLODER = 'static/uploads'
def base():
    return render_template('base.html')


def index():
    return render_template('index.html')


def yoloapp():
    return render_template('yoloapp.html')

def realtimeobjectdetection():
    return render_template('realtimeobjectdetection.html')

def getwidth(path):
    img = Image.open(path)
    size = img.size # width and height
    aspect = size[0]/size[1] # width / height
    w = 300 * aspect
    return int(w)

def video_feed():
    # initialize the video stream and allow the camera sensor to
    # warmup
    # vs = VideoStream(usePiCamera=1).start()
    vs = VideoStream(src=0).start()
    time.sleep(0.1)
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(vs),mimetype = "multipart/x-mixed-replace; boundary=frame")


def objectdetection():

    if request.method == "POST":
        f = request.files['image']
        filename=  f.filename
        path = os.path.join(UPLOAD_FLODER,filename)
        f.save(path)
        w = getwidth(path)
        objectClassifier(path,filename)

        return render_template('objectdectection.html', fileupload=True, img_name=filename, w=w)


    return render_template('objectdectection.html', fileupload=False, img_name="freeai.png")