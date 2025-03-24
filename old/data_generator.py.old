#!/usr/bin/env python3
import numpy as np

# Create categories with more data points
CATEGORIES = {
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'horse', 'elephant', 'tiger', 'lion', 'bear'],
    'vehicles': ['car', 'boat', 'plane', 'train', 'bus', 'truck', 'motorcycle', 'helicopter', 'submarine', 'bicycle'],
    'food': ['apple', 'banana', 'orange', 'pizza', 'burger', 'pasta', 'sushi', 'bread', 'cheese', 'cake'],
    'nature': ['mountain', 'ocean', 'forest', 'river', 'desert', 'cloud', 'flower', 'sun', 'moon', 'star']
}

# Colors for each category
CATEGORY_COLORS = {
    'animals': 'royalblue',
    'vehicles': 'forestgreen',
    'food': 'darkorange',
    'nature': 'purple'
}

def generate_initial_spaces():
    """
    Generate initial image and text spaces with items clustered by category.
    The spaces are intentionally misaligned.
    """
    np.random.seed(42)  # For reproducibility
    
    # Create image space - clustered by category
    image_points = {}
    # Place each category in a different quadrant
    category_centers = {
        'animals': np.array([0.75, 0.75]),
        'vehicles': np.array([0.25, 0.25]),
        'food': np.array([0.25, 0.75]),
        'nature': np.array([0.75, 0.25])
    }
    
    for category, items in CATEGORIES.items():
        for item in items:
            image_points[item] = category_centers[category] + np.random.normal(0, 0.07, 2)
    
    # Create text space - differently oriented
    text_points = {}
    
    # Create a rotation and scaling transformation
    rotation = np.array([
        [0, -1],
        [1, 0]
    ])
    
    for item in image_points:
        # Apply rotation and shift to create a differently oriented space
        text_points[item] = rotation @ image_points[item] + np.array([0.1, 0.1])
    
    return image_points, text_points
