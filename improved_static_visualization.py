#!/usr/bin/env python3
"""
Fixed version of the improved static visualization that addresses the tight_layout warnings.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import ConnectionPatch

def plot_spaces(image_points, text_points, step, total_steps, output_dir, categories, category_colors):
    """Create an enhanced visualization of the two spaces at a given step"""
    # Set style for modern, clean look
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Set up figure with higher DPI for better quality
    fig = plt.figure(figsize=(16, 9), dpi=150)
    
    # Create a custom layout with more space for the plots
    gs = fig.add_gridspec(2, 2, height_ratios=[5, 1], width_ratios=[1, 1], 
                        hspace=0.3, wspace=0.2)
    
    # Plot image space
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Add a subtle background gradient for visual appeal
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    
    # Create a circular gradient centered at each category's mean position
    gradient = np.zeros_like(X)
    for category, items in categories.items():
        category_points = [image_points[item] for item in items if item in image_points]
        if category_points:
            mean_pos = np.mean(category_points, axis=0)
            category_gradient = np.exp(-10 * ((X - mean_pos[0])**2 + (Y - mean_pos[1])**2))
            gradient += category_gradient * 0.1  # Subtle effect
    
    ax1.imshow(gradient, extent=[0, 1, 0, 1], origin='lower', 
              cmap='Blues', alpha=0.1, aspect='auto')
    
    # Plot points by category with improved styling
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            if item in image_points:
                point = image_points[item]
                ax1.scatter(point[0], point[1], s=180, alpha=0.8, 
                           color=category_color, edgecolors='white', linewidth=1.5,
                           zorder=10)  # Ensure points are on top
                
                # Add text with improved styling
                ax1.annotate(item.upper(), (point[0], point[1]), fontsize=9, 
                           ha='center', va='center', weight='bold',
                           color='white', bbox=dict(boxstyle="round,pad=0.2", 
                                                 fc=category_color, ec="none", alpha=0.7),
                           zorder=11)  # Ensure text is on top
    
    ax1.set_title('Image Embedding Space', fontsize=18, fontweight='bold', pad=15)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xlabel('Dimension 1', fontsize=12)
    ax1.set_ylabel('Dimension 2', fontsize=12)
    
    # Add subtle grid lines
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # Plot text space
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Add similar gradient effect for text space
    gradient = np.zeros_like(X)
    for category, items in categories.items():
        category_points = [text_points[item] for item in items if item in text_points]
        if category_points:
            mean_pos = np.mean(category_points, axis=0)
            category_gradient = np.exp(-10 * ((X - mean_pos[0])**2 + (Y - mean_pos[1])**2))
            gradient += category_gradient * 0.1
    
    ax2.imshow(gradient, extent=[0, 1, 0, 1], origin='lower', 
              cmap='Blues', alpha=0.1, aspect='auto')
    
    # Plot points by category
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            if item in text_points:
                point = text_points[item]
                # Use square markers for text points to differentiate from image points
                ax2.scatter(point[0], point[1], s=160, alpha=0.8, 
                           color=category_color, edgecolors='white', linewidth=1.5,
                           marker='s', zorder=10)
                
                ax2.annotate(f"'{item.upper()}'", (point[0], point[1]), fontsize=9, 
                           ha='center', va='center', weight='bold',
                           color='white', bbox=dict(boxstyle="round,pad=0.2", 
                                                  fc=category_color, ec="none", alpha=0.7),
                           zorder=11)
    
    ax2.set_title('Text Embedding Space', fontsize=18, fontweight='bold', pad=15)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Dimension 1', fontsize=12)
    ax2.set_ylabel('Dimension 2', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    # Add connecting lines between corresponding points
    for item in image_points:
        if item in text_points:
            # Calculate opacity based on alignment progress
            t = step / total_steps
            img_point = image_points[item]
            txt_point = text_points[item]
            
            # Adjust opacity to highlight alignment process
            line_alpha = max(0.1, 1.0 - np.linalg.norm(np.array(img_point) - np.array(txt_point)))
            
            # Create a connection patch between the two points
            con = ConnectionPatch(
                xyA=img_point, xyB=txt_point,
                coordsA="data", coordsB="data",
                axesA=ax1, axesB=ax2,
                color='gray', linestyle='--', linewidth=1, alpha=line_alpha * 0.5,
                zorder=0  # Place lines behind points
            )
            fig.add_artist(con)
    
    # Add explanation in a text box
    explanation_ax = fig.add_subplot(gs[1, :])
    explanation_ax.axis('off')
    
    if step == 0:
        explanation = "Starting with misaligned spaces: similar concepts are in different positions"
        color = 'darkorange'
    elif step < total_steps // 4:
        explanation = "Beginning alignment through contrastive learning..."
        color = 'darkorange'
    elif step < total_steps // 2:
        explanation = "Gradually aligning spaces through contrastive learning..."
        color = 'darkcyan'
    elif step < 3 * total_steps // 4:
        explanation = "Similar concepts are being pulled together across spaces"
        color = 'darkcyan'
    else:
        explanation = "Spaces nearing perfect alignment"
        color = 'darkgreen'
    
    if step == total_steps:
        explanation = "Spaces aligned! Same concepts now occupy the same positions"
        color = 'darkgreen'
        
    # Add a progress bar
    progress = step / total_steps
    progress_height = 0.1
    progress_y = 0.4
    
    # Background bar
    explanation_ax.add_patch(plt.Rectangle((0.1, progress_y), 0.8, progress_height, 
                                        facecolor='lightgray', edgecolor='gray', 
                                        alpha=0.5, zorder=1))
    
    # Progress indicator
    progress_color = plt.cm.viridis(progress)  # Color changes with progress
    explanation_ax.add_patch(plt.Rectangle((0.1, progress_y), 0.8 * progress, progress_height, 
                                        facecolor=progress_color, edgecolor=None, 
                                        alpha=0.8, zorder=2))
    
    # Progress text
    explanation_ax.text(0.5, progress_y - 0.15, f"Progress: {int(progress * 100)}%", 
                       ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Step counter
    explanation_ax.text(0.9, progress_y, f"Step: {step}/{total_steps}", 
                       ha='center', va='center', fontsize=10)
    
    # Main explanation text
    explanation_ax.text(0.5, progress_y + 0.25, explanation, 
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       color=color, bbox=dict(boxstyle="round,pad=0.5", 
                                           fc='white', ec=color, alpha=0.7))
    
    # Add legend for categories
    legend_elements = []
    for category, color in category_colors.items():
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                      markerfacecolor=color, markersize=10, 
                                      label=category.capitalize()))
    
    legend = explanation_ax.legend(handles=legend_elements, loc='center left', 
                                 bbox_to_anchor=(0.1, 0.7), frameon=True, 
                                 fontsize=10, title="Categories", title_fontsize=12)
    
    # Add a title to the entire figure
    fig.suptitle(f'Contrastive Learning Space Alignment', 
                 fontsize=22, fontweight='bold', y=0.98)
    
    # Add attribution
    explanation_ax.text(0.95, 0.05, "Visualization by Mikey Bee", 
                       ha='right', va='bottom', fontsize=8, 
                       color='gray', style='italic')
    
    # Save the figure without tight_layout (source of the warnings)
    # Format step number with leading zeros
    padded_step = str(step).zfill(len(str(total_steps)))
    
    # Use a simpler approach: adjust subplot parameters instead of tight_layout
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
    
    # Save the figure
    plt.savefig(f"{output_dir}/step_{padded_step}.png", dpi=150)
    plt.close()

def plot_combined_space(image_points, text_points, output_dir, categories, category_colors):
    """Create an enhanced visualization of the final aligned space"""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(12, 10), dpi=150)
    
    # Create a subtle background gradient
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    
    # Create a circular gradient centered at each category's mean position
    gradient = np.zeros_like(X)
    for category, items in categories.items():
        category_points = []
        for item in items:
            if item in image_points:
                category_points.append(image_points[item])
        
        if category_points:
            mean_pos = np.mean(category_points, axis=0)
            category_gradient = np.exp(-5 * ((X - mean_pos[0])**2 + (Y - mean_pos[1])**2))
            gradient += category_gradient * 0.15
    
    plt.imshow(gradient, extent=[0, 1, 0, 1], origin='lower', 
              cmap='Blues', alpha=0.1, aspect='auto')
    
    # Add subtle contour lines to show embedding space topology
    contour_levels = np.linspace(0.1, 0.9, 5)
    contour = plt.contour(X, Y, gradient, levels=contour_levels, 
                         colors='blue', alpha=0.1, linestyles='solid', linewidths=0.5)
    
    # Add legend for categories with improved styling
    for category, color in category_colors.items():
        plt.scatter([], [], s=180, color=color, label=category.capitalize(), 
                   edgecolors='white', linewidth=1.5)
    
    legend = plt.legend(loc='upper right', fontsize=12, framealpha=0.7, 
                       title="Categories", title_fontsize=14)
    
    # Plot points by category
    for category, items in categories.items():
        category_color = category_colors[category]
        
        for item in items:
            # Plot image points with circle markers
            if item in image_points:
                img_point = image_points[item]
                plt.scatter(img_point[0], img_point[1], s=180, alpha=0.9, 
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
                plt.scatter(txt_point[0], txt_point[1], s=160, alpha=0.7, 
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
    plt.title('Aligned Shared Embedding Space', fontsize=22, fontweight='bold', pad=20)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xlabel('Dimension 1', fontsize=14)
    plt.ylabel('Dimension 2', fontsize=14)
    
    # Add explanation box
    explanation_text = "Image and text representations now occupy the same semantic space"
    plt.figtext(0.5, 0.02, explanation_text, 
               ha='center', fontsize=16, fontweight='bold', color='darkgreen', 
               bbox=dict(boxstyle="round,pad=0.5", fc='white', ec='darkgreen', alpha=0.7))
    
    # Add technical details
    tech_details = "Contrastive Learning Alignment Complete - Final State"
    plt.figtext(0.5, 0.06, tech_details, ha='center', fontsize=12, color='darkblue')
    
    # Add attribution
    plt.figtext(0.95, 0.01, "Visualization by Mikey Bee", 
               ha='right', va='bottom', fontsize=8, 
               color='gray', style='italic')
    
    # Adjust subplot parameters instead of using tight_layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)
    
    # Save the figure
    plt.savefig(f"{output_dir}/combined_space.png", dpi=200)
    plt.close()

def create_animated_gif(output_dir, total_steps, fps=10):
    """Create an animated GIF from the rendered frames"""
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.animation import PillowWriter
    import glob
    
    # Get all step images
    image_files = sorted(glob.glob(f"{output_dir}/step_*.png"))
    
    # Create figure that matches the size of the images
    sample_img = plt.imread(image_files[0])
    height, width, _ = sample_img.shape
    fig = plt.figure(figsize=(width/100, height/100), dpi=100)
    
    # Remove axes
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    # Create animation function
    def animate(i):
        img = plt.imread(image_files[i])
        ax.imshow(img)
        ax.set_title(f"Frame {i+1}/{len(image_files)}")
        return [ax]
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=len(image_files), interval=1000/fps)
    
    # Save as GIF
    writer = PillowWriter(fps=fps)
    anim.save(f"{output_dir}/contrastive_learning_animation.gif", writer=writer)
    
    print(f"Animation created: {output_dir}/contrastive_learning_animation.gif")
