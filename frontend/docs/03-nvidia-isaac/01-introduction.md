---
sidebar_position: 1
title: Introduction to NVIDIA Isaac
description: The end-to-end platform for robotics simulation and AI.
---

# Module 3: The AI-Robot Brain

## 3.1 What is NVIDIA Isaac?

**NVIDIA Isaac** is a comprehensive platform built to accelerate the development, simulation, and deployment of AI-enabled robots. It consists of two main pillars that we will cover in this module:

1.  **Isaac Sim:** A photo-realistic simulation application built on Omniverse.
2.  **Isaac ROS:** Hardware-accelerated ROS 2 packages for perception and navigation.

## 3.2 Why Isaac Sim?

Unlike Gazebo, which focuses on physics, Isaac Sim focuses on **Data Generation** for AI.

- **Photorealism:** Ray-tracing allow robots to "see" the world exactly as they would in reality.
- **Synthetic Data:** Generate millions of labeled images to train neural networks without human effort.

## 3.3 The Isaac Workflow

1.  **Import Robot:** Load your URDF into Isaac Sim.
2.  **Build Environment:** Use the USD (Universal Scene Description) format to create a warehouse, home, or factory.
3.  **Train:** Use Reinforcement Learning (Isaac Gym) to teach the robot to walk or grasp.
4.  **Deploy:** Export the trained policy to the physical robot's Jetson Orin computer.
