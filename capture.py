import cv2
import numpy as np
import datetime

# Open Video Capture on attached Camera
cap = cv2.VideoCapture(0)

# Collect stream information
framerate = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Assign font for writing on frame
font = cv2.FONT_HERSHEY_SIMPLEX

# Open Video Writer for RTP Stream
out = cv2.VideoWriter('appsrc ! videoconvert !\
                        x264enc tune=zerolatency ! rtph264pay !\
                        udpsink host=127.0.0.1 port=5000',
                        cv2.CAP_GSTREAMER, 0, framerate, (width,height), True)

# When capture and out are open
while cap.isOpened() and out.isOpened():

    #Capture Camera frame
    ret, frame = cap.read()
    if ret:
        # Write current time to frame
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        cv2.putText(frame, f"Time: {time}", (10, 40), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

        # Show frame
        cv2.imshow("Capturing",frame)

        #Write frame to output stream
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
