---
sidebar_position: 1
title: Vision-Language-Action Models
description: The convergence of Generative AI and Robotics.
---

# Module 4: Vision-Language-Action (VLA)

## 4.1 The Next Frontier

Traditional robotics pipelines (Perception -> Planning -> Control) are brittle. If the perception module fails, the planner fails. **VLA Models** (like Google's RT-2 or Tesla's FSD end-to-end network) replace this disjointed pipeline with a single, massive neural network.

## 4.2 How VLA Works

A VLA model takes two inputs:
1.  **Vision:** Camera images from the robot's eyes.
2.  **Language:** A command like "Pick up the apple."

And outputs:
1.  **Action:** A sequence of joint velocities (or end-effector delta pose) to execute the command.

> **Analogy:** Just like ChatGPT predicts the next *word* in a sentence, a VLA model predicts the next *action* a robot should take.

## 4.3 Grounding LLMs

LLMs live in a world of text. To make them useful for robotics, we must **ground** them in physical reality.

- **VLM (Vision-Language Model):** Can look at an image and say "That is a red apple on the table."
- **VLA (Vision-Language-Action):** Can look at the image and say "I need to move my arm 10cm forward to grasp the apple."
