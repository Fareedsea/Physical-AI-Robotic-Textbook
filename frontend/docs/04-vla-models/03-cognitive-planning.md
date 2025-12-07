---
sidebar_position: 3
title: Cognitive Planning
description: Using LLMs to break down complex tasks.
---

# 4.3 Cognitive Planning

Robots are good at low-level actions ("Move arm to X,Y,Z"). They are bad at high-level reasoning. **Cognitive Planning** uses an LLM (like GPT-4o) as the "Prefrontal Cortex" of the robot.

## 4.3.1 Chain of Thought (CoT)

If you tell a robot "Clean the room," it doesn't know what that means. An LLM can break it down:

**Prompt:**
> You are a robot assistant. The user said "Clean the room." detailed the steps.

**LLM Output:**
1.  Scan the environment for misplaced objects.
2.  Identify "Socks" on the floor.
3.  Identify "Trash" on the table.
4.  For each object:
    - Pick it up.
    - Navigate to the appropriate bin (Laundry vs. Trash).
    - Drop it.

## 4.3.2 Code Generation Agents

Instead of outputting text steps, advanced agents write Python code that the robot executes directly.

```python
# The LLM generates this code based on available skills
def clean_room(robot):
    objects = robot.perception.scan()
    for obj in objects:
        if obj.category == 'trash':
            robot.arm.pick(obj)
            robot.nav.go_to('trash_bin')
            robot.arm.drop()
```

This transforms the LLM from a chatbot into a **System Orchestrator**.
