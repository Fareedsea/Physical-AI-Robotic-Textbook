---
sidebar_position: 4
title: Understanding URDF
description: The Unified Robot Description Format for Humanoids.
---

# 1.4 Unified Robot Description Format (URDF)

**URDF** is an XML format used in ROS to describe all elements of a robot. It defines the physical structure, kinematics, and dynamics of the robot.

## 1.4.1 Structure of a URDF

A robot is defined as a tree of **Links** connected by **Joints**.

- **Link:** A rigid body (e.g., forearm, wheel, chassis). It has visual (mesh/shape) and collision properties.
- **Joint:** The connection between two links (e.g., hinge, slider, fixed). It defines the range of motion.

## 1.4.2 Example: A Simple Humanoid Arm

```xml
<robot name="simple_arm">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.2"/>
      </geometry>
    </visual>
  </link>

  <!-- Upper Arm Link -->
  <link name="upper_arm">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.5"/>
      </geometry>
    </visual>
  </link>

  <!-- Shoulder Joint -->
  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm"/>
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
  </joint>
</robot>
```

## 1.4.3 Importance in Physical AI

For a humanoid robot, the URDF is critical because:

1.  **Simulation:** Gazebo and Isaac Sim use it to render the robot physics.
2.  **Kinematics:** MoveIt uses the joint limits to calculate valid paths for the arm to move without self-collision.
3.  **Digital Twin:** It ensures the virtual robot matches the physical robot exactly.
