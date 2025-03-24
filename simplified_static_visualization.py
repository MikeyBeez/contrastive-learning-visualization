#!/usr/bin/env python3
"""
Simplified version of the static visualization with progress indicators
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import time

def plot_spaces(image_points, text_points, step, total_steps, output_dir, categories, category_colors):
    """Create a simplified visualization of the two spaces at a given step with progress feedback"""
    # Print progress indicator
    progress_percent = int((step / total_steps) * 100)
    print(f"\rGenerating frame {step}/{total_steps} [{progress_percent}%]", end="", flush=True)
    
    # Set up figure with simple layout
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Plot image space
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            if item in image_points:
                point = image_points[item]
                ax1.scatter(point[0], point[1], s=150, alpha=0.8, 
                           color=category_color, edgecolors='white', linewidth=1.5)
                
                # Add text with improved styling - simplified
                ax1.annotate(item.upper(), (point[0], point[1]), fontsize=9, 
                           ha='center', va='center', weight='bold',
                           color='white', bbox=dict(boxstyle="round,pad=0.2", 
                                                 fc=category_color, ec="none", alpha=0.7))
    
    ax1.set_title('Image Embedding Space', fontsize=16, fontweight='bold')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xlabel('Dimension 1', fontsize=12)
    ax1.set_ylabel('Dimension 2', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # Plot text space
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            if item in text_points:
                point = text_points[item]
                # Use square markers for text points to differentiate from image points
                ax2.scatter(point[0], point[1], s=150, alpha=0.8, 
                           color=category_color, edgecolors='white', linewidth=1.5,
                           marker='s')
                
                ax2.annotate(f"'{item.upper()}'", (point[0], point[1]), fontsize=9, 
                           ha='center', va='center', weight='bold',
                           color='white', bbox=dict(boxstyle="round,pad=0.2", 
                                                  fc=category_color, ec="none", alpha=0.7))
    
    ax2.set_title('Text Embedding Space', fontsize=16, fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Dimension 1', fontsize=12)
    ax2.set_ylabel('Dimension 2', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    # Add a title to the entire figure
    fig.suptitle(f'Contrastive Learning Space Alignment - Step {step}/{total_steps}', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Add attribution
    plt.figtext(0.95, 0.01, "Visualization by Mikey Bee", 
               ha='right', va='bottom', fontsize=8, 
               color='gray', style='italic')
    
    # Use standard adjust - no tight_layout
    plt.subplots_adjust(wspace=0.3, left=0.05, right=0.95, bottom=0.1, top=0.9)
    
    # Format step number with leading zeros
    padded_step = str(step).zfill(len(str(total_steps)))
    
    # Save the figure
    plt.savefig(f"{output_dir}/step_{padded_step}.png", dpi=150)
    plt.close()

def plot_combined_space(image_points, text_points, output_dir, categories, category_colors):
    """Create a simplified visualization of the final aligned space"""
    print("\rGenerating final combined view...", end="", flush=True)
    
    # Create figure
    plt.figure(figsize=(10, 8))
    
    # Add legend for categories with improved styling
    for category, color in category_colors.items():
        plt.scatter([], [], s=150, color=color, label=category.capitalize(), 
                   edgecolors='white', linewidth=1.5)
    
    plt.legend(loc='upper right', fontsize=12, framealpha=0.7, 
              title="Categories")
    
    # Plot points by category
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            # Plot image points with circle markers
            if item in image_points:
                img_point = image_points[item]
                plt.scatter(img_point[0], img_point[1], s=150, alpha=0.9, 
                           color=category_color, edgecolors='white', linewidth=1.5,
                           marker='o', zorder=10)
                
                plt.annotate(item.upper(), (img_point[0], img_point[1]), fontsize=9, 
                           ha='center', va='center', weight='bold',
                           color='white', bbox=dict(boxstyle="round,pad=0.2", 
                                                 fc=category_color, ec="none", alpha=0.7),
                           zorder=11)
            
            # Plot text points with square markers
            if item in text_points:
                txt_point = text_points[item]
                plt.scatter(txt_point[0], txt_point[1], s=150, alpha=0.7, 
                          color=category_color, edgecolors='white', linewidth=1.5,
                          marker='s', zorder=9)
                
                plt.annotate(f"'{item.upper()}'", 
                           (txt_point[0] + 0.02, txt_point[1] - 0.02), 
                           fontsize=9, ha='center', va='center', weight='bold',
                           color='white', bbox=dict(boxstyle="round,pad=0.2", 
                                                  fc=category_color, ec="none", alpha=0.6),
                           zorder=11)
                
                # Draw connecting line between corresponding points
                plt.plot([img_point[0], txt_point[0]], [img_point[1], txt_point[1]], 
                         'k--', alpha=0.3, zorder=5, linewidth=1.5)
                
                # Add a midpoint indicator to show where the points will converge
                mid_point = [(img_point[0] + txt_point[0])/2, (img_point[1] + txt_point[1])/2]
                plt.scatter(mid_point[0], mid_point[1], s=40, alpha=0.3, 
                           color='gray', marker='x', zorder=6)
    
    # Add title and explanation
    plt.title('Aligned Shared Embedding Space', fontsize=18, fontweight='bold')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xlabel('Dimension 1', fontsize=14)
    plt.ylabel('Dimension 2', fontsize=14)
    
    # Add explanation box
    explanation_text = "Image and text representations now occupy the same semantic space"
    plt.figtext(0.5, 0.02, explanation_text, 
               ha='center', fontsize=14, fontweight='bold', color='darkgreen')
    
    # Add attribution
    plt.figtext(0.95, 0.01, "Visualization by Mikey Bee", 
               ha='right', va='bottom', fontsize=8, 
               color='gray', style='italic')
    
    # Use standard adjust
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    # Save the figure
    plt.savefig(f"{output_dir}/combined_space.png", dpi=150)
    plt.close()
    
    print("\rCombined view generated!                 ")

def create_animated_gif(output_dir, total_steps, fps=10):
    """Create an animated GIF from the rendered frames"""
    print("\nCreating animated GIF...", end="", flush=True)
    
    try:
        import imageio
        import glob
        
        # Get all step images
        image_files = sorted(glob.glob(f"{output_dir}/step_*.png"))
        
        # Create GIF animation directly with imageio (simpler approach)
        with imageio.get_writer(f"{output_dir}/contrastive_learning_animation.gif", mode='I', fps=fps) as writer:
            for image_file in image_files:
                image = imageio.imread(image_file)
                writer.append_data(image)
        
        print(f"\rAnimation created: {output_dir}/contrastive_learning_animation.gif")
    except ImportError:
        print("\rCould not create animation. Please install imageio: pip install imageio")
