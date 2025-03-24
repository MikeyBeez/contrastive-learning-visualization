#!/usr/bin/env python3
"""
Enhanced Contrastive Learning Visualization Runner
Author: Mikey Bee, 2025

This script brings together all the enhanced visualization techniques:
1. Improved static visualization with matplotlib
2. 3D visualization for more expressive representation
3. Manim animation for high-quality video output
4. HTML interactive viewer with advanced features

Usage:
  python enhanced_runner.py --mode all --steps 100 --output contrastive_viz
  
  Mode options:
    - static: Generate improved static frames only
    - 3d: Generate 3D visualization only
    - manim: Generate Manim animation only
    - html: Generate improved HTML viewer only
    - all: Generate all visualizations (default)
"""

import os
import argparse
import subprocess
import sys
import shutil
from importlib.util import find_spec
from visualizer import plot_spaces, plot_combined_space
from html_creator import create_html_viewer
from data_generator import generate_initial_spaces, CATEGORIES, CATEGORY_COLORS

# Import the new 3D visualizer
from improved_3d_visualizer import ContrastiveLearning3DVisualizer

def check_dependencies(mode):
    """Check if required dependencies are installed based on mode."""
    missing_dependencies = []
    
    if mode in ["static", "3d", "all"]:
        for module in ["numpy", "matplotlib"]:
            if find_spec(module) is None:
                missing_dependencies.append(module)
    
    if mode in ["3d", "all"]:
        for module in ["imageio"]:
            if find_spec(module) is None:
                missing_dependencies.append(module)
    
    if mode in ["manim", "all"]:
        for module in ["manim"]:
            if find_spec(module) is None:
                missing_dependencies.append(module)
    
    if missing_dependencies:
        print(f"Error: Missing dependencies: {', '.join(missing_dependencies)}")
        print("Please install the required packages:")
        
        if "manim" in missing_dependencies:
            print("For Manim: pip install manim")
        
        if set(missing_dependencies) - {"manim"}:
            modules = set(missing_dependencies) - {"manim"}
            print(f"For other dependencies: pip install {' '.join(modules)}")
        
        return False
    
    return True

def create_static_visualization(steps, output_dir):
    """Create improved static visualization with matplotlib."""
    print(f"\n=== Creating Enhanced Static Visualization with {steps} steps ===")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate initial spaces
    image_points_orig, text_points_orig = generate_initial_spaces()
    
    # Create copies to transform
    image_points = {k: v.copy() for k, v in image_points_orig.items()}
    text_points = {k: v.copy() for k, v in text_points_orig.items()}
    
    # Import the improved plot_spaces function
    from improved_static_visualization import plot_spaces as improved_plot_spaces
    from improved_static_visualization import plot_combined_space as improved_plot_combined
    from improved_static_visualization import create_animated_gif
    
    # Plot initial state
    improved_plot_spaces(image_points, text_points, 0, steps, output_dir, CATEGORIES, CATEGORY_COLORS)
    
    # For each step, transform the spaces
    for step in range(1, steps + 1):
        # Calculate interpolation parameter
        t = step / steps
        
        # For each item, interpolate between original and target
        for item in image_points:
            if item in text_points:
                # Calculate target position (halfway between points)
                target = (image_points_orig[item] + text_points_orig[item]) / 2
                
                # Move both points toward the target
                image_points[item] = image_points_orig[item] * (1 - t) + target * t
                text_points[item] = text_points_orig[item] * (1 - t) + target * t
        
        # Plot current state
        improved_plot_spaces(image_points, text_points, step, steps, output_dir, CATEGORIES, CATEGORY_COLORS)
    
    # Create combined space visualization
    improved_plot_combined(image_points, text_points, output_dir, CATEGORIES, CATEGORY_COLORS)
    
    # Create animated GIF
    create_animated_gif(output_dir, steps)
    
    # Create enhanced HTML viewer
    from improved_html_creator import create_enhanced_html_viewer
    create_enhanced_html_viewer(output_dir, steps + 1)
    
    print(f"Enhanced static visualization complete! {steps+1} frames created in '{output_dir}' folder.")
    print(f"To view the visualization, open: {output_dir}/interactive_viewer.html")

def create_3d_visualization(steps, output_dir):
    """Create 3D visualization."""
    print(f"\n=== Creating 3D Visualization with {steps} steps ===")
    
    # Create output directory with 3d suffix
    output_dir_3d = f"{output_dir}_3d"
    
    # Create the 3D visualization
    visualizer = ContrastiveLearning3DVisualizer(output_dir_3d, steps)
    visualizer.create_visualization()
    
    print(f"3D visualization complete! {steps+1} frames created in '{output_dir_3d}' folder.")
    print(f"Animation saved as: {output_dir_3d}/contrastive_learning_3d.gif")

def create_manim_animation(steps, output_dir):
    """Create Manim animation."""
    print(f"\n=== Creating Manim Animation ===")
    
    # Set environment variable for output directory
    os.environ["MEDIA_DIR"] = output_dir
    
    # Run the improved Manim script
    try:
        command = [
            sys.executable, 
            "improved_manim_animation.py", 
            "-qh", # High quality
            "--disable_caching",
            f"--output_file=contrastive_learning"
        ]
        
        subprocess.run(command, check=True)
        print("Manim animation created successfully!")
        
        # Copy the output file to the desired location if needed
        manim_output = "./media/videos/improved_manim_animation/1080p60/contrastive_learning.mp4"
        if os.path.exists(manim_output):
            os.makedirs(output_dir, exist_ok=True)
            shutil.copy(manim_output, f"{output_dir}/contrastive_learning_manim.mp4")
            print(f"Animation saved to: {output_dir}/contrastive_learning_manim.mp4")
    
    except subprocess.CalledProcessError as e:
        print(f"Error running Manim animation: {e}")
        return False
    
    return True

def create_improved_html_viewer(steps, output_dir):
    """Create an improved standalone HTML viewer."""
    print(f"\n=== Creating Enhanced Interactive HTML Viewer ===")
    
    # Ensure relevant directories exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create HTML viewer using the improved version
    from improved_html_creator import create_enhanced_html_viewer
    create_enhanced_html_viewer(output_dir, steps + 1)
    
    print(f"Enhanced HTML viewer created: {output_dir}/interactive_viewer.html")

def main():
    """Main function to run the enhanced visualizations."""
    parser = argparse.ArgumentParser(description="Create enhanced visualizations of contrastive learning space alignment.")
    parser.add_argument("-m", "--mode", type=str, choices=["static", "3d", "manim", "html", "all"], 
                       default="all", help="Visualization mode to run (default: all)")
    parser.add_argument("-s", "--steps", type=int, default=100, 
                       help="Number of transformation steps (default: 100)")
    parser.add_argument("-o", "--output", type=str, default="contrastive_viz",
                       help="Output directory prefix (default: contrastive_viz)")
    
    args = parser.parse_args()
    
    # Welcome message
    print("\n========================================================")
    print("  Enhanced Contrastive Learning Visualization Generator  ")
    print("========================================================")
    print(f"Mode: {args.mode}")
    print(f"Steps: {args.steps}")
    print(f"Output directory: {args.output}")
    print("--------------------------------------------------------")
    
    # Check dependencies
    if not check_dependencies(args.mode):
        return
    
    # Create visualizations based on mode
    if args.mode in ["static", "all"]:
        create_static_visualization(args.steps, f"{args.output}_static")
    
    if args.mode in ["3d", "all"]:
        create_3d_visualization(args.steps, args.output)
    
    if args.mode in ["manim", "all"]:
        create_manim_animation(args.steps, f"{args.output}_manim")
    
    if args.mode in ["html", "all"]:
        create_improved_html_viewer(args.steps, f"{args.output}_html")
    
    print("\n========================================================")
    print("All requested visualizations completed successfully!")
    print("========================================================")

if __name__ == "__main__":
    main()
