#!/bin/bash
#

# Start the webcam streaming server

mjpg_streamer -i "input_uvc.so -d /dev/videoA -n -r 1280x720 -f 15" -o "output_http.so -p 8090 -n -w /usr/www"

