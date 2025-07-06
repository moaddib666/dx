<template>
  <canvas 
    ref="canvas" 
    class="dice-canvas"
    @mousedown="handleMouseDown"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
    @wheel="handleWheel"
  ></canvas>
</template>

<script>
import * as THREE from 'three'
import { markRaw } from 'vue'
import D20Service from '@/services/dice/d20Service.js'
import RollStateService from '@/services/dice/rollStateService.js'
import D20TextureService from '@/services/dice/d20TextureService.js'

export default {
  name: 'DiceCanvas',

  emits: ['ready', 'error', 'roll-complete', 'state-change'],

  data() {
    return {
      d20Service: null,
      rollStateService: null,
      textureService: null,
      isInitialized: false,
      animationId: null,
      lastTime: 0,
      
      // Mouse controls
      mouseDown: false,
      mouseX: 0,
      mouseY: 0
    }
  },

  async mounted() {
    try {
      await this.initializeServices()
      await this.setupCanvas()
      this.startAnimation()
      this.$emit('ready')
    } catch (error) {
      console.error('Failed to initialize dice canvas:', error)
      this.$emit('error', error)
    }
  },

  beforeUnmount() {
    this.cleanup()
  },

  methods: {
    async initializeServices() {
      // Initialize services with markRaw to prevent Vue reactivity
      this.d20Service = markRaw(new D20Service())
      this.rollStateService = markRaw(new RollStateService())
      this.textureService = markRaw(new D20TextureService())

      // Setup callbacks
      this.rollStateService.setCallbacks({
        onStateChange: this.handleStateChange,
        onRollComplete: this.handleRollComplete,
        onNumberChange: this.handleNumberChange
      })
    },

    async setupCanvas() {
      const canvas = this.$refs.canvas
      const parent = canvas.parentElement
      
      // Set canvas size
      const width = parent.clientWidth || 800
      const height = parent.clientHeight || 600
      
      canvas.width = width
      canvas.height = height
      canvas.style.width = `${width}px`
      canvas.style.height = `${height}px`

      // Initialize D20 service
      const success = await this.d20Service.initializeScene(canvas, width, height)
      if (!success) {
        throw new Error('Failed to initialize 3D scene')
      }

      // Create initial dice
      this.d20Service.createDice()
      this.isInitialized = true
    },

    startAnimation() {
      const animate = (currentTime) => {
        if (!this.isInitialized) return

        const deltaTime = (currentTime - this.lastTime) / 1000
        this.lastTime = currentTime

        // Update roll state
        if (this.rollStateService.isCurrentlyRolling()) {
          const state = this.rollStateService.update(
            deltaTime,
            this.d20Service.faceNumbers,
            this.d20Service.faceNormals,
            this.d20Service.calculateTargetRotation.bind(this.d20Service)
          )

          // Update dice rotation and position
          this.d20Service.updateDiceRotation(state.rotation)
          this.d20Service.updateDicePosition(state.position)
        }

        // Render scene
        this.d20Service.render()

        this.animationId = requestAnimationFrame(animate)
      }

      this.animationId = requestAnimationFrame(animate)
    },

    async rollToTarget(targetNumber) {
      if (!this.isInitialized || this.rollStateService.isCurrentlyRolling()) {
        return null
      }

      return new Promise((resolve) => {
        // Store resolve function to call when roll completes
        this.pendingRollResolve = resolve

        // Start the roll
        this.rollStateService.startRoll(targetNumber, true)
      })
    },

    async rollRandom() {
      if (!this.isInitialized || this.rollStateService.isCurrentlyRolling()) {
        return null
      }

      const randomTarget = Math.floor(Math.random() * 20) + 1
      
      return new Promise((resolve) => {
        this.pendingRollResolve = resolve
        this.rollStateService.startRoll(randomTarget, false)
      })
    },

    async setUserTexture(file) {
      if (!this.textureService) return false

      const success = await this.textureService.setUserTexture(file)
      if (success && this.isInitialized) {
        // Rebuild dice with new texture
        this.d20Service.createDice()
      }
      return success
    },

    resetCamera() {
      if (this.d20Service) {
        this.d20Service.setCameraView('angle')
      }
    },

    setCameraView(viewType) {
      if (this.d20Service) {
        this.d20Service.setCameraView(viewType)
      }
    },

    toggleWireframe() {
      if (this.d20Service) {
        return this.d20Service.toggleWireframe()
      }
      return false
    },

    // Event handlers
    handleStateChange(state) {
      this.$emit('state-change', state)
    },

    handleRollComplete(result) {
      // Rebuild dice to highlight the result
      if (this.isInitialized) {
        const faceIndex = this.d20Service.faceNumbers.indexOf(result.number)
        this.d20Service.createDice(faceIndex)
      }

      this.$emit('roll-complete', result)
      
      // Resolve pending promise
      if (this.pendingRollResolve) {
        this.pendingRollResolve(result)
        this.pendingRollResolve = null
      }
    },

    handleNumberChange(number) {
      // This could be used to update UI displays in real-time
      this.$emit('number-change', number)
    },

    // Mouse control handlers
    handleMouseDown(event) {
      if (event.button !== 0) return // Only left click
      
      this.mouseDown = true
      this.mouseX = event.clientX
      this.mouseY = event.clientY
      event.preventDefault()
    },

    handleMouseUp() {
      this.mouseDown = false
    },

    handleMouseMove(event) {
      if (!this.mouseDown || !this.d20Service) return

      const deltaX = event.clientX - this.mouseX
      const deltaY = event.clientY - this.mouseY

      // Simple orbit controls
      const camera = this.d20Service.camera
      if (camera) {
        const spherical = new THREE.Spherical().setFromVector3(camera.position)
        spherical.theta -= deltaX * 0.01
        spherical.phi += deltaY * 0.01
        spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi))
        
        camera.position.setFromSpherical(spherical)
        camera.lookAt(0, 1, 0)
      }

      this.mouseX = event.clientX
      this.mouseY = event.clientY
    },

    handleWheel(event) {
      if (!this.d20Service) return

      const camera = this.d20Service.camera
      if (camera) {
        const spherical = new THREE.Spherical().setFromVector3(camera.position)
        spherical.radius += event.deltaY * 0.01
        spherical.radius = Math.max(3, Math.min(20, spherical.radius))
        
        camera.position.setFromSpherical(spherical)
        camera.lookAt(0, 1, 0)
      }

      event.preventDefault()
    },

    // Resize handling
    handleResize() {
      if (!this.isInitialized) return

      const canvas = this.$refs.canvas
      const parent = canvas.parentElement
      const width = parent.clientWidth || 800
      const height = parent.clientHeight || 600

      canvas.width = width
      canvas.height = height
      canvas.style.width = `${width}px`
      canvas.style.height = `${height}px`

      this.d20Service.resize(width, height)
    },

    cleanup() {
      if (this.animationId) {
        cancelAnimationFrame(this.animationId)
        this.animationId = null
      }

      if (this.d20Service) {
        this.d20Service.dispose()
        this.d20Service = null
      }

      if (this.rollStateService) {
        this.rollStateService.dispose()
        this.rollStateService = null
      }

      if (this.textureService) {
        this.textureService.dispose()
        this.textureService = null
      }

      this.isInitialized = false
    }
  }
}
</script>

<style scoped>
.dice-canvas {
  width: 100%;
  height: 100%;
  display: block;
  cursor: grab;
  background: transparent;
}

.dice-canvas:active {
  cursor: grabbing;
}
</style>