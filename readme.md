# Contrastive Learning Visualization

This repository contains tools for visualizing contrastive learning space alignment - showing how different representation spaces (like text and images) can be aligned through contrastive learning.

## Overview

Contrastive learning is a powerful technique in which models learn to align representations from different modalities (like images and text) in a shared embedding space. This visualization demonstrates the process of alignment, showing how initially disparate spaces gradually converge.

## Visualization Methods

This project includes several different visualization approaches:

1. **Static Visualization**: Generates frame-by-frame images showing the alignment process
2. **3D Visualization**: Shows the alignment in three dimensions for a more comprehensive view
3. **Manim Animation**: Creates high-quality animations using the Manim library
4. **Interactive HTML Viewer**: Provides an interactive web-based viewer for exploring the visualization

## Requirements

- Python 3.7+
- Required packages: numpy, matplotlib
- Optional packages: 
  - imageio (for creating GIFs)
  - manim (for creating Manim animations)

You can install the required packages with:

```bash
pip install numpy matplotlib imageio
```

For Manim animations (optional):

```bash
pip install manim
```

## Running the Visualizations

### Basic Static Visualization

For the simplest and most reliable visualization:

```bash
python simplified_runner.py --steps 100 --output contrastive_viz
```

Options:
- `--steps`: Number of frames to generate (default: 100)
- `--output`: Output directory name (default: contrastive_viz)

### Enhanced Visualization

For more advanced visualization options:

```bash
python enhanced_runner.py --mode all --steps 100 --output contrastive_viz
```

Options:
- `--mode`: Visualization mode (static, 3d, manim, html, all)
- `--steps`: Number of frames to generate (default: 100)
- `--output`: Output directory name (default: contrastive_viz)

### Viewing the Results

#### Using the HTML Viewer

1. Save the `simple_viewer.html` file to the parent directory of your output folder
2. Open it in a web browser:

```bash
# On macOS
open simple_viewer.html

# On Linux
xdg-open simple_viewer.html

# On Windows
start simple_viewer.html
```

#### Viewing the GIF Animation

```bash
# On macOS
open contrastive_viz/contrastive_learning_animation.gif

# On Linux
xdg-open contrastive_viz/contrastive_learning_animation.gif

# On Windows
start contrastive_viz/contrastive_learning_animation.gif
```

## File Structure

- `simplified_runner.py`: Simple runner script with progress feedback
- `simplified_static_visualization.py`: Simplified visualization with progress indicators
- `enhanced_runner.py`: Advanced runner for all visualization types
- `improved_static_visualization.py`: Enhanced static visualization with better styling
- `improved_3d_visualizer.py`: 3D visualization using matplotlib's 3D capabilities
- `improved_manim_animation.py`: Enhanced Manim animation
- `data_generator.py`: Generates the initial data for visualization
- `simple_viewer.html`: Web-based interactive viewer

## Troubleshooting

If you encounter issues with the enhanced visualization hanging:

1. Try the simplified version first: `python simplified_runner.py --steps 50`
2. Reduce the number of steps: `--steps 50` instead of `--steps 100`
3. Make sure you have enough memory available (generating many high-quality frames can be memory-intensive)

## Understanding the Visualization

- **Image Space**: Represents embeddings from the image modality (circles)
- **Text Space**: Represents embeddings from the text modality (squares)
- **Colors**: Different colors represent different semantic categories
- **Convergence**: Watch how points of the same semantic meaning gradually align

## Author

Mikey Bee, 2025

## License

MIT License
