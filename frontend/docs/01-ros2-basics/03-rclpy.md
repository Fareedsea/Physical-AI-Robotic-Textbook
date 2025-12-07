---
sidebar_position: 3
title: Coding with rclpy
description: writing ROS 2 nodes in Python.
---

# 1.3 Bridging Python Agents (rclpy)

**rclpy** (ROS Client Library for Python) provides the standard interface for interacting with ROS 2 from Python code. It allows us to write nodes that can publish messages, subscribe to topics, and call services.

## 1.3.1 Key Components

- `rclpy.init()`: Initializes the ROS 2 communications.
- `Node`: The class we inherit from to create our own nodes.
- `create_publisher()`: Method to create a data broadcaster.
- `create_subscription()`: Method to create a data listener.
- `rclpy.spin()`: Keeps the node running and listening for callbacks.

## 1.3.2 Example: Minimal Publisher

Here is a simple python script that acts as a "Talker", publishing a messge every 0.5 seconds.

```python title="simple_publisher.py"
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    
    # Destroy the node explicitly
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.3.3 Integration with AI Agents

In Physical AI, we use `rclpy` to bridge the gap between Large Language Models (LLMs) and the robot.

1.  **User Prompt:** "Pick up the red ball."
2.  **LLM Processing:** Decides on an action sequence `pick_object(target='red_ball')`.
3.  **rclpy Execution:** Python script translates `pick_object` into ROS 2 Twist messages or MoveIt commands to control the robot arm.
