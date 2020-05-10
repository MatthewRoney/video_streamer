import cv2
import numpy as np
import datetime

# Open Video Capture on attached Camera
capture = cv2.VideoCapture(0)

# Collect stream information
framerate = capture.get(cv2.CAP_PROP_FPS)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Assign font for writing on frame
font = cv2.FONT_HERSHEY_SIMPLEX

# Open Video Writer for RTP Stream
output = cv2.VideoWriter('appsrc ! videoconvert !\
                        x264enc tune=zerolatency ! rtph264pay !\
                        udpsink host=127.0.0.1 port=5000',
                        cv2.CAP_GSTREAMER, 0, framerate, (width,height), True)

# When capture and out are open
while capture.isOpened() and output.isOpened():

    #Capture Camera frame
    ret, frame = capture.read()
    if ret:
        # Write current time to frame
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        cv2.putText(frame, f"Time: {time}", (10, 40), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

        # Convert frame to HSV
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define a range for colour and mask image
        lower_range = np.array([100,200,0])
        upper_range = np.array([110,255,255])
        mask = cv2.inRange(hsv_image, lower_range, upper_range)

        # Find contours of image and draw a bounding box
        contours,_ = cv2.findContours(mask, 1, 2)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        # Uncomment to show captured frame
        # cv2.imshow("Capture",frame)

        # Write frame to output stream
        output.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release capture and output when job is finished
capture.release()
output.release()
