---
sidebar_position: 2
title: Physics with Gazebo
description: Simulating gravity, collisions, and dynamics.
---

# 2.2 Gazebo Simulator

**Gazebo** is the de facto standard simulator for ROS 2. It excels at simulating rigid body dynamics, making it perfect for testing robot navigation and manipulation physics.

## 2.2.1 Core Components

- **World Files (.sdf):** Define the environment (ground plane, walls, sun, gravity).
- **Models:** Robot assets and static objects.
- **Plugins:** C++ code that connects ROS 2 topics to Gazebo properties (e.g., `diff_drive_controller` so `cmd_vel` moves the virtual robot).

## 2.2.2 Simulating Physics

Gazebo handles the math of the physical world:

1.  **Gravity:** Things fall down.
2.  **Collision:** Objects don't pass through each other.
3.  **Friction:** Wheels need traction to move.
4.  **Inertia:** Heavy arms are harder to stop moving.

## 2.2.3 Launching a Simulation

```bash
# Install Gazebo
sudo apt install ros-humble-gazebo-ros-pkgs

# Launch a demo world
ros2 launch gazebo_ros gazebo.launch.py
```

## 2.2.4 Spawning a Robot

To spawn a URDF robot into Gazebo, we use the `spawn_entity` node:

```bash
ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity my_robot
```
