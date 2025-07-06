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

  emits: ['ready', 'error', 'roll-complete', 'state-change', 'number-change'],

  data() {
    return {
      d20Service: null,
      rollStateServices: [], // Array of roll state services for multiple dice
      textureService: null,
      isInitialized: false,
      animationId: null,
      lastTime: 0,

      // Multi-dice support
      diceCount: 1,
      resultMode: 'best',
      activeRolls: [], // Track active rolling states
      pendingResults: [], // Store results as they complete

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
      this.textureService = markRaw(new D20TextureService())

      // Initialize roll state services for potential multiple dice
      this.createRollStateServices(2) // Initialize for up to 2 dice
    },

    createRollStateServices(maxDice) {
      // Clear existing services
      this.rollStateServices.forEach(service => service.dispose())
      this.rollStateServices = []

      // Create roll state services for each potential dice
      for (let i = 0; i < maxDice; i++) {
        const rollStateService = markRaw(new RollStateService())

        // Set initial position for this specific dice based on its index
        this.initializeRollStatePosition(rollStateService, i)

        rollStateService.setCallbacks({
          onStateChange: (state) => this.handleStateChange(state, i),
          onRollComplete: (result) => this.handleRollComplete(result, i),
          onNumberChange: (number) => this.handleNumberChange(number, i)
        })
        this.rollStateServices.push(rollStateService)
      }
    },

    initializeRollStatePosition(rollStateService, diceIndex) {
      // Calculate the correct starting position for this dice based on current dice count
      const spacing = 3.5
      const currentDiceCount = this.diceCount || 1

      if (currentDiceCount === 1) {
        // Single dice always at center
        rollStateService.state.position.set(0, 1, 0)
      } else {
        // Multiple dice positioning
        const totalWidth = (currentDiceCount - 1) * spacing
        const startOffset = -totalWidth / 2
        const xOffset = startOffset + (diceIndex * spacing)
        rollStateService.state.position.set(xOffset, 1, 0)
      }
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

        // Update roll states for all active dice
        this.rollStateServices.forEach((rollStateService, index) => {
          if (rollStateService.isCurrentlyRolling() && index < this.diceCount) {
            const state = rollStateService.update(
              deltaTime,
              this.d20Service.faceNumbers,
              this.d20Service.faceNormals,
              this.d20Service.calculateTargetRotation.bind(this.d20Service)
            )

            // Update specific dice rotation and position
            this.d20Service.updateDiceRotation(state.rotation, index)
            this.d20Service.updateDicePosition(state.position, index)
          }
        })

        // Render scene
        this.d20Service.render(deltaTime)

        this.animationId = requestAnimationFrame(animate)
      }

      this.animationId = requestAnimationFrame(animate)
    },

    async rollToTarget(targetNumber) {
      if (!this.isInitialized || this.isAnyDiceRolling()) {
        return null
      }

      if (this.diceCount === 1) {
        // Single dice roll
        return new Promise((resolve) => {
          this.pendingRollResolve = resolve
          this.rollStateServices[0].startRoll(targetNumber, true)
        })
      } else {
        // Multiple dice roll - each dice gets the same target for now
        // For different targets per dice, use rollToTargets() method
        return this.rollMultipleDice([targetNumber, targetNumber], true)
      }
    },

    async rollToTargets(targetNumbers) {
      if (!this.isInitialized || this.isAnyDiceRolling()) {
        return null
      }

      if (!Array.isArray(targetNumbers)) {
        return this.rollToTarget(targetNumbers)
      }

      // Ensure we have enough targets for all dice
      const targets = [...targetNumbers]
      while (targets.length < this.diceCount) {
        targets.push(targets[targets.length - 1] || 20)
      }

      return this.rollMultipleDice(targets.slice(0, this.diceCount), true)
    },

    isAnyDiceRolling() {
      return this.rollStateServices.some(service => service.isCurrentlyRolling())
    },

    async rollRandom() {
      if (!this.isInitialized || this.isAnyDiceRolling()) {
        return null
      }
      for (let i = 0; i < this.diceCount; i++) {
        const randomTarget = Math.floor(Math.random() * 20) + 1
        new Promise((resolve) => {
          this.pendingRollResolve = resolve
          this.rollStateServices[i].startRoll(randomTarget, true)
        })
      }
    },

    async rollMultipleDice(targetNumbers = null, deterministic = false) {
      return new Promise((resolve) => {
        this.pendingResults = []
        this.pendingRollResolve = resolve

        // Start all dice rolling simultaneously
        for (let i = 0; i < this.diceCount; i++) {
          let diceTarget

          if (Array.isArray(targetNumbers)) {
            // Individual targets for each dice
            diceTarget = targetNumbers[i] || (Math.floor(Math.random() * 20) + 1)
          } else if (targetNumbers !== null) {
            // Same target for all dice
            diceTarget = targetNumbers
          } else {
            // Random target for each dice
            diceTarget = Math.floor(Math.random() * 20) + 1
          }

          this.rollStateServices[i].startRoll(diceTarget, deterministic)
        }
      })
    },

    calculateMultiDiceResult(results) {
      const numbers = results.map(r => r.number)
      let finalNumber
      let resultType = 'multiple'

      switch (this.resultMode) {
        case 'best':
          finalNumber = Math.max(...numbers)
          resultType = 'best'
          break
        case 'worst':
          finalNumber = Math.min(...numbers)
          resultType = 'worst'
          break
        case 'both':
          finalNumber = numbers
          resultType = 'both'
          break
        default:
          finalNumber = Math.max(...numbers)
          resultType = 'best'
      }

      return {
        number: finalNumber,
        numbers: numbers,
        resultType: resultType,
        rollTime: Math.max(...results.map(r => r.rollTime)),
        isDeterministic: results[0].isDeterministic,
        targetNumber: results[0].targetNumber,
        diceCount: this.diceCount
      }
    },

    async setUserTexture(file) {
      if (!this.d20Service) return false

      const success = await this.d20Service.setUserTexture(file)
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

    // Material and shader control methods
    setMaterialType(materialType) {
      if (this.d20Service) {
        return this.d20Service.setMaterialType(materialType)
      }
      return false
    },

    setShaderType(shaderType) {
      if (this.d20Service) {
        return this.d20Service.setShaderType(shaderType)
      }
      return false
    },

    getMaterialTypes() {
      if (this.d20Service) {
        return this.d20Service.getMaterialTypes()
      }
      return []
    },

    getShaderTypes() {
      if (this.d20Service) {
        return this.d20Service.getShaderTypes()
      }
      return []
    },

    getCurrentMaterialType() {
      if (this.d20Service) {
        return this.d20Service.getCurrentMaterialType()
      }
      return 'plastic'
    },

    getCurrentShaderType() {
      if (this.d20Service) {
        return this.d20Service.getCurrentShaderType()
      }
      return 'none'
    },

    // Multi-dice support methods
    setDiceCount(count) {
      this.diceCount = count
      if (this.isInitialized) {
        this.updateDiceConfiguration()
      }
    },

    setResultMode(mode) {
      this.resultMode = mode
    },

    updateDiceConfiguration() {
      // Always update the dice count and recreate the scene
      this.d20Service.diceCount = this.diceCount

      if (this.diceCount === 1) {
        // Single dice mode - use original setup
        this.d20Service.createDice()
      } else if (this.diceCount === 2) {
        // Two dice mode - create two dice with appropriate positioning
        this.d20Service.createMultipleDice(2)
      }

      // Update roll state services positions for new dice count
      this.updateRollStatePositions()
    },

    updateRollStatePositions() {
      // Recalculate and update positions for all roll state services
      for (let i = 0; i < this.rollStateServices.length; i++) {
        this.initializeRollStatePosition(this.rollStateServices[i], i)
      }
    },

    // Event handlers
    handleStateChange(state, diceIndex) {
      // For single dice or first dice, emit state change
      if (diceIndex === 0) {
        this.$emit('state-change', state)
      }
    },

    handleRollComplete(result, diceIndex) {
      // Store result for this specific dice
      this.pendingResults[diceIndex] = { ...result, diceIndex }

      // Check if all dice have completed
      if (this.pendingResults.length === this.diceCount &&
          this.pendingResults.every(r => r !== undefined)) {

        if (this.diceCount === 1) {
          // Single dice - highlight and emit
          const faceIndex = this.d20Service.faceNumbers.indexOf(result.number)
          this.d20Service.createDice(faceIndex)

          this.$emit('roll-complete', result)

          if (this.pendingRollResolve) {
            this.pendingRollResolve(result)
            this.pendingRollResolve = null
          }
        } else {
          // Multiple dice - calculate final result
          const finalResult = this.calculateMultiDiceResult(this.pendingResults)

          // Highlight dice based on result mode - use ordered results by dice index
          const orderedResults = new Array(this.diceCount)
          this.pendingResults.forEach(res => {
            orderedResults[res.diceIndex] = res
          })

          this.highlightMultipleDice(orderedResults, finalResult)

          this.$emit('roll-complete', finalResult)

          if (this.pendingRollResolve) {
            this.pendingRollResolve(finalResult)
            this.pendingRollResolve = null
          }
        }

        // Clear pending results
        this.pendingResults = []
      }
    },

    highlightMultipleDice(results, finalResult) {
      // Create highlight faces array with each dice's target number
      const highlightFaces = results.map(result => result.number)

      // Use the new individual highlighting method
      this.d20Service.createDiceWithIndividualHighlights(highlightFaces)
    },

    handleNumberChange(number, diceIndex) {
      // For single dice or first dice, emit number change
      if (diceIndex === 0) {
        this.$emit('number-change', number)
      }
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

      this.rollStateServices.forEach(service => {
        if (service) {
          service.dispose()
        }
      })
      this.rollStateServices = []

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