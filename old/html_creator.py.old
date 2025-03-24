#!/usr/bin/env python3
import os

def generate_frame_descriptions(total_frames):
    """Generate descriptive text for each frame of the visualization"""
    descriptions = []
    
    # First frame description
    descriptions.append("Starting with misaligned spaces: similar concepts are in different positions")
    
    # Generate descriptions for intermediate frames
    quarter = total_frames // 4
    for i in range(1, total_frames):
        if i < quarter:
            descriptions.append(f"Beginning alignment through contrastive learning - step {i}")
        elif i < 2 * quarter:
            descriptions.append(f"Gradually aligning spaces through contrastive learning - step {i}")
        elif i < 3 * quarter:
            descriptions.append(f"Similar concepts are being pulled together across spaces - step {i}")
        elif i < total_frames - 1:
            descriptions.append(f"Spaces nearing perfect alignment - step {i}")
        else:
            descriptions.append("Spaces aligned! Same concepts now occupy the same positions")
    
    return descriptions

def create_html_viewer(output_dir, total_frames):
    """Create an HTML file for interactive viewing of the visualization"""
    # Calculate number of digits needed for frame numbering
    num_digits = len(str(total_frames - 1))
    
    # Generate descriptions for each frame
    descriptions = generate_frame_descriptions(total_frames)
    
    # Build JavaScript array of descriptions
    descriptions_js = "[\n"
    for desc in descriptions:
        descriptions_js += f'        "{desc}",\n'
    descriptions_js += '        "Final view: Image and text representations now occupy the same semantic space"\n'
    descriptions_js += "      ]"
    
    # Create the HTML content - this is a large multi-line string
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Interactive Contrastive Learning Visualization</title>
  <style>
    :root {{
      --primary-color: #4a6fa5;
      --primary-hover: #38547e;
      --background-color: #f5f5f7;
      --text-color: #333;
      --border-color: #ddd;
      --shadow-color: rgba(0,0,0,0.1);
    }}
    
    body {{ 
      display: flex; 
      flex-direction: column;
      justify-content: center; 
      align-items: center; 
      min-height: 100vh;
      margin: 0;
      padding: 20px;
      background: var(--background-color);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: var(--text-color);
      transition: background-color 0.3s;
    }}
    
    .container {{
      display: flex;
      flex-direction: column;
      align-items: center;
      max-width: 95%;
      width: 100%;
    }}
    
    .title {{
      text-align: center;
      margin-bottom: 20px;
    }}
    
    .image-container {{
      position: relative;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 20px;
    }}
    
    img {{ 
      max-width: 100%;
      max-height: 70vh;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      box-shadow: 0 4px 12px var(--shadow-color);
      transition: transform 0.2s ease;
    }}
    
    .description {{
      text-align: center;
      margin: 15px 0;
      min-height: 50px;
      font-size: 18px;
      padding: 0 20px;
    }}
    
    .controls {{
      display: flex;
      gap: 12px;
      align-items: center;
      margin: 10px 0;
      flex-wrap: wrap;
      justify-content: center;
    }}
    
    button {{
      padding: 10px 20px;
      font-size: 16px;
      cursor: pointer;
      background-color: var(--primary-color);
      color: white;
      border: none;
      border-radius: 4px;
      transition: background-color 0.2s;
    }}
    
    button:hover {{
      background-color: var(--primary-hover);
    }}
    
    button:disabled {{
      background-color: #ccc;
      cursor: not-allowed;
    }}
    
    .counter {{
      font-size: 16px;
      font-weight: bold;
      min-width: 60px;
      text-align: center;
    }}
    
    .slider-container {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 15px;
    }}
    
    .slider {{
      width: 200px;
    }}
    
    .speed-label {{
      min-width: 120px;
      text-align: left;
    }}
    
    .toggle-container {{
      margin-top: 15px;
      display: flex;
      gap: 15px;
      flex-wrap: wrap;
      justify-content: center;
    }}
    
    .toggle-switch {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    
    .toggle-label {{
      font-size: 14px;
    }}
    
    .checkbox {{
      cursor: pointer;
    }}
    
    .progress-bar {{
      width: 100%;
      height: 6px;
      background-color: #ddd;
      border-radius: 3px;
      margin-top: 10px;
      overflow: hidden;
    }}
    
    .progress {{
      height: 100%;
      background-color: var(--primary-color);
      width: 0%;
      transition: width 0.3s;
    }}
    
    .dark-mode {{
      background-color: #2d2d2d;
      color: #f0f0f0;
    }}
    
    .dark-mode img {{
      border-color: #444;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    /* Keyboard navigation indicator */
    .key-hint {{
      position: absolute;
      bottom: 10px;
      right: 10px;
      background-color: rgba(0,0,0,0.6);
      color: white;
      padding: 5px 10px;
      border-radius: 4px;
      font-size: 12px;
      opacity: 0.7;
    }}
    
    /* Jump input container */
    .jump-container {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 15px;
    }}
    
    .jump-input {{
      width: 60px;
      padding: 5px;
      text-align: center;
      border: 1px solid var(--border-color);
      border-radius: 4px;
    }}
    
    .small-button {{
      padding: 5px 10px;
      font-size: 14px;
    }}
    
    @media (max-width: 768px) {{
      .controls {{
        flex-direction: column;
        gap: 10px;
      }}
      
      .slider-container {{
        flex-direction: column;
      }}
      
      .title {{
        font-size: 20px;
      }}
      
      .description {{
        font-size: 16px;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1 class="title">Contrastive Learning Space Alignment</h1>
    
    <div class="image-container">
      <img id="frame" src="step_0.png" alt="Contrastive Learning Visualization Frame" />
      <div class="key-hint">Use ← → keys to navigate</div>
    </div>
    
    <div id="description" class="description">
      Starting with misaligned spaces: similar concepts are in different positions
    </div>
    
    <div class="progress-bar">
      <div id="progress" class="progress"></div>
    </div>
    
    <div class="controls">
      <button id="firstButton" onclick="goToFirst()" title="Go to first frame">⏮</button>
      <button id="prevButton" onclick="prevFrame()">◀ Previous</button>
      <span id="counter" class="counter">1/{total_frames}</span>
      <button id="nextButton" onclick="nextFrame()">Next ▶</button>
      <button id="lastButton" onclick="goToLast()" title="Go to last frame">⏭</button>
      <button id="playButton" onclick="toggleAutoplay()">▶ Play</button>
    </div>
    
    <div class="jump-container">
      <span>Jump to frame:</span>
      <input type="number" id="jumpInput" class="jump-input" min="1" max="{total_frames}" value="1">
      <button class="small-button" onclick="jumpToFrame()">Go</button>
    </div>
    
    <div class="slider-container">
      <span class="speed-label">Animation Speed:</span>
      <input type="range" min="50" max="2000" value="200" class="slider" id="speedSlider">
      <span id="speedValue">0.2 sec</span>
    </div>
    
    <div class="toggle-container">
      <div class="toggle-switch">
        <input type="checkbox" id="loopToggle" class="checkbox" checked>
        <span class="toggle-label">Loop Animation</span>
      </div>
      
      <div class="toggle-switch">
        <input type="checkbox" id="reverseToggle" class="checkbox">
        <span class="toggle-label">Ping-Pong Effect</span>
      </div>
      
      <div class="toggle-switch">
        <input type="checkbox" id="darkModeToggle" class="checkbox">
        <span class="toggle-label">Dark Mode</span>
      </div>
      
      <div class="toggle-switch">
        <input type="checkbox" id="showCombinedToggle" class="checkbox" checked>
        <span class="toggle-label">Show Combined View</span>
      </div>
    </div>
  </div>

  <script>
    // Configuration
    const config = {{
      totalFrames: {total_frames - 1}, // Total number of step frames (not including combined view)
      imagePrefix: "step_", // Prefix of files
      imageExtension: ".png", // Extension of files
      fileDigits: {num_digits}, // Number of digits in file name
      initialDelay: 200, // Initial delay in milliseconds
      combinedImagePath: "combined_space.png", // Path to the combined view image
      descriptions: {descriptions_js},
      combinedDescription: "Final view: Image and text representations now occupy the same semantic space"
    }};
    
    // State
    let state = {{
      currentFrame: 0,
      direction: 1, // 1 = forward, -1 = backward
      autoplay: false,
      autoplayInterval: null,
      delay: config.initialDelay,
      showingCombinedView: false
    }};
    
    // DOM Elements
    const elements = {{
      frame: document.getElementById("frame"),
      counter: document.getElementById("counter"),
      description: document.getElementById("description"),
      playButton: document.getElementById("playButton"),
      prevButton: document.getElementById("prevButton"),
      nextButton: document.getElementById("nextButton"),
      firstButton: document.getElementById("firstButton"),
      lastButton: document.getElementById("lastButton"),
      speedSlider: document.getElementById("speedSlider"),
      speedValue: document.getElementById("speedValue"),
      loopToggle: document.getElementById("loopToggle"),
      reverseToggle: document.getElementById("reverseToggle"),
      darkModeToggle: document.getElementById("darkModeToggle"),
      showCombinedToggle: document.getElementById("showCombinedToggle"),
      progress: document.getElementById("progress"),
      jumpInput: document.getElementById("jumpInput")
    }};
    
    // Functions
    function updateImage() {{
      if (state.showingCombinedView) {{
        elements.frame.src = config.combinedImagePath;
        elements.counter.textContent = "Combined";
        elements.description.textContent = config.combinedDescription;
        elements.progress.style.width = "100%";
        elements.jumpInput.value = config.totalFrames + 1;
      }} else {{
        const frameNum = state.currentFrame.toString().padStart(config.fileDigits, "0");
        elements.frame.src = `${{config.imagePrefix}}${{frameNum}}${{config.imageExtension}}`;
        elements.counter.textContent = `${{state.currentFrame + 1}}/${{config.totalFrames + 1}}`;
        elements.description.textContent = config.descriptions[state.currentFrame];
        elements.jumpInput.value = state.currentFrame + 1;
        
        // Update progress bar
        const progressPercentage = (state.currentFrame / config.totalFrames) * 100;
        elements.progress.style.width = `${{progressPercentage}}%`;
      }}
      
      // Update button states
      updateButtonStates();
    }}
    
    function updateButtonStates() {{
      // Disable previous/first buttons at first frame (unless showing combined)
      elements.prevButton.disabled = state.currentFrame === 0 && !state.showingCombinedView;
      elements.firstButton.disabled = state.currentFrame === 0 && !state.showingCombinedView;
      
      // Disable next/last buttons at last frame (unless can go to combined)
      const atLastFrame = state.currentFrame === config.totalFrames;
      elements.nextButton.disabled = atLastFrame && state.showingCombinedView;
      elements.lastButton.disabled = atLastFrame && state.showingCombinedView;
    }}
    
    function nextFrame() {{
      if (state.showingCombinedView) {{
        // If showing combined view, go back to regular frames
        state.showingCombinedView = false;
        updateImage();
        return;
      }}
      
      if (state.currentFrame < config.totalFrames) {{
        state.currentFrame++;
        updateImage();
      }} else if (elements.showCombinedToggle.checked) {{
        // Show combined view after last frame if enabled
        state.showingCombinedView = true;
        updateImage();
      }} else if (elements.loopToggle.checked) {{
        // Loop back to first frame if looping is enabled
        state.currentFrame = 0;
        updateImage();
      }} else {{
        // Stop autoplay if we've reached the end
        if (state.autoplay) {{
          stopAutoplay();
        }}
      }}
    }}
    
    function prevFrame() {{
      if (state.showingCombinedView) {{
        // If showing combined view, go to last regular frame
        state.showingCombinedView = false;
        updateImage();
        return;
      }}
      
      if (state.currentFrame > 0) {{
        state.currentFrame--;
        updateImage();
      }}
    }}
    
    function goToFirst() {{
      state.showingCombinedView = false;
      state.currentFrame = 0;
      updateImage();
    }}
    
    function goToLast() {{
      if (elements.showCombinedToggle.checked) {{
        state.showingCombinedView = true;
      }} else {{
        state.showingCombinedView = false;
        state.currentFrame = config.totalFrames;
      }}
      updateImage();
    }}
    
    function jumpToFrame() {{
      const frameNumber = parseInt(elements.jumpInput.value);
      if (isNaN(frameNumber) || frameNumber < 1 || frameNumber > config.totalFrames + 1) {{
        // Invalid input
        elements.jumpInput.value = state.currentFrame + 1;
        return;
      }}
      
      if (frameNumber === config.totalFrames + 1) {{
        // Jump to combined view
        if (elements.showCombinedToggle.checked) {{
          state.showingCombinedView = true;
          updateImage();
        }} else {{
          // Combined view disabled, go to last regular frame
          state.showingCombinedView = false;
          state.currentFrame = config.totalFrames;
          updateImage();
        }}
      }} else {{
        // Jump to regular frame
        state.showingCombinedView = false;
        state.currentFrame = frameNumber - 1;
        updateImage();
      }}
    }}
    
    function advanceAnimation() {{
      // Handle ping-pong effect if enabled
      if (elements.reverseToggle.checked) {{
        // If at the end, reverse direction
        if (state.currentFrame === config.totalFrames && state.direction === 1) {{
          state.direction = -1;
        }} 
        // If at the beginning, reverse direction
        else if (state.currentFrame === 0 && state.direction === -1) {{
          state.direction = 1;
        }}
        
        // Move in current direction
        if (state.direction === 1) {{
          nextFrame();
        }} else {{
          prevFrame();
        }}
      }} else {{
        // Normal mode - always move forward
        nextFrame();
      }}
    }}
    
    function startAutoplay() {{
      state.autoplay = true;
      elements.playButton.textContent = "⏸ Pause";
      elements.playButton.title = "Pause animation";
      
      // Clear any existing interval
      if (state.autoplayInterval) {{
        clearInterval(state.autoplayInterval);
      }}
      
      // Start new interval
      state.autoplayInterval = setInterval(advanceAnimation, state.delay);
    }}
    
    function stopAutoplay() {{
      state.autoplay = false;
      elements.playButton.textContent = "▶ Play";
      elements.playButton.title = "Play animation";
      
      if (state.autoplayInterval) {{
        clearInterval(state.autoplayInterval);
        state.autoplayInterval = null;
      }}
    }}
    
    function toggleAutoplay() {{
      if (state.autoplay) {{
        stopAutoplay();
      }} else {{
        startAutoplay();
      }}
    }}
    
    function updateSpeedDisplay() {{
      const speedInSeconds = state.delay / 1000;
      elements.speedValue.textContent = `${{speedInSeconds.toFixed(1)}} sec`;
    }}
    
    function toggleDarkMode() {{
      document.body.classList.toggle('dark-mode');
    }}
    
    // Event Listeners
    elements.speedSlider.addEventListener("input", function() {{
      state.delay = parseInt(this.value);
      updateSpeedDisplay();
      
      // Update running interval if autoplay is active
      if (state.autoplay) {{
        clearInterval(state.autoplayInterval);
        state.autoplayInterval = setInterval(advanceAnimation, state.delay);
      }}
    }});
    
    elements.darkModeToggle.addEventListener("change", toggleDarkMode);
    
    elements.showCombinedToggle.addEventListener("change", function() {{
      updateButtonStates();
    }});
    
    elements.jumpInput.addEventListener("keydown", function(e) {{
      if (e.key === "Enter") {{
        jumpToFrame();
      }}
    }});
    
    // Keyboard navigation
    document.addEventListener("keydown", function(e) {{
      switch(e.key) {{
        case "ArrowLeft":
          prevFrame();
          break;
        case "ArrowRight":
          nextFrame();
          break;
        case "Home":
          goToFirst();
          break;
        case "End":
          goToLast();
          break;
        case " ":
          toggleAutoplay();
          e.preventDefault(); // Prevent scrolling with spacebar
          break;
      }}
    }});
    
    // Touch swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    
    elements.frame.addEventListener("touchstart", function(e) {{
      touchStartX = e.changedTouches[0].screenX;
    }});
    
    elements.frame.addEventListener("touchend", function(e) {{
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }});
    
    function handleSwipe() {{
      const threshold = 50; // Minimum distance for swipe
      if (touchEndX < touchStartX - threshold) {{
        // Swipe left - go forward
        nextFrame();
      }} else if (touchEndX > touchStartX + threshold) {{
        // Swipe right - go backward
        prevFrame();
      }}
    }}
    
    // Initialize
    function initialize() {{
      // Set initial speed value display
      updateSpeedDisplay();
      
      // Initialize first frame
      updateImage();
      
      // Set up hover events to pause/resume
      elements.frame.addEventListener("mouseenter", function() {{
        if (state.autoplay) {{
          clearInterval(state.autoplayInterval);
        }}
      }});
      
      elements.frame.addEventListener("mouseleave", function() {{
        if (state.autoplay) {{
          state.autoplayInterval = setInterval(advanceAnimation, state.delay);
        }}
      }});
    }}
    
    // Start the visualization
    initialize();
  </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open(f"{output_dir}/interactive_viewer.html", "w") as f:
        f.write(html_content)
    
    print(f"Interactive HTML viewer created: {output_dir}/interactive_viewer.html")
