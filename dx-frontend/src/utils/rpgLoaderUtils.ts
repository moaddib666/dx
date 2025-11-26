/**
 * RPG Loader utility functions for handling loading states in the application
 * Replaces the old loaderUtils.js with Vue component-based loading
 */

import { createApp, App } from 'vue'
import { createI18n } from 'vue-i18n'
import RPGLoader from '@/components/RPGLoader/RPGLoader.vue'

let loaderApp: App | null = null
let loaderContainer: HTMLElement | null = null

interface LoaderOptions {
  text?: string
  message?: string
  mode?: 'fullscreen' | 'overlay' | 'inline'
  fadeIn?: boolean
  fadeOut?: boolean
  fastLoad?: boolean
}

interface ErrorOptions {
  message?: string
  mode?: 'fullscreen' | 'overlay' | 'inline'
}

/**
 * Shows the RPG loader in the specified element
 * @param {string} elementId - The ID of the element to show the loader in
 * @param {LoaderOptions} options - Options for customizing the loader
 */
export function showRPGLoader(elementId = 'app', options: LoaderOptions = {}) {
  const element = document.getElementById(elementId)
  if (!element) {
    console.warn(`Element with ID '${elementId}' not found`)
    return
  }

  // Hide any existing loader first
  hideRPGLoader()

  // Create a container for the loader
  loaderContainer = document.createElement('div')
  loaderContainer.id = 'rpg-loader-container'
  loaderContainer.style.position = options.mode === 'fullscreen' ? 'fixed' : 'absolute'
  loaderContainer.style.top = '0'
  loaderContainer.style.left = '0'
  loaderContainer.style.width = '100%'
  loaderContainer.style.height = '100%'
  loaderContainer.style.zIndex = '9999'

  // Create i18n instance for the loader
  const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: {
      en: {
        common: {
          loading: 'Loading',
          preparingAdventure: 'Preparing your adventure...'
        }
      }
    }
  })

  // Create Vue app with RPGLoader
  loaderApp = createApp(RPGLoader, {
    loadingText: options.text || '',
    message: options.message || '',
    visible: true,
    mode: options.mode || 'fullscreen',
    fadeIn: options.fadeIn !== false,
    fadeOut: options.fadeOut !== false,
    fastLoad: options.fastLoad || false
  })

  loaderApp.use(i18n)

  // Mount the loader
  element.appendChild(loaderContainer)
  loaderApp.mount(loaderContainer)
}

/**
 * Hides the currently displayed RPG loader
 */
export function hideRPGLoader() {
  try {
    if (loaderApp && loaderContainer) {
      // Check if the app is still mounted before unmounting
      if (loaderContainer.parentNode) {
        loaderApp.unmount()
        loaderContainer.parentNode.removeChild(loaderContainer)
      }
      loaderApp = null
      loaderContainer = null
    }
  } catch (error) {
    console.warn('Error hiding RPG loader:', error)
    // Clean up references even if unmounting failed
    loaderApp = null
    loaderContainer = null
  }
}

/**
 * Shows an error message using the RPG loader
 * @param {string} elementId - The ID of the element to show the error in
 * @param {string} message - The error message to display
 * @param {ErrorOptions} options - Options for customizing the error display
 */
export function showRPGError(elementId = 'app', message = 'Failed to load application.', options: ErrorOptions = {}) {
  const element = document.getElementById(elementId)
  if (!element) {
    console.warn(`Element with ID '${elementId}' not found`)
    return
  }

  // Hide any existing loader first
  hideRPGLoader()

  // Create a container for the error
  loaderContainer = document.createElement('div')
  loaderContainer.id = 'rpg-error-container'
  loaderContainer.style.position = options.mode === 'fullscreen' ? 'fixed' : 'absolute'
  loaderContainer.style.top = '0'
  loaderContainer.style.left = '0'
  loaderContainer.style.width = '100%'
  loaderContainer.style.height = '100%'
  loaderContainer.style.zIndex = '9999'

  // Create i18n instance for the error
  const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: {
      en: {
        common: {
          loading: 'Loading',
          preparingAdventure: 'Preparing your adventure...'
        }
      }
    }
  })

  // Create Vue app with RPGLoader in error mode
  loaderApp = createApp(RPGLoader, {
    visible: true,
    mode: options.mode || 'fullscreen',
    showError: true,
    errorMessage: message,
    fadeIn: true,
    fadeOut: true
  })

  loaderApp.use(i18n)

  // Mount the error display
  element.appendChild(loaderContainer)
  loaderApp.mount(loaderContainer)
}

/**
 * Legacy compatibility functions to maintain backward compatibility
 */

/**
 * @deprecated Use showRPGLoader instead
 */
export function showLoader(elementId = 'app', options: any = {}) {
  console.warn('showLoader is deprecated. Use showRPGLoader instead.')
  showRPGLoader(elementId, {
    text: options.text,
    message: options.message,
    mode: 'fullscreen',
    fastLoad: true // Use fast load for legacy compatibility
  })
}

/**
 * @deprecated Use showRPGError instead
 */
export function showError(elementId = 'app', message = 'Failed to load application.') {
  console.warn('showError is deprecated. Use showRPGError instead.')
  showRPGError(elementId, message)
}

// Export default object for backward compatibility
export default {
  showRPGLoader,
  hideRPGLoader,
  showRPGError,
  showLoader,
  showError
}