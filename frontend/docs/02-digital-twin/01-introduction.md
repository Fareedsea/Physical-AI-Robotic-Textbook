---
sidebar_position: 1
title: Introduction to Digital Twins
description: Why we simulate robots before building them.
---

# Module 2: The Digital Twin

## 2.1 What is a Digital Twin?

A **Digital Twin** is a virtual replica of a physical robot and its environment. In Physical AI, we rarely train robots directly in the real world because it is:

1.  **Expensive:** Robots break easily if they crash.
2.  **Slow:** Real-time collection of training data takes weeks.
3.  **Dangerous:** Large humanoids can injure operators.

Simulations allow us to train policies safely and thousands of times faster than real-time.

## 2.2 The Simulation Stack

To create a valid digital twin, we need two key components:

1.  **Physics Engine:** Calculates gravity, friction, collisions, and joint dynamics (e.g., Gazebo, MuJoCo, PhysX).
2.  **Rendering Engine:** Generates photo-realistic images for the robot's cameras (e.g., Unity, Unreal Engine, Isaac Sim).

## 2.3 Sim-to-Real Gap

Use simulations effectively requires closing the "Sim-to-Real" gap—ensuring that a policy learned in the matrix works in the real world.

> **Key Concept:** Domain Randomization (varying colors, friction, lighting in sim) helps the AI generalize to the real world.
