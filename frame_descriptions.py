#!/usr/bin/env python3
"""
Frame Descriptions for Contrastive Learning Visualization
Author: Mikey Bee, 2025

This module provides detailed descriptions for each frame of the visualization.
"""

def generate_enhanced_frame_descriptions(total_frames):
    """Generate more detailed explanatory text for each frame of the visualization."""
    descriptions = []
    
    # First frame description
    descriptions.append({
        "title": "Initial Misaligned Spaces",
        "text": "Starting with separate embedding spaces: similar concepts occupy different positions in image vs. text space.",
        "technical": "In contrastive learning, different modalities initially have their own separate feature spaces with different structures and orientations."
    })
    
    # Generate descriptions for intermediate frames
    quarter = total_frames // 4
    for i in range(1, total_frames):
        if i < quarter:
            descriptions.append({
                "title": f"Beginning Alignment (Step {i})",
                "text": "Contrastive learning begins pulling corresponding points together across modalities.",
                "technical": "The contrastive loss function minimizes distance between positive pairs (same concept in different modalities) while pushing apart negative pairs."
            })
        elif i < 2 * quarter:
            descriptions.append({
                "title": f"Progressive Alignment (Step {i})",
                "text": "Gradual alignment continues as the embedding spaces transform toward a common structure.",
                "technical": "Both image and text encoders are trained concurrently, adjusting their parameters to project semantically similar concepts to nearby regions."
            })
        elif i < 3 * quarter:
            descriptions.append({
                "title": f"Approaching Alignment (Step {i})",
                "text": "Similar concepts across modalities are now positioned much closer in the embedding space.",
                "technical": "The temperature parameter in the contrastive loss controls how sharply the model focuses on the hardest negative examples."
            })
        elif i < total_frames - 1:
            descriptions.append({
                "title": f"Near-Complete Alignment (Step {i})",
                "text": "Embedding spaces are nearly aligned, enabling effective cross-modal retrieval.",
                "technical": "The projection heads transform the representation to a space where contrastive loss is applied, often discarded after training."
            })
        else:
            descriptions.append({
                "title": "Complete Alignment",
                "text": "Spaces aligned! Same concepts now occupy similar positions across modalities.",
                "technical": "A successful alignment enables zero-shot transfer between modalities and robust multimodal fusion."
            })
    
    # Final combined view description
    descriptions.append({
        "title": "Combined Multimodal Space",
        "text": "The final shared embedding space where both modalities effectively represent the same concepts.",
        "technical": "This shared space enables cross-modal operations like image-to-text retrieval, text-to-image retrieval, and zero-shot transfer learning."
    })
    
    return descriptions
