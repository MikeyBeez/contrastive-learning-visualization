from manim import *
import numpy as np

class ContrastiveLearningAnimation(Scene):
    def construct(self):
        # Configuration
        total_steps = 100
        np.random.seed(42)  # For reproducibility
        
        # Categories and their colors
        categories = {
            'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'horse'],
            'vehicles': ['car', 'boat', 'plane', 'train', 'bus', 'truck'],
            'food': ['apple', 'banana', 'orange', 'pizza', 'burger', 'pasta'],
            'nature': ['mountain', 'ocean', 'forest', 'river', 'desert', 'cloud']
        }
        
        category_colors = {
            'animals': BLUE,
            'vehicles': GREEN,
            'food': ORANGE,
            'nature': PURPLE
        }
        
        # Generate initial spaces
        image_points, text_points = self.generate_initial_spaces(categories)
        
        # Create visualization layout
        title = Text("Contrastive Learning Space Alignment", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create two coordinate systems for image and text spaces
        image_axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            axis_config={"color": GREY},
            x_length=4,
            y_length=4,
        ).scale(1.5)
        
        text_axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            axis_config={"color": GREY},
            x_length=4,
            y_length=4,
        ).scale(1.5)
        
        # Position the axes
        image_axes.move_to(LEFT * 3)
        text_axes.move_to(RIGHT * 3)
        
        # Add labels to the axes
        image_label = Text("Image Space", font_size=24)
        image_label.next_to(image_axes, UP)
        
        text_label = Text("Text Space", font_size=24)
        text_label.next_to(text_axes, UP)
        
        # Add everything to the scene
        self.play(
            Create(image_axes),
            Create(text_axes),
            Write(image_label),
            Write(text_label)
        )
        
        # Create dots for each item
        image_dots = {}
        text_dots = {}
        image_labels = {}
        text_labels = {}
        
        # Create dots and labels for image space
        for category, items in categories.items():
            color = category_colors[category]
            for item in items:
                # Convert the coordinates to Manim points
                point = image_points[item]
                position = image_axes.c2p(point[0], point[1])
                
                dot = Dot(position, color=color, radius=0.08)
                label = Text(item.upper(), font_size=14, color=WHITE)
                label.next_to(dot, UP, buff=0.1)
                
                image_dots[item] = dot
                image_labels[item] = label
                self.add(dot, label)
        
        # Create dots and labels for text space
        for category, items in categories.items():
            color = category_colors[category]
            for item in items:
                # Convert the coordinates to Manim points
                point = text_points[item]
                position = text_axes.c2p(point[0], point[1])
                
                dot = Dot(position, color=color, radius=0.08)
                label = Text(f"T:{item.upper()}", font_size=14, color=WHITE)
                label.next_to(dot, UP, buff=0.1)
                
                text_dots[item] = dot
                text_labels[item] = label
                self.add(dot, label)
        
        # Create progress tracker
        progress_bar_bg = Rectangle(height=0.2, width=10, fill_color=GREY, fill_opacity=0.3)
        progress_bar_bg.to_edge(DOWN, buff=0.5)
        progress_bar = Rectangle(height=0.2, width=0, fill_color=BLUE, fill_opacity=1)
        progress_bar.align_to(progress_bar_bg, LEFT)
        progress_bar.to_edge(DOWN, buff=0.5)
        
        progress_label = Text("Step: 0/100", font_size=20)
        progress_label.next_to(progress_bar_bg, UP)
        
        self.play(
            Create(progress_bar_bg),
            Create(progress_bar),
            Write(progress_label)
        )
        
        # Add explanation text
        explanation = Text("Starting with misaligned spaces", font_size=24)
        explanation.next_to(progress_label, UP)
        self.play(Write(explanation))
        
        # Wait a moment to let viewer see the initial state
        self.wait(2)
        
        # Animation loop - transform spaces
        for step in range(1, total_steps + 1):
            # Update explanation text
            if step < total_steps // 4:
                new_explanation = Text("Beginning alignment process...", font_size=24)
            elif step < total_steps // 2:
                new_explanation = Text("Gradually aligning spaces...", font_size=24)
            elif step < 3 * total_steps // 4:
                new_explanation = Text("Similar concepts being pulled together...", font_size=24)
            else:
                new_explanation = Text("Spaces nearing perfect alignment", font_size=24)
                
            if step == total_steps:
                new_explanation = Text("Spaces aligned! Same concepts now occupy the same positions", font_size=24)
            
            new_explanation.next_to(progress_label, UP)
            
            # Update progress bar
            new_progress = Rectangle(
                height=0.2, 
                width=10 * (step / total_steps), 
                fill_color=BLUE, 
                fill_opacity=1
            )
            new_progress.align_to(progress_bar_bg, LEFT)
            new_progress.to_edge(DOWN, buff=0.5)
            
            new_progress_label = Text(f"Step: {step}/{total_steps}", font_size=20)
            new_progress_label.next_to(progress_bar_bg, UP)
            
            # Calculate interpolation parameter
            t = step / total_steps
            
            # Create animations for all dots
            dot_animations = []
            label_animations = []
            
            for item in image_points:
                if item in text_points:
                    # Calculate target position (center point)
                    img_point = image_points[item]
                    txt_point = text_points[item]
                    target = (img_point + txt_point) / 2
                    
                    # Calculate new positions
                    new_img_pos = img_point * (1 - t) + target * t
                    new_txt_pos = txt_point * (1 - t) + target * t
                    
                    # Convert to Manim coordinates
                    new_img_manim_pos = image_axes.c2p(new_img_pos[0], new_img_pos[1])
                    new_txt_manim_pos = text_axes.c2p(new_txt_pos[0], new_txt_pos[1])
                    
                    # Add animations to move dots
                    dot_animations.append(image_dots[item].animate.move_to(new_img_manim_pos))
                    dot_animations.append(text_dots[item].animate.move_to(new_txt_manim_pos))
                    
                    # Add animations to move labels
                    label_animations.append(image_labels[item].animate.next_to(new_img_manim_pos, UP, buff=0.1))
                    label_animations.append(text_labels[item].animate.next_to(new_txt_manim_pos, UP, buff=0.1))
            
            # Play all animations together
            self.play(
                *dot_animations,
                *label_animations,
                Transform(progress_bar, new_progress),
                Transform(progress_label, new_progress_label),
                Transform(explanation, new_explanation),
                run_time=0.5  # Make each step fairly quick
            )
        
        # Final state - show comparison lines
        self.wait(1)
        connecting_lines = []
        
        for item in image_points:
            if item in text_points:
                start_pos = image_dots[item].get_center()
                end_pos = text_dots[item].get_center()
                line = DashedLine(start_pos, end_pos, color=GREY, dash_length=0.1)
                connecting_lines.append(line)
        
        self.play(
            *[Create(line) for line in connecting_lines]
        )
        
        # Final explanation
        final_explanation = Text("Image and text points now occupy the same positions in their spaces", font_size=24)
        final_explanation.next_to(progress_label, UP)
        
        self.play(Transform(explanation, final_explanation))
        
        # Hold final state
        self.wait(3)
    
    def generate_initial_spaces(self, categories):
        """Generate initial image and text spaces with items clustered by category"""
        # Create image space - clustered by category
        image_points = {}
        # Place each category in a different quadrant
        category_centers = {
            'animals': np.array([0.75, 0.75]),
            'vehicles': np.array([0.25, 0.25]),
            'food': np.array([0.25, 0.75]),
            'nature': np.array([0.75, 0.25])
        }
        
        for category, items in categories.items():
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
