#!/bin/bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
source /opt/ros/foxy/setup.bash
ros2 launch octomap_server2 octomap_server.py
