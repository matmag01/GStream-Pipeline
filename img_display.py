import cv2
import yaml
import argparse
import os
import sys
import numpy as np
import socket
import time


def open_gst_cam(device_number):
    """Create a GStreamer pipeline to open the Blackmagic DeckLink camera."""
    pipeline_str = (
        f"decklinkvideosrc device-number={device_number} ! "
        "videoconvert ! "
        "videocrop left=310 right=310 top=28 bottom=28 ! "
        "video/x-raw,format=BGR ! deinterlace ! "
        "appsink name=appsink"
    )
    cap = cv2.VideoCapture(pipeline_str, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print(f"Error: Unable to open camera {device_number}")
        sys.exit(1)
    return cap

def main():

    # Open the two cameras
    cap_left = open_gst_cam(0)
    # cap_no_deinterlace = open_gst_cam_no_deinterlace(0)
    #cap_right = open_gst_cam(1)


    while True:
        # Capture frames
        retL, frameL = cap_left.read()
        # ret_no_deinterlace, frame_no_deinterlace = cap_no_deinterlace.read()
        h, w = frameL.shape[:2]
        print(f"Frame dimensions: {w}x{h}")
        if not retL: # or not ret_no_deinterlace:
            print("Error: Unable to read from video streams")
            break

        cv2.imshow("Left", frameL)

        if (cv2.waitKey(2) & 0xFF == ord('q')):
            break

    cap_left.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
