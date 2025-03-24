#!/usr/bin/env python3
"""
Simplified Runner for Contrastive Learning Visualization
Author: Mikey Bee, 2025

This script creates a simplified visualization with proper progress feedback.
"""

import os
import argparse
import time
from visualizer import plot_spaces, plot_combined_space
from data_generator import generate_initial_spaces, CATEGORIES, CATEGORY_COLORS

def try_import(module_name):
    """Try to import a module and return whether it was successful."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def create_static_visualization(steps, output_dir):
    """Create simplified static visualization with matplotlib."""
    print(f"\n=== Creating Static Visualization with {steps} steps ===")
    start_time = time.time()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate initial spaces
    image_points_orig, text_points_orig = generate_initial_spaces()
    
    # Create copies to transform
    image_points = {k: v.copy() for k, v in image_points_orig.items()}
    text_points = {k: v.copy() for k, v in text_points_orig.items()}
    
    # Try to import the simplified visualization
    if try_import('simplified_static_visualization'):
        from simplified_static_visualization import plot_spaces as improved_plot_spaces
        from simplified_static_visualization import plot_combined_space as improved_plot_combined
        from simplified_static_visualization import create_animated_gif
        print("Using simplified visualization with progress feedback.")
    else:
        print("Using default visualization (no progress feedback).")
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
    
    # Calculate and show elapsed time
    elapsed_time = time.time() - start_time
    print(f"\nStatic visualization complete! {steps+1} frames created in '{output_dir}' folder.")
    print(f"Total time: {elapsed_time:.2f} seconds ({elapsed_time/steps:.2f} seconds per frame)")
    print(f"To view the visualization, open: {output_dir}/combined_space.png")

def main():
    """Main function to run the simplified visualization."""
    parser = argparse.ArgumentParser(description="Create simplified visualizations of contrastive learning space alignment.")
    parser.add_argument("-s", "--steps", type=int, default=100, 
                       help="Number of transformation steps (default: 100)")
    parser.add_argument("-o", "--output", type=str, default="contrastive_viz",
                       help="Output directory (default: contrastive_viz)")
    
    args = parser.parse_args()
    
    # Welcome message
    print("\n========================================================")
    print("  Simplified Contrastive Learning Visualization Generator  ")
    print("========================================================")
    print(f"Steps: {args.steps}")
    print(f"Output directory: {args.output}")
    print("--------------------------------------------------------")
    
    # Create visualization
    create_static_visualization(args.steps, args.output)
    
    print("\n========================================================")
    print("Visualization completed successfully!")
    print("========================================================")

if __name__ == "__main__":
    main()
