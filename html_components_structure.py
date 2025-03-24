#!/usr/bin/env python3
"""
HTML Components Structure for Contrastive Learning Visualization
Author: Mikey Bee, 2025

This module provides the HTML structure and CSS styling for the interactive visualization viewer.
"""

def generate_html_header():
    """Generate the HTML header."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enhanced Contrastive Learning Visualization</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
"""

def generate_html_styles():
    """Generate the CSS styles."""
    return """  <style>
    :root {
      /* Light theme variables */
      --primary-color: #3f83f8;
      --primary-hover: #2c64dd;
      --secondary-color: #34d399;
      --background-color: #f9fafb;
      --secondary-bg: #ffffff;
      --text-color: #111827;
      --secondary-text: #4b5563;
      --border-color: #e5e7eb;
      --shadow-color: rgba(0,0,0,0.1);
      --code-bg: #f3f4f6;
    }
    
    /* Dark theme */
    .dark-mode {
      --primary-color: #4f83cc;
      --primary-hover: #3b6ebd;
      --secondary-color: #34d399;
      --background-color: #111827;
      --secondary-bg: #1f2937;
      --text-color: #f9fafb;
      --secondary-text: #d1d5db;
      --border-color: #374151;
      --shadow-color: rgba(0,0,0,0.5);
      --code-bg: #2d3748;
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      transition: background-color 0.3s, color 0.3s;
    }
    
    body { 
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      margin: 0;
      padding: 0;
      background: var(--background-color);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
        Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      color: var(--text-color);
    }
    
    header {
      background-color: var(--secondary-bg);
      padding: 1rem;
      box-shadow: 0 2px 8px var(--shadow-color);
      z-index: 10;
    }
    
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1400px;
      margin: 0 auto;
    }
    
    .title {
      font-size: 1.5rem;
      font-weight: bold;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .title i {
      color: var(--primary-color);
    }
    
    .right-nav {
      display: flex;
      gap: 1rem;
      align-items: center;
    }
    
    .theme-toggle {
      background: none;
      border: none;
      font-size: 1.2rem;
      color: var(--text-color);
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 50%;
    }
    
    .theme-toggle:hover {
      background-color: var(--border-color);
    }
    
    .info-button {
      background: var(--primary-color);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.25rem;
      cursor: pointer;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .info-button:hover {
      background-color: var(--primary-hover);
    }
    
    .main-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      max-width: 1400px;
      width: 100%;
      margin: 0 auto;
      padding: 1rem;
    }
    
    .visualization-container {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    
    .view-options {
      display: flex;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    
    .view-tab {
      padding: 0.5rem 1rem;
      background-color: var(--secondary-bg);
      border: 1px solid var(--border-color);
      border-radius: 0.25rem;
      cursor: pointer;
      font-weight: 500;
    }
    
    .view-tab.active {
      background-color: var(--primary-color);
      color: white;
      border-color: var(--primary-color);
    }
    
    .image-wrapper {
      position: relative;
      width: 100%;
      background-color: var(--secondary-bg);
      border: 1px solid var(--border-color);
      border-radius: 0.5rem;
      overflow: hidden;
      box-shadow: 0 4px 6px var(--shadow-color);
    }
    
    .single-view, .side-by-side-view, .comparison-view {
      display: none;
    }
    
    .active-view {
      display: block;
    }
    
    .side-by-side-view {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
    }
    
    .side-by-side-view .image-half {
      flex: 1;
      min-width: 300px;
    }
    
    .comparison-slider {
      position: relative;
      overflow: hidden;
      width: 100%;
    }
    
    .comparison-slider img {
      width: 100%;
      display: block;
    }
    
    .comparison-slider .img-overlay {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      overflow: hidden;
    }
    
    .comparison-slider .slider-handle {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 4px;
      background: var(--primary-color);
      cursor: ew-resize;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    
    .comparison-slider .slider-handle::after {
      content: '';
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--primary-color);
      border: 3px solid white;
      box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    
    .comparison-slider .slider-handle::before,
    .comparison-slider .slider-handle::after {
      content: '⟷';
      color: white;
      font-size: 20px;
      font-weight: bold;
      z-index: 3;
    }
    
    .image-container {
      display: flex;
      justify-content: center;
      position: relative;
    }
    
    img { 
      max-width: 100%;
      height: auto;
      border-radius: 0.25rem;
    }
    
    .key-hint {
      position: absolute;
      bottom: 10px;
      right: 10px;
      background-color: rgba(0,0,0,0.6);
      color: white;
      padding: 5px 10px;
      border-radius: 4px;
      font-size: 12px;
      opacity: 0.7;
    }
    
    .info-panel {
      background-color: var(--secondary-bg);
      padding: 1.5rem;
      border-radius: 0.5rem;
      margin-bottom: 1.5rem;
      border: 1px solid var(--border-color);
      box-shadow: 0 4px 6px var(--shadow-color);
    }
    
    .info-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    
    .info-title {
      font-size: 1.5rem;
      font-weight: bold;
      color: var(--primary-color);
    }
    
    .info-content {
      display: flex;
      flex-wrap: wrap;
      gap: 1.5rem;
    }
    
    .info-section {
      flex: 1;
      min-width: 250px;
    }
    
    .info-section h3 {
      margin-bottom: 0.5rem;
      border-bottom: 2px solid var(--primary-color);
      padding-bottom: 0.5rem;
      display: inline-block;
    }
    
    .info-section p {
      margin-bottom: 1rem;
      line-height: 1.6;
    }
    
    .tech-details {
      background-color: var(--code-bg);
      padding: 1rem;
      border-radius: 0.25rem;
      margin-top: 1rem;
      border-left: 4px solid var(--primary-color);
    }
    
    .tech-details h4 {
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .tech-details p {
      font-size: 0.9rem;
      color: var(--secondary-text);
    }
    
    .controls {
      background-color: var(--secondary-bg);
      padding: 1rem;
      border-radius: 0.5rem;
      margin-top: 1rem;
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      align-items: center;
      justify-content: space-between;
      border: 1px solid var(--border-color);
      box-shadow: 0 4px 6px var(--shadow-color);
    }
    
    .playback-controls {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }
    
    .counter {
      font-weight: bold;
      margin: 0 0.5rem;
    }
    
    button {
      background-color: var(--secondary-bg);
      color: var(--text-color);
      border: 1px solid var(--border-color);
      padding: 0.5rem;
      border-radius: 0.25rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
    }
    
    button:hover {
      background-color: var(--border-color);
    }
    
    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .play-button {
      background-color: var(--primary-color);
      color: white;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
    }
    
    .play-button:hover {
      background-color: var(--primary-hover);
    }
    
    .settings-controls {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      align-items: center;
    }
    
    .slider-container {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .slider-container label {
      font-size: 0.9rem;
      white-space: nowrap;
    }
    
    .slider {
      -webkit-appearance: none;
      width: 150px;
      height: 5px;
      border-radius: 5px;
      background: var(--border-color);
      outline: none;
    }
    
    .slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      background: var(--primary-color);
      cursor: pointer;
    }
    
    .checkbox-container {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .checkbox-container input[type="checkbox"] {
      width: 16px;
      height: 16px;
    }
    
    .progress-outer {
      width: 100%;
      height: 8px;
      background-color: var(--border-color);
      border-radius: 4px;
      margin-top: 1rem;
      overflow: hidden;
    }
    
    .progress-inner {
      height: 100%;
      background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
      width: 0%;
      transition: width 0.3s;
    }
    
    .attribution {
      margin-top: 2rem;
      text-align: center;
      font-size: 0.8rem;
      color: var(--secondary-text);
    }
    
    /* Info modal */
    .modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
      z-index: 100;
      align-items: center;
      justify-content: center;
    }
    
    .modal-content {
      background-color: var(--secondary-bg);
      width: 90%;
      max-width: 800px;
      max-height: 90vh;
      overflow-y: auto;
      border-radius: 0.5rem;
      padding: 2rem;
      position: relative;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    .close-modal {
      position: absolute;
      top: 1rem;
      right: 1rem;
      font-size: 1.5rem;
      cursor: pointer;
      color: var(--secondary-text);
    }
    
    .close-modal:hover {
      color: var(--text-color);
    }
    
    .modal-title {
      font-size: 1.8rem;
      margin-bottom: 1.5rem;
      color: var(--primary-color);
    }
    
    .modal-content h2 {
      font-size: 1.5rem;
      margin: 1.5rem 0 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--primary-color);
    }
    
    .modal-content p {
      margin-bottom: 1rem;
      line-height: 1.6;
    }
    
    .modal-content ul {
      margin-bottom: 1rem;
      padding-left: 2rem;
    }
    
    .modal-content li {
      margin-bottom: 0.5rem;
    }
    
    .code-block {
      background-color: var(--code-bg);
      padding: 1rem;
      border-radius: 0.25rem;
      margin: 1rem 0;
      overflow-x: auto;
      font-family: monospace;
    }
    
    .algorithm {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      padding-left: 1.5rem;
    }
    
    .algorithm-step {
      display: flex;
      gap: 0.5rem;
    }
    
    .step-number {
      color: var(--primary-color);
      font-weight: bold;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
      .title {
        font-size: 1.2rem;
      }
      
      .info-button span {
        display: none;
      }
      
      .view-options {
        flex-wrap: wrap;
      }
      
      .controls {
        flex-direction: column;
        align-items: stretch;
      }
      
      .playback-controls,
      .settings-controls {
        justify-content: center;
      }
      
      .slider {
        width: 100px;
      }
    }
  </style>
</head>"""

def generate_html_body(total_frames):
    """Generate the HTML body."""
    return f"""<body>
  <header>
    <div class="navbar">
      <div class="title">
        <i class="fas fa-brain"></i>
        <span>Contrastive Learning Visualization</span>
      </div>
      <div class="right-nav">
        <button class="theme-toggle" id="themeToggle">
          <i class="fas fa-moon"></i>
        </button>
        <button class="info-button" id="showInfo">
          <i class="fas fa-info-circle"></i>
          <span>Learn About Contrastive Learning</span>
        </button>
      </div>
    </div>
  </header>

  <div class="main-container">
    <div class="view-options">
      <div class="view-tab active" data-view="single">Single View</div>
      <div class="view-tab" data-view="side-by-side">Side by Side</div>
      <div class="view-tab" data-view="comparison">Comparison Slider</div>
    </div>
    
    <div class="visualization-container">
      <!-- Single View -->
      <div class="single-view active-view">
        <div class="image-wrapper">
          <div class="image-container">
            <img id="currentFrame" src="step_0.png" alt="Contrastive Learning Visualization Frame" />
            <div class="key-hint">Use ← → keys to navigate</div>
          </div>
        </div>
      </div>
      
      <!-- Side by Side View -->
      <div class="side-by-side-view">
        <div class="image-half">
          <div class="image-wrapper">
            <div class="image-container">
              <img id="beforeFrame" src="step_0.png" alt="Before" />
            </div>
          </div>
        </div>
        <div class="image-half">
          <div class="image-wrapper">
            <div class="image-container">
              <img id="afterFrame" src="combined_space.png" alt="After" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Comparison Slider View -->
      <div class="comparison-view">
        <div class="image-wrapper">
          <div class="comparison-slider" id="comparisonSlider">
            <img id="comparisonBase" src="combined_space.png" alt="After" />
            <div class="img-overlay" id="imgOverlay">
              <img id="comparisonOverlay" src="step_0.png" alt="Before" />
            </div>
            <div class="slider-handle" id="sliderHandle"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Info Panel -->
    <div class="info-panel">
      <div class="info-header">
        <div class="info-title" id="frameTitle">Initial Misaligned Spaces</div>
      </div>
      <div class="info-content">
        <div class="info-section">
          <h3>Explanation</h3>
          <p id="frameDescription">Starting with separate embedding spaces: similar concepts occupy different positions in image vs. text space.</p>
        </div>
        <div class="info-section">
          <div class="tech-details">
            <h4><i class="fas fa-code"></i> Technical Details</h4>
            <p id="technicalDetails">In contrastive learning, different modalities initially have their own separate feature spaces with different structures and orientations.</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Controls -->
    <div class="controls">
      <div class="playback-controls">
        <button id="firstButton" title="Go to first frame">
          <i class="fas fa-fast-backward"></i>
        </button>
        <button id="prevButton" title="Previous frame">
          <i class="fas fa-step-backward"></i>
        </button>
        <button id="playButton" class="play-button" title="Play/Pause">
          <i class="fas fa-play" id="playIcon"></i>
        </button>
        <button id="nextButton" title="Next frame">
          <i class="fas fa-step-forward"></i>
        </button>
        <button id="lastButton" title="Go to last frame">
          <i class="fas fa-fast-forward"></i>
        </button>
        <div class="counter">
          <span id="currentStep">1</span>/<span id="totalSteps">{total_frames}</span>
        </div>
      </div>
      
      <div class="settings-controls">
        <div class="slider-container">
          <label for="speedSlider">Speed:</label>
          <input type="range" id="speedSlider" class="slider" min="50" max="1000" value="300">
          <span id="speedValue">300ms</span>
        </div>
        
        <div class="checkbox-container">
          <input type="checkbox" id="loopToggle" checked>
          <label for="loopToggle">Loop</label>
        </div>
        
        <div class="checkbox-container">
          <input type="checkbox" id="pingpongToggle">
          <label for="pingpongToggle">Ping-pong</label>
        </div>
        
        <div class="slider-container">
          <label for="easingSlider">Easing:</label>
          <input type="range" id="easingSlider" class="slider" min="0" max="100" value="50">
        </div>
      </div>
      
      <div class="progress-outer">
        <div class="progress-inner" id="progressBar"></div>
      </div>
    </div>
    
    <div class="attribution">
      <p>© Visualization by Mikey Bee, 2025</p>
    </div>
  </div>
  
  <!-- Info Modal -->
  <div class="modal" id="infoModal">
    <div class="modal-content">
      <span class="close-modal" id="closeModal">&times;</span>
      <h1 class="modal-title">Understanding Contrastive Learning</h1>
      
      <p>Contrastive learning is a powerful paradigm in self-supervised learning that allows models to learn useful representations by contrasting positive pairs against negative pairs. It's particularly effective for aligning different data modalities like images and text.</p>
      
      <h2>Key Concepts</h2>
      <ul>
        <li><strong>Embedding Space:</strong> A high-dimensional space where data is represented as vectors</li>
        <li><strong>Modality:</strong> Different types of data (e.g., images, text, audio)</li>
        <li><strong>Positive Pairs:</strong> Different views or modalities of the same concept</li>
        <li><strong>Negative Pairs:</strong> Different concepts</li>
        <li><strong>Alignment:</strong> The process of bringing similar concepts from different modalities close together in embedding space</li>
      </ul>
      
      <h2>The Contrastive Learning Algorithm</h2>
      <div class="code-block">
        <div class="algorithm">
          <div class="algorithm-step">
            <span class="step-number">1.</span>
            <span>Sample a batch of data pairs (e.g., images and their corresponding text)</span>
          </div>
          <div class="algorithm-step">
            <span class="step-number">2.</span>
            <span>Compute embeddings for both modalities using separate encoders</span>
          </div>
          <div class="algorithm-step">
            <span class="step-number">3.</span>
            <span>Calculate similarity scores between all possible pairs</span>
          </div>
          <div class="algorithm-step">
            <span class="step-number">4.</span>
            <span>Maximize similarity for positive pairs (same concept)</span>
          </div>
          <div class="algorithm-step">
            <span class="step-number">5.</span>
            <span>Minimize similarity for negative pairs (different concepts)</span>
          </div>
          <div class="algorithm-step">
            <span class="step-number">6.</span>
            <span>Update the encoders to improve alignment</span>
          </div>
          <div class="algorithm-step">
            <span class="step-number">7.</span>
            <span>Repeat until convergence</span>
          </div>
        </div>
      </div>
      
      <h2>Applications</h2>
      <ul>
        <li><strong>Cross-modal Retrieval:</strong> Search for images using text queries and vice versa</li>
        <li><strong>Zero-shot Learning:</strong> Recognize new classes without explicit training examples</li>
        <li><strong>Transfer Learning:</strong> Apply knowledge from one modality to another</li>
        <li><strong>Multimodal Fusion:</strong> Combine information from multiple modalities</li>
      </ul>
      
      <h2>Famous Examples</h2>
      <ul>
        <li><strong>CLIP (Contrastive Language-Image Pretraining):</strong> Aligns image and text representations</li>
        <li><strong>SimCLR:</strong> Learns visual representations by contrasting different views of the same image</li>
        <li><strong>BYOL:</strong> A variant that doesn't require explicit negative pairs</li>
      </ul>
      
      <p>This visualization demonstrates how contrastive learning gradually aligns embedding spaces for different modalities, enabling powerful cross-modal capabilities.</p>
    </div>
  </div>"""
