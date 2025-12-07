---
sidebar_position: 3
title: Rendering with Unity
description: High-fidelity visual simulation for Human-Robot Interaction.
---

# 2.3 Unity for Robotics

While Gazebo is great for physics, **Unity** is a game engine engine designed for visual fidelity. In Physical AI, we use Unity when the robot needs to "see" and understand the world visually, or interact with humans naturally.

## 2.3.1 Unity Robotics Hub

Unity provides the **Unity Robotics Hub**, which includes the `ROS-TCP-Connector`. This allows Unity to talk to ROS 2.

- **Unity -> ROS:** Sends simulated camera images, LiDAR scans.
- **ROS -> Unity:** Sends joint positions to move the robot avatar.

## 2.3.2 Human-Robot Interaction (HRI)

Simulating HRI requires realistic human avatars. Using Unity, we can:

1.  Place animated human characters in the scene.
2.  Train the robot to navigate around people without collision (Social Navigation).
3.  Test gesture recognition systems.

## 2.3.3 Setting up the Connector

In your Unity Project:

1.  Go to `Window > Robotics > ROS Settings`.
2.  Set `ROS IP Address` to your ROS 2 machine (or `127.0.0.1` if local).
3.  Set `ROS Port` (default `10000`).

In ROS 2:

```bash
ros2 launch ros_tcp_endpoint endpoint.launch.py
```
