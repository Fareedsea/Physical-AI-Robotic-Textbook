---
sidebar_position: 4
title: Simulating Sensors
description: Modeling LiDAR, Cameras, and IMUs.
---

# 2.4 Simulating Sensors

A digital twin is useless if the robot is blind. We must simulate the data streams that the real robot would receive.

## 2.4.1 LiDAR (Light Detection and Ranging)

LiDAR uses lasers to create a 2D or 3D map of the environment.

- **Use case:** Obstacle avoidance, SLAM (Mapping).
- **In Simulation:** Ray-casting from the sensor origin to objects in the scene to calculate distance.

## 2.4.2 Depth Cameras (RGB-D)

Cameras like the **Intel RealSense** or **Stereolabs ZED** provide both color (RGB) and Depth (D).

- **Use case:** Object recognition, 3D reconstruction.
- **In Simulation:** The rendering engine generates the RGB image, and the Depth buffer contains the distance to each pixel.

## 2.4.3 IMU (Inertial Measurement Unit)

The IMU (Accelerometer + Gyroscope) tells the robot its orientation and acceleration.

- **Use case:** Balancing (for humanoids), Odometry.
- **In Simulation:** The physics engine reads the exact velocity of the model and adds Gaussian noise to simulate real-world sensor imperfection.

> **Note:** Clean simulation data is often "too perfect." Always add noise to sensor plugins to make your AI robust.
