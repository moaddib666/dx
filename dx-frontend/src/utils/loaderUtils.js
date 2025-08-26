/**
 * Utility functions for handling loading states in the application
 */

// Cache for preloaded assets
const assetCache = new Map();

// Track loader display timing to prevent flickering
let loaderStartTime = null;
const MINIMUM_DISPLAY_DURATION = 3000; // 3 seconds

/**
 * Preloads and caches fonts and images for blazingly fast loading
 */
function preloadAssets() {
  // Preload Cinzel font
  const fontLink = document.createElement('link');
  fontLink.rel = 'preload';
  fontLink.as = 'font';
  fontLink.type = 'font/woff2';
  fontLink.href = 'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&display=swap';
  fontLink.crossOrigin = 'anonymous';
  document.head.appendChild(fontLink);

  // Load Google Fonts CSS
  const fontCSS = document.createElement('link');
  fontCSS.rel = 'stylesheet';
  fontCSS.href = 'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&display=swap';
  document.head.appendChild(fontCSS);

  // Preload campfire image
  const campfireImg = new Image();
  campfireImg.src = 'src/assets/images/loader/campfire_mini.png';
  campfireImg.onload = () => {
    assetCache.set('campfire', campfireImg.src);
  };
}

// Initialize asset preloading
preloadAssets();

/**
 * Shows a campfire-themed loading screen in the specified element
 * @param {string} elementId - The ID of the element to show the loader in
 * @param {Object} options - Options for customizing the loader
 * @param {string} options.text - The text to display (defaults to "Loading")
 * @param {string} options.message - The message to display (defaults to "Preparing your adventure...")
 */
export function showLoader(elementId = 'app', options = {}) {
  const element = document.getElementById(elementId);
  if (!element) return;

  const text = options.text || 'Loading';
  const message = options.message || 'Preparing your adventure...';

  // Create the campfire loader HTML
  const loaderHTML = `
    <div class="global-loading-overlay">
      <div class="loading-container">
        <div class="campfire-container">
          <img src="src/assets/images/loader/campfire_mini.png"
               alt="Campfire"
               class="campfire-image">
          <div class="shadow-effect" id="shadowEffect"></div>
          <div class="fire-particle"></div>
          <div class="fire-particle"></div>
          <div class="fire-particle"></div>
          <div class="fire-particle"></div>
          <div class="fire-particle"></div>
        </div>
        <div class="loading-text">
          ${text}<span class="loading-dots"></span>
        </div>
        ${message ? `<div class="loading-message">${message}</div>` : ''}
      </div>
    </div>
  `;

  // Create the campfire loader CSS
  const loaderCSS = `
    .global-loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #000;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      overflow: hidden;
      font-family: Arial, sans-serif;
      opacity: 0;
      transition: opacity 0.5s ease-in-out;
    }

    .global-loading-overlay.fade-in {
      opacity: 1;
    }

    .global-loading-overlay.fade-out {
      opacity: 0;
    }

    .loading-container {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 10;
    }

    .campfire-container {
      position: relative;
      width: 200px;
      height: 200px;
      margin-bottom: 30px;
    }

    .campfire-image {
      width: 100%;
      height: 100%;
      object-fit: contain;
      position: relative;
      z-index: 2;
      filter: brightness(1.2) contrast(1.3) saturate(1.1);
      mix-blend-mode: screen;
      opacity: 0.95;
      user-select: none;
      pointer-events: none;
      -webkit-user-drag: none;
      -khtml-user-drag: none;
      -moz-user-drag: none;
      -o-user-drag: none;
      user-drag: none;
    }

    .shadow-effect {
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(0, 0, 0, 0.7) 20%,
        rgba(0, 0, 0, 0.9) 50%,
        rgba(0, 0, 0, 0.7) 80%,
        transparent 100%
      );
      z-index: 3;
      opacity: 0;
      pointer-events: none;
    }

    .shadow-effect.active {
      animation: shadowPass 3s ease-in-out;
    }

    @keyframes shadowPass {
      0% {
        left: -100%;
        opacity: 0;
      }
      10% {
        opacity: 1;
      }
      90% {
        opacity: 1;
      }
      100% {
        left: 100%;
        opacity: 0;
      }
    }

    .fire-particle {
      position: absolute;
      width: 3px;
      height: 3px;
      background: #00ffff;
      border-radius: 50%;
      pointer-events: none;
      animation: floatUp 3s linear infinite;
      opacity: 0;
    }

    .fire-particle:nth-child(3) { left: 45%; animation-delay: 0s; }
    .fire-particle:nth-child(4) { left: 55%; animation-delay: 0.5s; }
    .fire-particle:nth-child(5) { left: 50%; animation-delay: 1s; }
    .fire-particle:nth-child(6) { left: 40%; animation-delay: 1.5s; }
    .fire-particle:nth-child(7) { left: 60%; animation-delay: 2s; }

    @keyframes floatUp {
      0% {
        opacity: 1;
        transform: translateY(0px) scale(1);
        background: #00ffff;
      }
      50% {
        opacity: 0.7;
        background: #80ffff;
      }
      100% {
        opacity: 0;
        transform: translateY(-80px) scale(0.5);
        background: #ffff00;
      }
    }

    .loading-text {
      color: #fada95;
      font-size: 2rem;
      font-weight: 600;
      font-family: 'Cinzel', serif;
      text-align: center;
      margin-top: 20px;
      user-select: none;
      pointer-events: none;
      -webkit-touch-callout: none;
      -webkit-user-select: none;
      -khtml-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      text-shadow:
        2px 2px 4px rgba(0, 0, 0, 0.5),
        4px 4px 8px rgba(0, 0, 0, 0.3),
        0px 0px 10px rgba(250, 218, 149, 0.6),
        0px 0px 20px rgba(250, 218, 149, 0.3);
    }

    .loading-message {
      color: #00ffff;
      font-size: 1rem;
      text-align: center;
      margin-top: 10px;
      opacity: 0.8;
      text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
    }

    .loading-dots {
      display: inline-block;
      animation: dots 1.5s steps(4, end) infinite;
    }

    @keyframes dots {
      0%, 20% { content: ''; }
      40% { content: '.'; }
      60% { content: '..'; }
      80%, 100% { content: '...'; }
    }

    /* Responsive design */
    @media (max-width: 768px) {
      .campfire-container {
        width: 150px;
        height: 150px;
      }

      .loading-text {
        font-size: 1.5rem;
      }
    }
  `;

  // Create a style element and append the CSS
  const styleElement = document.createElement('style');
  styleElement.id = 'global-loader-style';
  styleElement.textContent = loaderCSS;
  document.head.appendChild(styleElement);

  // Set the loader HTML
  element.innerHTML = loaderHTML;

  // Record the start time for minimum display duration
  loaderStartTime = Date.now();

  // Trigger fade-in animation after a brief delay to ensure DOM is ready
  setTimeout(() => {
    const overlay = element.querySelector('.global-loading-overlay');
    if (overlay) {
      overlay.classList.add('fade-in');
    }
  }, 10);

  // Initialize dynamic effects
  initializeLoaderEffects();
}

/**
 * Initializes dynamic effects for the campfire loader
 */
function initializeLoaderEffects() {
  // Create additional dynamic particles
  function createParticle() {
    const container = document.querySelector('.campfire-container');
    if (!container) return;

    const particle = document.createElement('div');
    particle.className = 'fire-particle';

    // Random horizontal position
    particle.style.left = (Math.random() * 30 + 35) + '%';

    // Random vertical position - spawn from both top and bottom areas
    const spawnFromTop = Math.random() > 0.5;
    if (spawnFromTop) {
      particle.style.top = '10%';
      particle.style.bottom = 'auto';
    } else {
      particle.style.bottom = '20%';
      particle.style.top = 'auto';
    }

    // Random animation duration
    particle.style.animationDuration = (Math.random() * 2 + 2) + 's';

    container.appendChild(particle);

    // Remove particle after animation
    setTimeout(() => {
      if (particle.parentNode) {
        particle.parentNode.removeChild(particle);
      }
    }, 4000);
  }

  // Create particles periodically
  const particleInterval = setInterval(createParticle, 800);

  // Shadow effect function - triggers every 20-30 seconds
  function triggerShadowEffect() {
    const shadowElement = document.getElementById('shadowEffect');
    if (shadowElement) {
      shadowElement.classList.add('active');

      // Remove the active class after animation completes
      setTimeout(() => {
        shadowElement.classList.remove('active');
      }, 3000);
    }
  }

  // Start shadow effect with random timing between 20-30 seconds
  function scheduleShadowEffect() {
    const randomDelay = Math.random() * 10000 + 20000; // 20-30 seconds in milliseconds
    setTimeout(() => {
      triggerShadowEffect();
      scheduleShadowEffect(); // Schedule the next shadow effect
    }, randomDelay);
  }

  // Start the shadow effect scheduling
  scheduleShadowEffect();

  // Store intervals for cleanup
  if (!window.loaderIntervals) {
    window.loaderIntervals = [];
  }
  window.loaderIntervals.push(particleInterval);
}

/**
 * Hides the loader with a smooth fade-out transition and enforces minimum display duration
 * @param {string} elementId - The ID of the element containing the loader
 * @param {Function} callback - Optional callback to execute after hiding
 */
export function hideLoader(elementId = 'app', callback = null) {
  const element = document.getElementById(elementId);
  if (!element) return;

  const overlay = element.querySelector('.global-loading-overlay');
  if (!overlay) return;

  // Calculate elapsed time since loader was shown
  const elapsedTime = loaderStartTime ? Date.now() - loaderStartTime : MINIMUM_DISPLAY_DURATION;
  const remainingTime = Math.max(0, MINIMUM_DISPLAY_DURATION - elapsedTime);

  // Function to actually hide the loader
  function performHide() {
    // Apply fade-out class
    overlay.classList.remove('fade-in');
    overlay.classList.add('fade-out');

    // Wait for transition to complete before removing
    setTimeout(() => {
      // Clean up intervals
      if (window.loaderIntervals) {
        window.loaderIntervals.forEach(interval => clearInterval(interval));
        window.loaderIntervals = [];
      }

      // Remove the loader style
      const loaderStyle = document.getElementById('global-loader-style');
      if (loaderStyle) {
        loaderStyle.remove();
      }

      // Clear the element content
      element.innerHTML = '';

      // Reset loader start time
      loaderStartTime = null;

      // Execute callback if provided
      if (callback && typeof callback === 'function') {
        callback();
      }
    }, 500); // Match the CSS transition duration
  }

  // If minimum time hasn't passed, wait for the remaining time
  if (remainingTime > 0) {
    setTimeout(performHide, remainingTime);
  } else {
    performHide();
  }
}

/**
 * Shows an error message in the specified element
 * @param {string} elementId - The ID of the element to show the error in
 * @param {string} message - The error message to display
 */
export function showError(elementId = 'app', message = 'Failed to load application.') {
  const element = document.getElementById(elementId);
  if (!element) return;

  // Remove the loader style if it exists
  const loaderStyle = document.getElementById('global-loader-style');
  if (loaderStyle) {
    loaderStyle.remove();
  }

  // Create the error HTML
  const errorHTML = `
    <div class="global-error-overlay">
      <div class="global-error-icon">⚠️</div>
      <div class="global-error-text">Error</div>
      <div class="global-error-message">${message}</div>
    </div>
  `;

  // Create the error CSS
  const errorCSS = `
    .global-error-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(42, 43, 43, 0.7);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }

    .global-error-icon {
      font-size: 48px;
      margin-bottom: 20px;
    }

    .global-error-text {
      font-size: 24px;
      color: #ff4d4d;
      margin-bottom: 15px;
      font-weight: 600;
    }

    .global-error-message {
      font-size: 16px;
      color: #ffffff;
      margin-bottom: 25px;
      line-height: 1.5;
      max-width: 80%;
      text-align: center;
    }
  `;

  // Create a style element and append the CSS
  const styleElement = document.createElement('style');
  styleElement.id = 'global-error-style';
  styleElement.textContent = errorCSS;
  document.head.appendChild(styleElement);

  // Set the error HTML
  element.innerHTML = errorHTML;
}