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
                    midpoint = (self.image_points_orig[item] + self.text_points_orig[item]) / 2
                    # Add slight elevation for more visual interest
                    midpoint[1] += 0.1
                    
                    # Move both points toward the target
                    image_points[item] = self.image_points_orig[item] * (1 - t) + midpoint * t
                    text_points[item] = self.text_points_orig[item] * (1 - t) + midpoint * t
            
            # Plot current state
            self._plot_spaces(image_points, text_points, step)
        
        print(f"3D visualization complete! {self.total_steps+1} frames created in '{self.output_dir}' folder.")
        
        # Create animated video
        self._create_animation()
    
    def _plot_spaces(self, image_points, text_points, step):
        """Create visualization of the 3D spaces at a given step."""
        # Create a figure with higher DPI for better quality
        fig = plt.figure(figsize=(14, 10), dpi=150)
        ax = fig.add_subplot(111, projection='3d')
        
        # Set background color and grid
        ax.set_facecolor('#f8f9fa')
        ax.grid(True, alpha=0.3)
        
        # Draw connecting lines first (so they appear behind points)
        for item in image_points:
            if item in text_points:
                img_point = image_points[item]
                txt_point = text_points[item]
                
                # Calculate line opacity based on distance (closer = more transparent)
                distance = np.linalg.norm(img_point - txt_point)
                max_dist = 1.0  # Maximum expected distance in normalized space
                alpha = min(1.0, distance / max_dist)
                
                # Draw connecting line
                ax.plot(
                    [img_point[0], txt_point[0]],
                    [img_point[1], txt_point[1]],
                    [img_point[2], txt_point[2]],
                    'gray', linestyle='--', alpha=alpha * 0.5, linewidth=1
                )
        
        # Plot points by category with improved styling
        for category, items in self.categories.items():
            category_color = self.category_colors[category]
            
            # Create category-specific collections for legend
            img_points_x, img_points_y, img_points_z = [], [], []
            txt_points_x, txt_points_y, txt_points_z = [], [], []
            
            for item in items:
                # Plot image points
                if item in image_points:
                    point = image_points[item]
                    img_points_x.append(point[0])
                    img_points_y.append(point[1])
                    img_points_z.append(point[2])
                    
                    # Draw each point
                    ax.scatter(
                        point[0], point[1], point[2],
                        s=150, alpha=0.8, color=category_color,
                        edgecolors='white', linewidth=1.5
                    )
                    
                    # Add text label
                    ax.text(
                        point[0], point[1], point[2] + 0.03,
                        item.upper(), fontsize=9, ha='center', va='bottom',
                        color='black', weight='bold',
                        bbox=dict(
                            boxstyle="round,pad=0.2",
                            fc=category_color, ec="none", alpha=0.7
                        )
                    )
                
                # Plot text points
                if item in text_points:
                    point = text_points[item]
                    txt_points_x.append(point[0])
                    txt_points_y.append(point[1])
                    txt_points_z.append(point[2])
                    
                    # Use square markers for text points
                    ax.scatter(
                        point[0], point[1], point[2],
                        s=150, alpha=0.8, color=category_color,
                        edgecolors='white', linewidth=1.5,
                        marker='s'
                    )
                    
                    # Add text label
                    ax.text(
                        point[0], point[1], point[2] + 0.03,
                        f"'{item.upper()}'", fontsize=9, ha='center', va='bottom',
                        color='black', weight='bold',
                        bbox=dict(
                            boxstyle="round,pad=0.2",
                            fc=category_color, ec="none", alpha=0.6
                        )
                    )
            
            # Add empty plots for legend entries
            ax.scatter([], [], [], s=100, color=category_color, label=category.capitalize())
        
        # Add legend
        ax.legend(loc='upper right', frameon=True, fontsize=12)
        
        # Set axis limits with slight padding
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)
        
        # Set labels
        ax.set_xlabel('Dimension 1', fontsize=12, labelpad=10)
        ax.set_ylabel('Dimension 2', fontsize=12, labelpad=10)
        ax.set_zlabel('Dimension 3', fontsize=12, labelpad=10)
        
        # Determine the optimal view angle based on step
        # Start with side view and rotate to top view as alignment progresses
        elevation = 30 - 20 * (step / self.total_steps)  # Gradually look more from above
        azimuth = 30 + 50 * (step / self.total_steps)    # Rotate around
        ax.view_init(elev=elevation, azim=azimuth)
        
        # Add title and explanation
        progress = step / self.total_steps
        
        if progress == 0:
            title = "Initial Misaligned Embedding Spaces"
            explanation = "Starting with separate embedding spaces for images and text"
        elif progress < 0.25:
            title = "Beginning Contrastive Learning Alignment"
            explanation = "Starting to align corresponding representations"
        elif progress < 0.5:
            title = "Contrastive Learning Alignment in Progress"
            explanation = "Corresponding points moving toward shared space"
        elif progress < 0.75:
            title = "Advanced Contrastive Learning Alignment"
            explanation = "Embedding spaces becoming more aligned"
        elif progress < 1.0:
            title = "Nearing Optimal Alignment"
            explanation = "Image and text embeddings converging to shared space"
        else:
            title = "Aligned Multimodal Embedding Space"
            explanation = "Contrastive learning has successfully aligned the embedding spaces"
        
        plt.suptitle(title, fontsize=22, fontweight='bold', y=0.98)
        fig.text(0.5, 0.02, explanation, ha='center', fontsize=16)
        
        # Add progress indicator
        fig.text(0.5, 0.05, f"Training Progress: {int(progress * 100)}%", 
                ha='center', fontsize=14, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", fc='white', ec='gray', alpha=0.7))
        
        # Add attribution
        fig.text(0.95, 0.01, "Visualization by Mikey Bee", 
                ha='right', va='bottom', fontsize=8, 
                color='gray', style='italic')
        
        # Format step number with leading zeros
        padded_step = str(step).zfill(len(str(self.total_steps)))
        
        # Save the figure
        plt.tight_layout(rect=[0, 0.07, 1, 0.96])
        plt.savefig(f"{self.output_dir}/step_{padded_step}.png", bbox_inches='tight')
        plt.close()
    
    def _create_animation(self):
        """Create an animated video from the rendered frames."""
        try:
            import imageio
            import glob
            
            # Get all step images
            image_files = sorted(glob.glob(f"{self.output_dir}/step_*.png"))
            
            # Create GIF animation
            print("Creating animated GIF...")
            with imageio.get_writer(f"{self.output_dir}/contrastive_learning_3d.gif", mode='I', fps=10) as writer:
                for image_file in image_files:
                    image = imageio.imread(image_file)
                    writer.append_data(image)
            
            # Try to create MP4 animation if ffmpeg is available
            try:
                print("Creating MP4 animation...")
                with imageio.get_writer(f"{self.output_dir}/contrastive_learning_3d.mp4", 
                                      fps=20, quality=8, bitrate='8000k') as writer:
                    for image_file in image_files:
                        image = imageio.imread(image_file)
                        writer.append_data(image)
                print(f"Animation saved as {self.output_dir}/contrastive_learning_3d.mp4")
            except:
                print("Could not create MP4 (ffmpeg might be missing). GIF was created successfully.")
                
            print(f"Animation saved as {self.output_dir}/contrastive_learning_3d.gif")
            
        except ImportError:
            print("Could not create animation. Please install 'imageio' package.")
            print("Run: pip install imageio imageio-ffmpeg")
    
    def _ease_in_out_cubic(self, t):
        """Apply cubic easing function for smoother animation."""
        if t < 0.5:
            return 4 * t * t * t
        else:
            p = 2 * t - 2
            return 0.5 * p * p * p + 1

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create a 3D visualization of contrastive learning space alignment.")
    parser.add_argument("-s", "--steps", type=int, default=100, 
                       help="Number of transformation steps (default: 100)")
    parser.add_argument("-o", "--output", type=str, default="contrastive_3d_frames",
                       help="Output directory (default: contrastive_3d_frames)")
    
    args = parser.parse_args()
    
    visualizer = ContrastiveLearning3DVisualizer(args.output, args.steps)
    visualizer.create_visualization()
