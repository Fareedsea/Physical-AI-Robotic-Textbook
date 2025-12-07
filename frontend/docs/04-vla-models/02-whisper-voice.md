---
sidebar_position: 2
title: Voice Control with Whisper
description: Commanding robots with natural speech.
---

# 4.2 Voice-to-Action

To interact naturally with humanoids, we shouldn't need a keyboard. We should just speak. **OpenAI Whisper** is the state-of-the-art model for Automatic Speech Recognition (ASR).

## 4.2.1 The Pipeline

1.  **Human Speaks:** "Robot, bring me a soda."
2.  **Whisper Transcribes:** Converts audio to text `"Robot, bring me a soda."`
3.  **LLM Planner:** Parses the intent. `Goal: Fetch object. Target: Soda.`
4.  **Robot Executes:** Nav2 plans a path to the kitchen.

## 4.2.2 Why Whisper?

- **Robustness:** Works in noisy environments (factories, warehouses).
- **Multilingual:** Supports 99 languages (including Urdu!).
- **Efficiency:** The `distil-whisper` variant can run in real-time on edge devices like the Jetson Orin.

## 4.2.3 Latency Challenges

The delay between speaking and the robot moving is critical.
- **Cloud API:** ~1-2 seconds latency (dependent on internet).
- **Local Inference:** <500ms latency (using `whisper.cpp` or TensorRT).

For safety-critical commands ("STOP!"), we always run keyword spotting locally on the robot.
