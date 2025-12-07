---
sidebar_position: 4
title: Capstone: Autonomous Humanoid
description: Building the final project.
---

# 4.4 Capstone Project: The Autonomous Humanoid

Congratulations Cadet. You have learned about ROS 2, Digital Twins, NVIDIA Isaac, and VLA Models. It is time to build the ultimate project.

## 4.4.1 The Mission

You will simulate a Unitree G1 Humanoid in NVIDIA Isaac Sim that can:
1.  **Patrol** a warehouse environment (Nav2).
2.  **Detect** intruders or anomalies (Isaac ROS / YOLO).
3.  **Respond** to voice commands (Whisper).
4.  **Explain** its actions (LLM Integration).

## 4.4.2 Architecture

```mermaid
graph TD
    User((User)) -- Voice Command --> Whisper[Whisper ASR]
    Whisper -- Text --> Brain[LLM Planner]
    Brain -- High-Level Plan --> Nav[Nav2 Stack]
    Brain -- Manipulation Goal --> Arm[MoveIt 2]
    
    subgraph "Robot Hardware / Sim"
        Nav -- cmd_vel --> Base[Mobile Base]
        Arm -- Joint Trajectory --> Hand[Gripper]
        Camera -- Images --> Vision[YOLOv8]
    end
    
    Vision -- Detections --> Brain
```

## 4.4.3 Submission

To complete this course, submit a video recording of your simulation performing a "Search and Retrieve" mission from a voice command.
