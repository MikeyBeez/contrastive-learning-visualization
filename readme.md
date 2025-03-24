# Contrastive Learning Visualization

This repository contains visualizations of contrastive learning space alignment - showing how different representation spaces (like text and images) can be aligned through contrastive learning.

## Visualization Methods

This project includes two different visualization approaches:
1. A Python-based static visualization that generates frames and an interactive HTML viewer
2. A Manim-based animated visualization for high-quality video output

## Setup and Usage

### Requirements
- Python 3.7+
- Required packages: numpy, matplotlib
- For Manim visualization: Manim and its dependencies (Cairo, FFmpeg)

### Running the Static Visualization
```bash
# Generate 100 frames with the static visualizer
python main.py --steps 100

# Open the interactive viewer
open contrastive_frames/interactive_viewer.html
