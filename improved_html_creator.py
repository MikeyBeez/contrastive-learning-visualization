#!/usr/bin/env python3
"""
Improved HTML Creator for Contrastive Learning Visualization (Modular Version)
Author: Mikey Bee, 2025

This module creates an enhanced interactive HTML viewer for the contrastive learning
visualization with a modular approach for better maintainability.
"""

import os
import json
from html_components_structure import generate_html_header, generate_html_styles, generate_html_body
from html_components_scripts import generate_html_scripts
from frame_descriptions import generate_enhanced_frame_descriptions

def create_enhanced_html_viewer(output_dir, total_frames):
    """Create an enhanced HTML file for interactive viewing of the visualization."""
    # Calculate number of digits needed for frame numbering
    num_digits = len(str(total_frames - 1))
    
    # Generate descriptions for each frame
    descriptions = generate_enhanced_frame_descriptions(total_frames)
    descriptions_json = json.dumps(descriptions)
    
    # Create HTML content by combining components
    html_content = "\n".join([
        generate_html_header(),
        generate_html_styles(),
        generate_html_body(total_frames),
        generate_html_scripts(total_frames, num_digits, descriptions_json)
    ])
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Write the HTML file
    with open(f"{output_dir}/interactive_viewer.html", "w") as f:
        f.write(html_content)
    
    print(f"Enhanced interactive HTML viewer created: {output_dir}/interactive_viewer.html")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create an enhanced HTML viewer for contrastive learning visualization.")
    parser.add_argument("-f", "--frames", type=int, default=100, 
                       help="Total number of frames (default: 100)")
    parser.add_argument("-o", "--output", type=str, default="contrastive_frames",
                       help="Output directory (default: contrastive_frames)")
    
    args = parser.parse_args()
    create_enhanced_html_viewer(args.output, args.frames)
