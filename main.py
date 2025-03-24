#!/usr/bin/env python3
import os
import argparse
from data_generator import generate_initial_spaces, CATEGORIES, CATEGORY_COLORS
from visualizer import plot_spaces, plot_combined_space
from html_creator import create_html_viewer

def create_visualization(total_steps=100, output_dir="contrastive_frames"):
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Creating visualization with {total_steps} steps...")
    
    # Generate initial spaces
    image_points_orig, text_points_orig = generate_initial_spaces()
    
    # Create a copy to transform
    image_points = {k: v.copy() for k, v in image_points_orig.items()}
    text_points = {k: v.copy() for k, v in text_points_orig.items()}
    
    # Plot initial state
    plot_spaces(image_points, text_points, 0, total_steps, output_dir, CATEGORIES, CATEGORY_COLORS)
    
    # For each step, transform the spaces
    for step in range(1, total_steps + 1):
        # Calculate interpolation parameter
        t = step / total_steps
        
        # For each item, interpolate between original and target
        for item in image_points:
            if item in text_points:
                # Calculate target position (halfway between points)
                target = (image_points_orig[item] + text_points_orig[item]) / 2
                
                # Move both points toward the target
                image_points[item] = image_points_orig[item] * (1 - t) + target * t
                text_points[item] = text_points_orig[item] * (1 - t) + target * t
        
        # Plot current state
        plot_spaces(image_points, text_points, step, total_steps, output_dir, CATEGORIES, CATEGORY_COLORS)
    
    # Create combined space visualization
    plot_combined_space(image_points, text_points, output_dir, CATEGORIES, CATEGORY_COLORS)
    
    print(f"Visualization complete! {total_steps+1} frames created in '{output_dir}' folder.")
    print(f"Creating interactive HTML viewer...")
    create_html_viewer(output_dir, total_steps + 1)
    print(f"To view the visualization, open: {output_dir}/interactive_viewer.html")

def main():
    parser = argparse.ArgumentParser(description="Create a visualization of contrastive learning space alignment.")
    parser.add_argument("-s", "--steps", type=int, default=100, 
                       help="Number of transformation steps (default: 100)")
    parser.add_argument("-o", "--output", type=str, default="contrastive_frames",
                       help="Output directory (default: contrastive_frames)")
    
    args = parser.parse_args()
    create_visualization(args.steps, args.output)

if __name__ == "__main__":
    main()
