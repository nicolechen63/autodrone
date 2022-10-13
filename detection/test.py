import cv2
import numpy as np
import time

import depth.depth as depth
import model.model as model


# camera input values
CAMERA_HEIGHT = 720
CAMERA_WIDTH = 1920 # left right together
# calibration
cal = depth.Depth()
# open camera
cap = cv2.VideoCapture(1)
# modify camera parameter
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
# warm up
_, frame = cap.read()
h, width,_ = frame.shape
w = int(width/2)

# set mouse click display distance
def onClick(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        print('depth = ' + str(depthmap[y][x]) + ' cm')

# stereo matching
cal.createStereoMatch()

# detection
detect = model.FlowerDetection('trained/YOLOv5n/weights/best.pt')

while(True):
    start_time = time.perf_counter()

    _, frame = cap.read()
    imgl = frame[0:h, 0:w]
    imgr = frame[0:h, w:width]

    # calibrate left and right
    imgl = cal.calibrate(imgl, 'L')
    imgr = cal.calibrate(imgr, 'R')

    depthmap = cal.depthMap(imgl, imgr) # get depth map from stereo matching

    # cv2.imshow('left', imgl)
    # cv2.imshow('right', imgr)
    cv2.imshow('depth', depthmap)

    # use left image for detecion
    results = detect.score_frame(imgl)
    img = detect.plot_boxes(results, imgl)

    end_time = time.perf_counter()
    fps = 1 / np.round(end_time - start_time, 3)
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

    cv2.imshow('img', img)
    cv2.setMouseCallback('img', onClick) # click on image to get the depth
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()