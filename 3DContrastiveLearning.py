#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os
from matplotlib import cm

class ContrastiveLearning3DVisualizer:
    """
    A class to create 3D visualizations of contrastive learning space alignment.
    This adds a third dimension to make the visualization more engaging and to
    better show the transformation between spaces.
    """
    
    def __init__(self, output_dir="contrastive_3d_frames", total_steps=100):
        """Initialize the visualizer with configuration parameters."""
        self.output_dir = output_dir
        self.total_steps = total_steps
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Categories and their colors
        self.categories = {
            'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'horse'],
            'vehicles': ['car', 'boat', 'plane', 'train', 'bus', 'truck'],
            'food': ['apple', 'banana', 'orange', 'pizza', 'burger', 'pasta'],
            'nature': ['mountain', 'ocean', 'forest', 'river', 'desert', 'cloud']
        }
        
        self.category_colors = {
            'animals': cm.Blues(0.7),
            'vehicles': cm.Greens(0.7),
            'food': cm.Oranges(0.7),
            'nature': cm.Purples(0.7)
        }
        
        # Generate initial spaces with 3D coordinates
        self.image_points_orig, self.text_points_orig = self._generate_initial_spaces()
        
        # Set the figure style
        plt.style.use('seaborn-v0_8-whitegrid')
    
    def _generate_initial_spaces(self):
        """Generate initial 3D coordinates for image and text spaces."""
        np.random.seed(42)  # For reproducibility
        
        # Create image space - clustered by category in 3D
        image_points = {}
        
        # Category centers in 3D space
        category_centers = {
            'animals': np.array([0.7, 0.7, 0.7]),
            'vehicles': np.array([0.3, 0.3, 0.3]),
            'food': np.array([0.3, 0.7, 0.3]),
            'nature': np.array([0.7, 0.3, 0.7])
        }
        
        for category, items in self.categories.items():
            for item in items:
                # Add random jitter around category centers
                image_points[item] = category_centers[category] + np.random.normal(0, 0.07, 3)
        
        # Create text space with a different orientation
        text_points = {}
        
        # Create a 3D rotation matrix (around y-axis)
        theta = np.pi / 2  # 90-degree rotation
        rotation_matrix = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
        
        for item, point in image_points.items():
            # Apply rotation and add an offset
            offset = np.array([0.1, 0.1, 0.1])
            text_points[item] = rotation_matrix @ point + offset
        
        return image_points, text_points
    
    def create_visualization(self):
        """Create the entire visualization sequence."""
        print(f"Creating 3D visualization with {self.total_steps} steps...")
        
        # Create copies to transform
        image_points = {k: v.copy() for k, v in self.image_points_orig.items()}
        text_points = {k: v.copy() for k, v in self.text_points_orig.items()}
        
        # Plot initial state
        self._plot_spaces(image_points, text_points, 0)
        
        # For each step, transform the spaces
        for step in range(1, self.total_steps + 1):
            # Calculate interpolation parameter with easing
            t = self._ease_in_out_cubic(step / self.total_steps)
            
            # For each item, interpolate between original and target
            for item in image_points:
                if item in text_points:
                    # Calculate target position (halfway between points with slight elevation)
                    midpoint =
