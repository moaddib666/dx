<template>
  <div class="google-auth-container">
    <div v-if="isGoogleAuthEnabled">
      <GoogleLogin
        :client-id="googleClientId"
        @success="handleGoogleSuccess"
        @error="handleGoogleError"
        :button-config="{
          theme: 'outline',
          size: 'large',
          text: 'signin_with',
          shape: 'rectangular',
          logo_alignment: 'left'
        }"
      />
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
    <div v-else class="google-auth-disabled">
      <!-- Google Auth is disabled -->
    </div>
  </div>
</template>

<script>
import { GoogleLogin } from 'vue3-google-login'
import { useI18n } from 'vue-i18n'
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'GoogleAuth',
  components: {
    GoogleLogin
  },
  props: {
    mode: {
      type: String,
      default: 'login', // 'login' or 'register'
      validator: (value) => ['login', 'register'].includes(value)
    }
  },
  emits: ['success', 'error'],
  setup(props, { emit }) {
    const { t } = useI18n()
    const store = useStore()
    const router = useRouter()

    const errorMessage = ref('')
    const googleClientId = import.meta.env.VITE_GOOGLE_AUTH_CLIENT_ID
    const googleAuthCookie = import.meta.env.VITE_GOOGLE_AUTH_HIDDEN_BY_COOKIE

    // Check if Google Auth is enabled by checking if client ID is provided
    // and if the cookie indicates it's enabled
    const isGoogleAuthEnabled = computed(() => {
      if (!googleClientId) return false

      // Check if there's a cookie that controls Google auth visibility
      if (googleAuthCookie) {
        // Check if the cookie exists and is set to enable Google auth
        const cookies = document.cookie.split(';')
        const authCookie = cookies.find(cookie =>
          cookie.trim().startsWith(`${googleAuthCookie}=`)
        )

        if (authCookie) {
          const cookieValue = authCookie.split('=')[1]
          return cookieValue === 'true' || cookieValue === '1'
        }

        // If cookie doesn't exist, default to enabled if client ID is present
        return true
      }

      return true
    })

    const handleGoogleSuccess = async (response) => {
      try {
        errorMessage.value = ''

        // Extract the credential (JWT token) from Google's response
        const { credential } = response

        if (!credential) {
          throw new Error('No credential received from Google')
        }

        // Send the Google token to your backend for verification and user creation/login
        const apiUrl = `${import.meta.env.VITE_API_BASE_URL}/auth/google/`
        const backendResponse = await axios.post(apiUrl, {
          token: credential,
          mode: props.mode // 'login' or 'register'
        })

        if (backendResponse.data.access) {
          // Store the JWT token in Vuex store
          store.dispatch('login', { token: backendResponse.data.access })

          // Emit success event to parent component
          emit('success', {
            user: backendResponse.data.user,
            token: backendResponse.data.access,
            mode: props.mode
          })

          // Redirect to dashboard
          router.push({ name: 'PlayerHomeDashboard' })
        } else {
          throw new Error('No access token received from backend')
        }

      } catch (error) {
        console.error('Google auth error:', error)

        let errorMsg = t('auth.googleAuthError')

        if (error.response) {
          // Backend returned an error
          if (error.response.status === 400) {
            errorMsg = error.response.data.message || t('auth.invalidGoogleToken')
          } else if (error.response.status === 409) {
            errorMsg = t('auth.userAlreadyExists')
          } else {
            errorMsg = t('auth.serverError')
          }
        } else if (error.message) {
          errorMsg = error.message
        }

        errorMessage.value = errorMsg
        emit('error', { error: errorMsg, mode: props.mode })
      }
    }

    const handleGoogleError = (error) => {
      console.error('Google login error:', error)
      const errorMsg = t('auth.googleLoginFailed')
      errorMessage.value = errorMsg
      emit('error', { error: errorMsg, mode: props.mode })
    }

    onMounted(() => {
      // Log configuration for debugging
      console.log('Google Auth Configuration:', {
        clientId: googleClientId ? 'Set' : 'Not set',
        cookieName: googleAuthCookie,
        isEnabled: isGoogleAuthEnabled.value,
        mode: props.mode
      })
    })

    return {
      errorMessage,
      googleClientId,
      isGoogleAuthEnabled,
      handleGoogleSuccess,
      handleGoogleError
    }
  }
}
</script>

<style scoped>
.google-auth-container {
  margin: 1rem 0;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 0.25rem;
  padding: 0.75rem 1rem;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.google-auth-disabled {
  display: none;
}

/* Ensure Google button fits well with the existing form styling */
:deep(.google-login-button) {
  width: 100%;
  margin: 0.5rem 0;
}
</style>