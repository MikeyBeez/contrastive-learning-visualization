#!/bin/bash
# Run the contrastive learning visualization with 100 steps
python3 main.py --steps 100

# Open the visualization in the default browser
echo "Opening the visualization in your browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open contrastive_frames/interactive_viewer.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open contrastive_frames/interactive_viewer.html
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    start contrastive_frames/interactive_viewer.html
else
    echo "Please open the visualization manually: contrastive_frames/interactive_viewer.html"
fi
