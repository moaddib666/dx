<template>
  <div class="test-page-container">
    <AuthBackground @toggle-zoom="toggleZoom" />
    <ZoomModal
      :is-visible="isZoomed"
      :image-url="currentZoomedImage"
      @close="closeZoom"
    />

    <main class="test-content">
      <TitleComponent>Google Auth Test Page</TitleComponent>

      <div class="test-section">
        <h2>Environment Variables Status</h2>
        <div class="env-status">
          <div class="env-item">
            <strong>VITE_GOOGLE_AUTH_CLIENT_ID:</strong>
            <span :class="{ 'status-ok': googleClientId, 'status-error': !googleClientId }">
              {{ googleClientId ? 'Set' : 'Not Set' }}
            </span>
          </div>
          <div class="env-item">
            <strong>VITE_GOOGLE_AUTH_HIDDEN_BY_COOKIE:</strong>
            <span :class="{ 'status-ok': googleAuthCookie, 'status-error': !googleAuthCookie }">
              {{ googleAuthCookie || 'Not Set' }}
            </span>
          </div>
          <div class="env-item">
            <strong>Google Auth Enabled:</strong>
            <span :class="{ 'status-ok': isGoogleAuthEnabled, 'status-error': !isGoogleAuthEnabled }">
              {{ isGoogleAuthEnabled ? 'Yes' : 'No' }}
            </span>
          </div>
        </div>
      </div>

      <div class="test-section">
        <h2>Google Auth Components Test</h2>

        <div class="auth-test-container">
          <div class="auth-mode">
            <h3>Login Mode</h3>
            <div class="test-form">
              <GoogleAuth
                mode="login"
                @success="handleGoogleAuthSuccess"
                @error="handleGoogleAuthError"
              />
            </div>
          </div>

          <div class="auth-mode">
            <h3>Register Mode</h3>
            <div class="test-form">
              <GoogleAuth
                mode="register"
                @success="handleGoogleAuthSuccess"
                @error="handleGoogleAuthError"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="test-section" v-if="testResults.length > 0">
        <h2>Test Results</h2>
        <div class="test-results">
          <div
            v-for="(result, index) in testResults"
            :key="index"
            :class="['test-result', result.type]"
          >
            <strong>{{ result.timestamp }}:</strong> {{ result.message }}
          </div>
        </div>
      </div>

      <div class="test-section">
        <h2>Cookie Control</h2>
        <div class="cookie-controls">
          <button @click="enableGoogleAuth" class="btn btn-success">
            Enable Google Auth (Set Cookie)
          </button>
          <button @click="disableGoogleAuth" class="btn btn-warning">
            Disable Google Auth (Remove Cookie)
          </button>
          <button @click="checkCookieStatus" class="btn btn-info">
            Check Cookie Status
          </button>
        </div>
      </div>

      <div class="navigation">
        <router-link :to="{ name: 'Login' }" class="nav-link">Go to Login</router-link>
        <router-link :to="{ name: 'Register' }" class="nav-link">Go to Register</router-link>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AuthBackground from "@/components/Auth/AuthBackground.vue"
import ZoomModal from "@/components/WhatIsIt/ZoomModal.vue"
import TitleComponent from "@/components/TitleComponent.vue"
import GoogleAuth from "@/components/Auth/GoogleAuth.vue"

export default {
  name: 'GoogleAuthTest',
  components: {
    AuthBackground,
    ZoomModal,
    TitleComponent,
    GoogleAuth
  },
  setup() {
    const { t } = useI18n()

    const isZoomed = ref(false)
    const currentZoomedImage = ref('')
    const scrollPosition = ref(0)
    const testResults = ref([])

    const googleClientId = import.meta.env.VITE_GOOGLE_AUTH_CLIENT_ID
    const googleAuthCookie = import.meta.env.VITE_GOOGLE_AUTH_HIDDEN_BY_COOKIE

    const isGoogleAuthEnabled = computed(() => {
      if (!googleClientId) return false

      if (googleAuthCookie) {
        const cookies = document.cookie.split(';')
        const authCookie = cookies.find(cookie =>
          cookie.trim().startsWith(`${googleAuthCookie}=`)
        )

        if (authCookie) {
          const cookieValue = authCookie.split('=')[1]
          return cookieValue === 'true' || cookieValue === '1'
        }

        return true
      }

      return true
    })

    const addTestResult = (message, type = 'info') => {
      testResults.value.unshift({
        timestamp: new Date().toLocaleTimeString(),
        message,
        type
      })

      // Keep only last 10 results
      if (testResults.value.length > 10) {
        testResults.value = testResults.value.slice(0, 10)
      }
    }

    const handleGoogleAuthSuccess = (data) => {
      addTestResult(`Google Auth Success (${data.mode}): User authenticated successfully`, 'success')
      console.log('Google auth success:', data)
    }

    const handleGoogleAuthError = (data) => {
      addTestResult(`Google Auth Error (${data.mode}): ${data.error}`, 'error')
      console.error('Google auth error:', data)
    }

    const enableGoogleAuth = () => {
      if (googleAuthCookie) {
        document.cookie = `${googleAuthCookie}=true; path=/; max-age=31536000`
        addTestResult('Google Auth enabled via cookie', 'success')
        // Force reactivity update
        setTimeout(() => {
          window.location.reload()
        }, 1000)
      } else {
        addTestResult('No cookie name configured for Google Auth control', 'warning')
      }
    }

    const disableGoogleAuth = () => {
      if (googleAuthCookie) {
        document.cookie = `${googleAuthCookie}=false; path=/; max-age=31536000`
        addTestResult('Google Auth disabled via cookie', 'warning')
        // Force reactivity update
        setTimeout(() => {
          window.location.reload()
        }, 1000)
      } else {
        addTestResult('No cookie name configured for Google Auth control', 'warning')
      }
    }

    const checkCookieStatus = () => {
      if (googleAuthCookie) {
        const cookies = document.cookie.split(';')
        const authCookie = cookies.find(cookie =>
          cookie.trim().startsWith(`${googleAuthCookie}=`)
        )

        if (authCookie) {
          const cookieValue = authCookie.split('=')[1]
          addTestResult(`Cookie ${googleAuthCookie} = ${cookieValue}`, 'info')
        } else {
          addTestResult(`Cookie ${googleAuthCookie} not found`, 'info')
        }
      } else {
        addTestResult('No cookie name configured', 'warning')
      }
    }

    const toggleZoom = (event) => {
      const imgElement = event.target.tagName === 'IMG' ? event.target : event.target.querySelector('img')

      if (imgElement) {
        currentZoomedImage.value = imgElement.src
        isZoomed.value = true
        scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop
        document.body.style.overflow = 'hidden'
      } else if (event.target.classList.contains('auth-background')) {
        const style = getComputedStyle(event.target)
        const bgImage = style.backgroundImage
        const url = bgImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '')
        currentZoomedImage.value = url
        isZoomed.value = true
        scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop
        document.body.style.overflow = 'hidden'
      }
    }

    const closeZoom = () => {
      isZoomed.value = false
      document.body.style.overflow = ''
      window.scrollTo(0, scrollPosition.value)
    }

    onMounted(() => {
      addTestResult('Google Auth Test Page loaded', 'info')
      addTestResult(`Client ID: ${googleClientId ? 'Configured' : 'Not configured'}`, googleClientId ? 'success' : 'error')
      addTestResult(`Cookie Control: ${googleAuthCookie || 'Not configured'}`, googleAuthCookie ? 'success' : 'warning')
    })

    return {
      isZoomed,
      currentZoomedImage,
      testResults,
      googleClientId,
      googleAuthCookie,
      isGoogleAuthEnabled,
      handleGoogleAuthSuccess,
      handleGoogleAuthError,
      enableGoogleAuth,
      disableGoogleAuth,
      checkCookieStatus,
      toggleZoom,
      closeZoom,
      t
    }
  }
}
</script>

<style scoped>
:root {
  --cyber-yellow: #ffd700;
  --cyber-cyan: #00ffff;
  --light-steel-blue: #b0c4de;
  --dark-overlay: rgba(0, 0, 0, 0.7);
}

.test-page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.test-content {
  padding: 2rem;
  color: white;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  min-height: 100vh;
}

.test-section {
  background: rgba(28, 28, 28, 0.8);
  border: 2px solid #444;
  border-radius: 8px;
  padding: 2rem;
  margin: 2rem 0;
  backdrop-filter: blur(5px);
}

.test-section h2 {
  color: var(--cyber-cyan);
  margin-bottom: 1rem;
  border-bottom: 2px solid #444;
  padding-bottom: 0.5rem;
}

.test-section h3 {
  color: var(--cyber-yellow);
  margin-bottom: 1rem;
}

.env-status {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.env-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: rgba(41, 41, 41, 0.8);
  border-radius: 4px;
}

.status-ok {
  color: #4caf50;
  font-weight: bold;
}

.status-error {
  color: #f44336;
  font-weight: bold;
}

.auth-test-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.auth-mode {
  background: rgba(41, 41, 41, 0.6);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #555;
}

.test-form {
  background: rgba(28, 28, 28, 0.8);
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #444;
}

.test-results {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.test-result {
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 4px solid;
}

.test-result.success {
  background: rgba(76, 175, 80, 0.1);
  border-left-color: #4caf50;
}

.test-result.error {
  background: rgba(244, 67, 54, 0.1);
  border-left-color: #f44336;
}

.test-result.warning {
  background: rgba(255, 193, 7, 0.1);
  border-left-color: #ffc107;
}

.test-result.info {
  background: rgba(33, 150, 243, 0.1);
  border-left-color: #2196f3;
}

.cookie-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btn-success {
  background: #4caf50;
  color: white;
}

.btn-success:hover {
  background: #45a049;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
}

.btn-info {
  background: #2196f3;
  color: white;
}

.btn-info:hover {
  background: #1976d2;
}

.navigation {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-top: 2rem;
}

.nav-link {
  color: var(--cyber-cyan);
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border: 2px solid var(--cyber-cyan);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: var(--cyber-cyan);
  color: #000;
}

@media (max-width: 768px) {
  .auth-test-container {
    grid-template-columns: 1fr;
  }

  .cookie-controls {
    flex-direction: column;
  }

  .navigation {
    flex-direction: column;
    align-items: center;
  }
}
</style>