#!/usr/bin/env python3
"""
HTML Components Scripts for Contrastive Learning Visualization
Author: Mikey Bee, 2025

This module provides the JavaScript scripts for the interactive visualization viewer.
"""

def generate_html_scripts(total_frames, num_digits, descriptions_json):
    """Generate the JavaScript for the HTML."""
    return f"""  <script>
    // Configuration
    const config = {{
      totalFrames: {total_frames},
      imagePrefix: "step_",
      imageExtension: ".png",
      fileDigits: {num_digits},
      combinedImagePath: "combined_space.png",
      descriptions: {descriptions_json}
    }};
    
    // State
    const state = {{
      currentFrame: 0,
      isPlaying: false,
      playInterval: null,
      playSpeed: 300,
      isLooping: true,
      isPingPong: false,
      direction: 1,
      easing: 0.5,
      comparePosition: 50
    }};
    
    // DOM Elements
    const elements = {{
      // Images
      currentFrame: document.getElementById("currentFrame"),
      beforeFrame: document.getElementById("beforeFrame"),
      afterFrame: document.getElementById("afterFrame"),
      comparisonBase: document.getElementById("comparisonBase"),
      comparisonOverlay: document.getElementById("comparisonOverlay"),
      imgOverlay: document.getElementById("imgOverlay"),
      sliderHandle: document.getElementById("sliderHandle"),
      comparisonSlider: document.getElementById("comparisonSlider"),
      
      // View tabs
      viewTabs: document.querySelectorAll(".view-tab"),
      singleView: document.querySelector(".single-view"),
      sideBySideView: document.querySelector(".side-by-side-view"),
      comparisonView: document.querySelector(".comparison-view"),
      
      // Controls
      playButton: document.getElementById("playButton"),
      playIcon: document.getElementById("playIcon"),
      prevButton: document.getElementById("prevButton"),
      nextButton: document.getElementById("nextButton"),
      firstButton: document.getElementById("firstButton"),
      lastButton: document.getElementById("lastButton"),
      currentStep: document.getElementById("currentStep"),
      totalSteps: document.getElementById("totalSteps"),
      progressBar: document.getElementById("progressBar"),
      
      // Settings
      speedSlider: document.getElementById("speedSlider"),
      speedValue: document.getElementById("speedValue"),
      loopToggle: document.getElementById("loopToggle"),
      pingpongToggle: document.getElementById("pingpongToggle"),
      easingSlider: document.getElementById("easingSlider"),
      
      // Info panel
      frameTitle: document.getElementById("frameTitle"),
      frameDescription: document.getElementById("frameDescription"),
      technicalDetails: document.getElementById("technicalDetails"),
      
      // Theme
      themeToggle: document.getElementById("themeToggle"),
      
      // Modal
      infoButton: document.getElementById("showInfo"),
      infoModal: document.getElementById("infoModal"),
      closeModal: document.getElementById("closeModal")
    }};
    
    // Initialize the application
    function initialize() {{
      // Set up view tab listeners
      elements.viewTabs.forEach(tab => {{
        tab.addEventListener("click", () => {{
          // Remove active class from all tabs
          elements.viewTabs.forEach(t => t.classList.remove("active"));
          // Add active class to clicked tab
          tab.classList.add("active");
          
          // Hide all views
          elements.singleView.classList.remove("active-view");
          elements.sideBySideView.classList.remove("active-view");
          elements.comparisonView.classList.remove("active-view");
          
          // Show selected view
          const viewType = tab.dataset.view;
          if (viewType === "single") {{
            elements.singleView.classList.add("active-view");
          }} else if (viewType === "side-by-side") {{
            elements.sideBySideView.classList.add("active-view");
          }} else if (viewType === "comparison") {{
            elements.comparisonView.classList.add("active-view");
            setupComparisonSlider();
          }}
        }});
      }});
      
      // Set up control buttons
      elements.playButton.addEventListener("click", togglePlay);
      elements.prevButton.addEventListener("click", prevFrame);
      elements.nextButton.addEventListener("click", nextFrame);
      elements.firstButton.addEventListener("click", goToFirst);
      elements.lastButton.addEventListener("click", goToLast);
      
      // Set up settings controls
      elements.speedSlider.addEventListener("input", updateSpeed);
      elements.loopToggle.addEventListener("change", () => {{ state.isLooping = elements.loopToggle.checked; }});
      elements.pingpongToggle.addEventListener("change", () => {{ state.isPingPong = elements.pingpongToggle.checked; }});
      elements.easingSlider.addEventListener("input", () => {{ state.easing = elements.easingSlider.value / 100; }});
      
      // Set up theme toggle
      elements.themeToggle.addEventListener("click", toggleTheme);
      
      // Set up modal controls
      elements.infoButton.addEventListener("click", () => {{
        elements.infoModal.style.display = "flex";
      }});
      
      elements.closeModal.addEventListener("click", () => {{
        elements.infoModal.style.display = "none";
      }});
      
      // Close modal when clicking outside content
      elements.infoModal.addEventListener("click", (e) => {{
        if (e.target === elements.infoModal) {{
          elements.infoModal.style.display = "none";
        }}
      }});
      
      // Set up keyboard navigation
      document.addEventListener("keydown", handleKeyPress);
      
      // Set initial state
      elements.totalSteps.textContent = config.totalFrames;
      updateFrame();
      
      // Setup comparison slider
      setupComparisonSlider();
    }}
    
    // Toggle play/pause
    function togglePlay() {{
      state.isPlaying = !state.isPlaying;
      
      if (state.isPlaying) {{
        elements.playIcon.className = "fas fa-pause";
        state.playInterval = setInterval(advanceFrame, state.playSpeed);
      }} else {{
        elements.playIcon.className = "fas fa-play";
        clearInterval(state.playInterval);
      }}
    }}
    
    // Navigate to previous frame
    function prevFrame() {{
      state.isPlaying = false;
      clearInterval(state.playInterval);
      elements.playIcon.className = "fas fa-play";
      
      if (state.currentFrame > 0) {{
        state.currentFrame--;
        updateFrame();
      }}
    }}
    
    // Navigate to next frame
    function nextFrame() {{
      state.isPlaying = false;
      clearInterval(state.playInterval);
      elements.playIcon.className = "fas fa-play";
      
      if (state.currentFrame < config.totalFrames) {{
        state.currentFrame++;
        updateFrame();
      }}
    }}
    
    // Go to first frame
    function goToFirst() {{
      state.isPlaying = false;
      clearInterval(state.playInterval);
      elements.playIcon.className = "fas fa-play";
      
      state.currentFrame = 0;
      updateFrame();
    }}
    
    // Go to last frame
    function goToLast() {{
      state.isPlaying = false;
      clearInterval(state.playInterval);
      elements.playIcon.className = "fas fa-play";
      
      state.currentFrame = config.totalFrames;
      updateFrame();
    }}
    
    // Advance frame during playback
    function advanceFrame() {{
      if (state.isPingPong) {{
        // Handle ping-pong mode
        if (state.currentFrame >= config.totalFrames && state.direction === 1) {{
          state.direction = -1;
        }} else if (state.currentFrame <= 0 && state.direction === -1) {{
          state.direction = 1;
        }}
        
        state.currentFrame += state.direction;
      }} else {{
        // Normal mode - always forward
        state.currentFrame++;
        
        // Handle looping
        if (state.currentFrame > config.totalFrames) {{
          if (state.isLooping) {{
            state.currentFrame = 0;
          }} else {{
            state.currentFrame = config.totalFrames;
            togglePlay(); // Stop at the end
          }}
        }}
      }}
      
      updateFrame();
    }}
    
    // Update frame display
    function updateFrame() {{
      // Format frame number with leading zeros
      const frameNum = state.currentFrame.toString().padStart(config.fileDigits, "0");
      
      // Handle the case where we're showing the combined view (last frame + 1)
      if (state.currentFrame === config.totalFrames) {{
        elements.currentFrame.src = config.combinedImagePath;
        elements.comparisonBase.src = config.combinedImagePath;
      }} else {{
        elements.currentFrame.src = `${{config.imagePrefix}}${{frameNum}}${{config.imageExtension}}`;
        elements.comparisonBase.src = `${{config.imagePrefix}}${{frameNum}}${{config.imageExtension}}`;
      }}
      
      // Update side-by-side view
      elements.beforeFrame.src = `${{config.imagePrefix}}0${{config.imageExtension}}`;
      elements.afterFrame.src = config.combinedImagePath;
      
      // Update comparison view
      elements.comparisonOverlay.src = config.combinedImagePath;
      
      // Update counter
      elements.currentStep.textContent = state.currentFrame + 1;
      
      // Update progress bar
      const progress = (state.currentFrame / config.totalFrames) * 100;
      elements.progressBar.style.width = `${{progress}}%`;
      
      // Update info panel
      const frameInfo = config.descriptions[state.currentFrame];
      elements.frameTitle.textContent = frameInfo.title;
      elements.frameDescription.textContent = frameInfo.text;
      elements.technicalDetails.textContent = frameInfo.technical;
      
      // Update button states
      elements.prevButton.disabled = state.currentFrame === 0;
      elements.firstButton.disabled = state.currentFrame === 0;
      elements.nextButton.disabled = state.currentFrame === config.totalFrames;
      elements.lastButton.disabled = state.currentFrame === config.totalFrames;
    }}
    
    // Update playback speed
    function updateSpeed() {{
      state.playSpeed = parseInt(elements.speedSlider.value);
      elements.speedValue.textContent = `${{state.playSpeed}}ms`;
      
      // Restart interval with new speed if playing
      if (state.isPlaying) {{
        clearInterval(state.playInterval);
        state.playInterval = setInterval(advanceFrame, state.playSpeed);
      }}
    }}
    
    // Toggle theme
    function toggleTheme() {{
      document.body.classList.toggle("dark-mode");
      
      // Update icon
      if (document.body.classList.contains("dark-mode")) {{
        elements.themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
      }} else {{
        elements.themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
      }}
    }}
    
    // Handle keyboard navigation
    function handleKeyPress(e) {{
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
          togglePlay();
          e.preventDefault(); // Prevent scrolling with spacebar
          break;
      }}
    }}
    
    // Set up comparison slider
    function setupComparisonSlider() {{
      const slider = elements.comparisonSlider;
      const handle = elements.sliderHandle;
      const overlay = elements.imgOverlay;
      let isDragging = false;
      
      // Initial position
      updateComparisonPosition(state.comparePosition);
      
      // Functions to handle slider movement
      function updateComparisonPosition(position) {{
        state.comparePosition = position;
        const pct = position + "%";
        overlay.style.width = pct;
        handle.style.left = pct;
      }}
      
      function handleSliderStart(e) {{
        isDragging = true;
        slider.classList.add("active");
        handleSliderMove(e);
      }}
      
      function handleSliderMove(e) {{
        if (!isDragging) return;
        
        let position;
        if (e.type.includes("touch")) {{
          position = (e.touches[0].clientX - slider.getBoundingClientRect().left) / slider.offsetWidth * 100;
        }} else {{
          position = (e.clientX - slider.getBoundingClientRect().left) / slider.offsetWidth * 100;
        }}
        
        // Constrain position to 0-100%
        position = Math.max(0, Math.min(100, position));
        updateComparisonPosition(position);
      }}
      
      function handleSliderEnd() {{
        isDragging = false;
        slider.classList.remove("active");
      }}
      
      // Mouse events
      handle.addEventListener("mousedown", handleSliderStart);
      document.addEventListener("mousemove", handleSliderMove);
      document.addEventListener("mouseup", handleSliderEnd);
      
      // Touch events for mobile
      handle.addEventListener("touchstart", handleSliderStart);
      document.addEventListener("touchmove", handleSliderMove);
      document.addEventListener("touchend", handleSliderEnd);
      
      // Click anywhere on slider to move handle
      slider.addEventListener("click", (e) => {{
        if (e.target !== handle) {{
          const position = (e.clientX - slider.getBoundingClientRect().left) / slider.offsetWidth * 100;
          updateComparisonPosition(position);
        }}
      }});
    }}
    
    // Start the application
    initialize();
  </script>
</body>
</html>"""
