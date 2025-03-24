#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_spaces(image_points, text_points, step, total_steps, output_dir, categories, category_colors):
    """Create a visualization of the two spaces at a given step"""
    # Set up figure with higher DPI for better quality
    plt.figure(figsize=(15, 7))
    
    # Plot image space
    plt.subplot(1, 2, 1)
    
    # Plot points by category
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            if item in image_points:
                point = image_points[item]
                plt.scatter(point[0], point[1], s=150, alpha=0.7, 
                           color=category_color, edgecolors='black')
                plt.annotate(item.upper(), (point[0], point[1]), fontsize=8, 
                           ha='center', va='center', weight='bold')
    
    plt.title('Image Space', fontsize=16, fontweight='bold')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    
    # Plot text space
    plt.subplot(1, 2, 2)
    
    # Plot points by category
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            if item in text_points:
                point = text_points[item]
                plt.scatter(point[0], point[1], s=150, alpha=0.7, 
                           color=category_color, edgecolors='black')
                plt.annotate(f"T:{item.upper()}", (point[0], point[1]), fontsize=8, 
                           ha='center', va='center', weight='bold')
    
    plt.title('Text Space', fontsize=16, fontweight='bold')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    
    # Add title and explanation
    plt.suptitle(f'Contrastive Learning Space Alignment - Step {step}/{total_steps}', 
                fontsize=18, fontweight='bold')
    
    # Add explanation based on step
    if step == 0:
        explanation = "Starting with misaligned spaces: similar concepts are in different positions"
    elif step < total_steps // 4:
        explanation = "Beginning alignment through contrastive learning..."
    elif step < total_steps // 2:
        explanation = "Gradually aligning spaces through contrastive learning..."
    elif step < 3 * total_steps // 4:
        explanation = "Similar concepts are being pulled together across spaces"
    else:
        explanation = "Spaces nearing perfect alignment"
    
    if step == total_steps:
        explanation = "Spaces aligned! Same concepts now occupy the same positions"
    
    plt.figtext(0.5, 0.01, explanation, ha='center', fontsize=14)
    
    # Save the figure with proper zero-padding in filename for correct sorting
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    
    # Format step number with leading zeros
    padded_step = str(step).zfill(len(str(total_steps)))
    
    plt.savefig(f"{output_dir}/step_{padded_step}.png", dpi=150, bbox_inches='tight')
    plt.close()

def plot_combined_space(image_points, text_points, output_dir, categories, category_colors):
    """Create a visualization of the final aligned space"""
    plt.figure(figsize=(12, 10))
    
    # Add legend for categories
    for category, color in category_colors.items():
        plt.scatter([], [], s=100, color=color, label=category.capitalize())
    
    # Plot points by category
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            # Plot image points
            if item in image_points:
                img_point = image_points[item]
                plt.scatter(img_point[0], img_point[1], s=150, alpha=0.7, 
                           color=category_color, edgecolors='black')
                plt.annotate(item.upper(), (img_point[0], img_point[1]), fontsize=8, 
                           ha='center', va='center', weight='bold')
            
            # Plot text points with slight offset
            if item in text_points:
                txt_point = text_points[item]
                offset = np.array([0.02, -0.02])
                plt.scatter(txt_point[0], txt_point[1], s=150, alpha=0.4, 
                          color=category_color, edgecolors='black', marker='s')
                plt.annotate(f"T:{item.upper()}", 
                           (txt_point[0] + offset[0], txt_point[1] + offset[1]), 
                           fontsize=8, ha='center', va='center', weight='bold')
                
                # Draw connecting line
                plt.plot([img_point[0], txt_point[0]], [img_point[1], txt_point[1]], 
                         'k--', alpha=0.3)
    
    plt.legend(loc='upper right', fontsize=12)
    
    # Add title and explanation
    plt.title('Aligned Shared Space', fontsize=18, fontweight='bold')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    
    plt.figtext(0.5, 0.01, "Image and text representations now occupy the same semantic space", 
               ha='center', fontsize=14)
    
    # Save the figure
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(f"{output_dir}/combined_space.png", dpi=150, bbox_inches='tight')
    plt.close()
