/**
 * Utility functions for handling loading states in the application
 */

/**
 * Shows a loading spinner in the specified element
 * @param {string} elementId - The ID of the element to show the loader in
 * @param {Object} options - Options for customizing the loader
 * @param {string} options.text - The text to display (defaults to "Loading, please wait...")
 * @param {string} options.message - The message to display (defaults to "Preparing your adventure...")
 */
export function showLoader(elementId = 'app', options = {}) {
  const element = document.getElementById(elementId);
  if (!element) return;

  const text = options.text || 'Loading, please wait...';
  const message = options.message || 'Preparing your adventure...';

  // Create the loader HTML
  const loaderHTML = `
    <div class="global-loading-overlay">
      <div class="global-loading-spinner"></div>
      <div class="global-loading-text">${text}</div>
      <div class="global-loading-message">${message}</div>
    </div>
  `;

  // Create the loader CSS
  const loaderCSS = `
    .global-loading-overlay {
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
      backdrop-filter: blur(3px);
    }

    .global-loading-spinner {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      border: 3px solid transparent;
      border-top: 3px solid #ffd700;
      border-right: 3px solid #00ffff;
      border-bottom: 3px solid #ffd700;
      border-left: 3px solid #00ffff;
      animation: global-spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
      box-shadow:
        0 0 15px rgba(255, 215, 0, 0.5),
        0 0 30px rgba(0, 255, 255, 0.3),
        inset 0 0 15px rgba(255, 215, 0, 0.3);
      position: relative;
    }

    .global-loading-spinner::before {
      content: '';
      position: absolute;
      top: -10px;
      left: -10px;
      right: -10px;
      bottom: -10px;
      border-radius: 50%;
      border: 1px solid rgba(255, 215, 0, 0.3);
      animation: global-pulse 2s linear infinite;
    }

    @keyframes global-spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    @keyframes global-pulse {
      0% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.4);
      }
      70% {
        transform: scale(1);
        box-shadow: 0 0 0 10px rgba(255, 215, 0, 0);
      }
      100% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(255, 215, 0, 0);
      }
    }

    .global-loading-text {
      margin-top: 20px;
      font-size: 18px;
      font-weight: 600;
      color: #ffd700;
      text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
      letter-spacing: 1px;
      animation: global-fadeInOut 2s ease-in-out infinite;
    }

    .global-loading-message {
      margin-top: 10px;
      font-size: 14px;
      color: #00ffff;
      text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
      opacity: 0.8;
      letter-spacing: 0.5px;
    }

    @keyframes global-fadeInOut {
      0%, 100% { opacity: 0.7; }
      50% { opacity: 1; }
    }
  `;

  // Create a style element and append the CSS
  const styleElement = document.createElement('style');
  styleElement.id = 'global-loader-style';
  styleElement.textContent = loaderCSS;
  document.head.appendChild(styleElement);

  // Set the loader HTML
  element.innerHTML = loaderHTML;
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