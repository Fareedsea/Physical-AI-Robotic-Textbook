---
sidebar_position: 2
title: Isaac Sim & Synthetic Data
description: Generating training data in the Metaverse.
---

# 3.2 Isaac Sim & Synthetic Data

Training computer vision models requires massive datasets (ImageNet, COCO). Collecting this data manually is slow and error-prone. **Synthetic Data Generation (SDG)** allows us to programmatically create infinite, perfectly labeled datasets.

## 3.2.1 Domain Randomization (DR)

To ensure the AI doesn't memorize the simulation, we use DR.

- **Visual DR:** Randomize lights, textures, colors, and camera positions.
- **Physical DR:** Randomize mass, friction, and gravity.

## 3.2.2 Replicator API

Isaac Sim provides the `Replicator` API to automate data collection.

```python
import omni.replicator.core as rep

with rep.new_layer():
    # Create a camera
    camera = rep.create.camera(position=(0, 5, 5), look_at=(0, 0, 0))

    # Randomize the position of the cube every frame
    cube = rep.create.cube(semantics=[('class', 'box')])
    with rep.trigger.on_frame():
        with cube:
            rep.randomizer.position(min=(-2, 0, -2), max=(2, 0, 2))
            rep.randomizer.color(colors=rep.distribution.uniform((0,0,0), (1,1,1)))
```

## 3.2.3 Exporting Data

The data generated includes:
- RGB Images
- Depth Maps
- Segmentation Masks
- 2D/3D Bounding Boxes

This data can be directly fed into YOLO or MaskRCNN for training.
