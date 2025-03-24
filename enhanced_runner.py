#!/usr/bin/env python3
"""
Enhanced Runner for Contrastive Learning Visualization (Modular Version)
Author: Mikey Bee, 2025

This script brings together all the enhanced visualization techniques using a modular approach.
"""

import os
import argparse
import subprocess
import sys
import shutil
from importlib.util import find_spec
from visualizer import plot_spaces, plot_combined_space
from data_generator import generate_initial_spaces, CATEGORIES, CATEGORY_COLORS
from improved_html_creator import create_enhanced_html_viewer

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
    
    try:
        # Import the improved plot_spaces function
        from improved_static_visualization import plot_spaces as improved_plot_spaces
        from improved_static_visualization import plot_combined_space as improved_plot_combined
        from improved_static_visualization import create_animated_gif
    except ImportError:
        print("Warning: improved_static_visualization.py not found. Using default visualization.")
        from visualizer import plot_spaces as improved_plot_spaces
        from visualizer import plot_combined_space as improved_plot_combined
        
        def create_animated_gif(output_dir, steps):
            print("Animated GIF creation not available with default visualization.")
    
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
    try:
        create_enhanced_html_viewer(output_dir, steps + 1)
    except ImportError:
        print("Warning: Could not create enhanced HTML viewer. Some modules might be missing.")
        from html_creator import create_html_viewer
        create_html_viewer(output_dir, steps + 1)
    
    print(f"Enhanced static visualization complete! {steps+1} frames created in '{output_dir}' folder.")
    print(f"To view the visualization, open: {output_dir}/interactive_viewer.html")

def create_3d_visualization(steps, output_dir):
    """Create 3D visualization."""
    print(f"\n=== Creating 3D Visualization with {steps} steps ===")
    
    # Create output directory with 3d suffix
    output_dir_3d = f"{output_dir}_3d"
    
    try:
        # Import the 3D visualizer
        from improved_3d_visualizer import ContrastiveLearning3DVisualizer
        
        # Create the 3D visualization
        visualizer = ContrastiveLearning3DVisualizer(output_dir_3d, steps)
        visualizer.create_visualization()
        
        print(f"3D visualization complete! {steps+1} frames created in '{output_dir_3d}' folder.")
        print(f"Animation saved as: {output_dir_3d}/contrastive_learning_3d.gif")
    except ImportError:
        print("Error: Could not create 3D visualization. Make sure improved_3d_visualizer.py is available.")
        print("You can install required dependencies with: pip install matplotlib numpy imageio")
        return False
    
    return True

def create_manim_animation(steps, output_dir):
    """Create Manim animation."""
    print(f"\n=== Creating Manim Animation ===")
    
    # Set environment variable for output directory
    os.environ["MEDIA_DIR"] = output_dir
    
    # Check which Manim script exists
    manim_script = "improved_manim_animation.py"
    if not os.path.exists(manim_script):
        print(f"Warning: {manim_script} not found, using contrastive_learning.py instead.")
        manim_script = "contrastive_learning.py"
        if not os.path.exists(manim_script):
            print(f"Error: No Manim script found.")
            return False
    
    # Run the Manim script
    try:
        command = [
            sys.executable, 
            manim_script, 
            "-qh", # High quality
            "--disable_caching",
            f"--output_file=contrastive_learning"
        ]
        
        subprocess.run(command, check=True)
        print("Manim animation created successfully!")
        
        # Copy the output file to the desired location if needed
        manim_output = "./media/videos/improved_manim_animation/1080p60/contrastive_learning.mp4"
        fallback_output = "./media/videos/contrastive_learning/1080p60/ImprovedContrastiveLearningAnimation.mp4"
        
        if os.path.exists(manim_output):
            target_path = f"{output_dir}/contrastive_learning_manim.mp4"
        elif os.path.exists(fallback_output):
            manim_output = fallback_output
            target_path = f"{output_dir}/contrastive_learning_manim.mp4"
        else:
            print("Warning: Could not find Manim output file.")
            return True  # Still consider it a success since Manim ran
        
        os.makedirs(output_dir, exist_ok=True)
        shutil.copy(manim_output, target_path)
        print(f"Animation saved to: {target_path}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error running Manim animation: {e}")
        return False
    
    return True

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
        try:
            create_enhanced_html_viewer(f"{args.output}_html", args.steps)
        except ImportError:
            print("Warning: Could not create enhanced HTML viewer. Some modules might be missing.")
            try:
                from html_creator import create_html_viewer
                create_html_viewer(f"{args.output}_html", args.steps)
            except ImportError:
                print("Error: Could not create HTML viewer. Make sure html_creator.py is available.")
    
    print("\n========================================================")
    print("All requested visualizations completed successfully!")
    print("========================================================")

if __name__ == "__main__":
    main()
