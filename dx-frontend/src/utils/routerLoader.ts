/**
 * Router loading interceptor for page transitions using RPGLoader
 * Provides smooth fade effects during navigation
 */

import { Router } from 'vue-router'
import { showRPGLoader, hideRPGLoader } from './rpgLoaderUtils'

let isLoading = false
let loadingTimeout: number | null = null

interface RouterLoaderOptions {
  minLoadingTime?: number // Minimum time to show loader (prevents flashing)
  maxLoadingTime?: number // Maximum time before forcing hide
  excludeRoutes?: string[] // Routes to exclude from loading
  loadingText?: string
  message?: string
}

const defaultOptions: RouterLoaderOptions = {
  minLoadingTime: 300,
  maxLoadingTime: 10000,
  excludeRoutes: [],
  loadingText: 'Loading page...',
  message: 'Preparing your adventure...'
}

/**
 * Sets up router loading interceptor
 * @param router - Vue Router instance
 * @param options - Configuration options
 */
export function setupRouterLoader(router: Router, options: RouterLoaderOptions = {}) {
  const config = { ...defaultOptions, ...options }

  // Before each route navigation
  router.beforeEach((to, from, next) => {
    // Skip loading for excluded routes
    if (config.excludeRoutes?.includes(to.name as string)) {
      next()
      return
    }

    // Skip loading if already on the same route
    if (to.path === from.path) {
      next()
      return
    }

    // Show loader
    showPageLoader(config)
    next()
  })

  // After each route navigation
  router.afterEach((to, from) => {
    // Hide loader after minimum time
    if (loadingTimeout) {
      clearTimeout(loadingTimeout)
    }

    loadingTimeout = window.setTimeout(() => {
      hidePageLoader()
    }, config.minLoadingTime)

    // Force hide after maximum time
    setTimeout(() => {
      if (isLoading) {
        console.warn('Router loader: Force hiding after max time')
        hidePageLoader()
      }
    }, config.maxLoadingTime)
  })

  // Handle navigation errors
  router.onError((error) => {
    console.error('Router navigation error:', error)
    hidePageLoader()
  })
}

/**
 * Shows the page loader
 */
function showPageLoader(config: RouterLoaderOptions) {
  if (isLoading) return

  isLoading = true
  showRPGLoader('app', {
    text: config.loadingText,
    message: config.message,
    mode: 'fullscreen',
    fadeIn: true,
    fadeOut: true,
    fastLoad: false // Use full animation for page transitions
  })
}

/**
 * Hides the page loader
 */
function hidePageLoader() {
  if (!isLoading) return

  isLoading = false
  if (loadingTimeout) {
    clearTimeout(loadingTimeout)
    loadingTimeout = null
  }
  hideRPGLoader()
}

/**
 * Manually show page loader (for programmatic use)
 */
export function showManualPageLoader(options: Partial<RouterLoaderOptions> = {}) {
  const config = { ...defaultOptions, ...options }
  showPageLoader(config)
}

/**
 * Manually hide page loader (for programmatic use)
 */
export function hideManualPageLoader() {
  hidePageLoader()
}

/**
 * Check if page loader is currently active
 */
export function isPageLoaderActive(): boolean {
  return isLoading
}

// Export default setup function
export default setupRouterLoader