# RTP Stream Demo
A RTP streaming Demo that overlays the time on a camera feed for display in VLC, this is done using GStreamer and OpenCV.

## Quickstart
Run setup in the root directory:
````
./setup.sh
````
This will install necessary packages.

Start the capture program:
````
python3 capture.py
````

In another terminal session, connect to the stream using VLC:
````
vlc view.sdp
````