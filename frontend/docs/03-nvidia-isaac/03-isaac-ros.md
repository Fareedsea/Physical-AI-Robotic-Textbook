---
sidebar_position: 3
title: Isaac ROS (GEMs)
description: Hardware-accelerated perception for ROS 2.
---

# 3.3 Isaac ROS (GEMs)

**Isaac ROS** is a collection of GPU-accelerated ROS 2 packages. These packages (GEMs) are highly optimized for NVIDIA Jetson hardware, providing real-time performance for heavy AI workloads.

## 3.3.1 Visual SLAM (VSLAM)

`isaac_ros_visual_slam` provides high-performance localization using stereo cameras. Unlike LiDAR SLAM, VSLAM works in dynamic environments and is cheaper (cameras < LiDAR).

**Key Topics:**
- `/visual_slam/tracking/odometry`: The robot's estimated position.
- `/visual_slam/tracking/vo_pose_covariance`: Confidence of the estimation.

## 3.3.2 AprilTag Detection

AprilTags are fiducial markers (like QR codes) used for ground-truth reference. `isaac_ros_apriltag` can detect tags at 60 FPS on a Jetson Nano.

## 3.3.3 Object Detection (YOLOv8)

`isaac_ros_yolov8` performs real-time object detection.

- **Input:** `/image_raw` (RGB)
- **Output:** `/detections` (Bounding Boxes + Class IDs)

## 3.3.4 Installation

Isaac ROS works best in a Docker container.

```bash
# Clone the common folder
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git

# Launch the container
cd isaac_ros_common
./scripts/run_dev.sh
```
