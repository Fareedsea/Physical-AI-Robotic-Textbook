---
sidebar_position: 1
title: Introduction to ROS 2
description: Understanding the Robot Operating System (ROS 2) middleware.
---

# Module 1: The Robotic Nervous System (ROS 2)

## 1.1 What is ROS 2?

**ROS 2 (Robot Operating System 2)** is not a traditional operating system like Windows or Linux. It is a set of software libraries and tools that help you build robot applications. Think of it as the **nervous system** of a robot—it allows different parts of the robot (sensors, motors, AI) to communicate with each other in real-time.

> **Key Concept:** ROS 2 provides the "plumbing" for your robot, handling message passing, hardware abstraction, and device control.

## 1.2 Why use ROS 2?

- **Real-time Capability:** Designed for mission-critical tasks requiring deterministic timing.
- **Security:** Built on DDS (Data Distribution Service) for secure communication.
- **Industry Standard:** Used by major robotics companies (NASA, Amazon Robotics, Tesla).

## 1.3 Architecture Overview

ROS 2 is built on a distributed arcitecture:

1.  **Nodes:** Processes that perform computation.
2.  **Topics:** Channels for nodes to exchange data (Publisher/Subscriber).
3.  **Services:** Synchronous communication (Client/Server).
4.  **Actions:** Asynchronous communication for long-running tasks.

![ROS 2 Architecture](/img/ros2-architecture-diagram.png)

## 1.4 Setting Up Yor Environment

To begin this module, ensure you have the following installed:

```bash
sudo apt update && sudo apt install ros-humble-desktop
source /opt/ros/humble/setup.bash
```

In the next section, we will build our first ROS 2 Node.
