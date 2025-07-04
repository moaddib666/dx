<template>
  <div class="dice-roller">
    <div ref="diceContainer" class="dice-container"></div>
    <div class="dice-controls">
      <button @click="rollDice" :disabled="isRolling" class="roll-button">
        {{ isRolling ? 'Rolling...' : 'Roll Dice' }}
      </button>
      <div v-if="results.length > 0" class="results">
        <h3>Results: {{ results.join(', ') }} (Total: {{ totalResult }})</h3>
      </div>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three'
import { markRaw } from 'vue'

export default {
  name: 'NewDiceRoller',
  props: {
    numberOfDice: {
      type: Number,
      default: 2
    },
    numberOfEdges: {
      type: Number,
      default: 6,
      validator: (value) => [4, 6, 8, 10, 12, 20].includes(value)
    },
    expectedResults: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      dice: [],
      results: [],
      totalResult: 0,
      isRolling: false,
      animationId: null
    }
  },
  mounted() {
    this.initThreeJS()
    this.createDice()
    this.animate()
  },
  beforeUnmount() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId)
    }
    if (this.renderer) {
      this.renderer.dispose()
    }
  },
  watch: {
    numberOfDice() {
      // Recreate dice when the number of dice changes
      this.clearDice()
      this.createDice()
    },
    numberOfEdges() {
      // Recreate dice when the number of edges changes
      this.clearDice()
      this.createDice()
    }
  },
  methods: {
    initThreeJS() {
      // Scene setup
      this.scene = markRaw(new THREE.Scene())
      this.scene.background = new THREE.Color(0x0a0a0a)

      // Camera setup
      const container = this.$refs.diceContainer
      const width = container.clientWidth || 400
      const height = container.clientHeight || 300

      this.camera = markRaw(new THREE.PerspectiveCamera(75, width / height, 0.1, 1000))
      this.camera.position.set(0, 8, 10)
      this.camera.lookAt(0, 0, 0)

      // Renderer setup
      this.renderer = markRaw(new THREE.WebGLRenderer({ antialias: true, alpha: true }))
      this.renderer.setSize(width, height)
      this.renderer.shadowMap.enabled = true
      this.renderer.shadowMap.type = THREE.PCFSoftShadowMap
      container.appendChild(this.renderer.domElement)

      // Lighting
      const ambientLight = markRaw(new THREE.AmbientLight(0x404040, 0.4))
      this.scene.add(ambientLight)

      const directionalLight = markRaw(new THREE.DirectionalLight(0x00ffff, 1))
      directionalLight.position.set(5, 10, 5)
      directionalLight.castShadow = true
      directionalLight.shadow.mapSize.width = 1024
      directionalLight.shadow.mapSize.height = 1024
      this.scene.add(directionalLight)

      // Point light for cyberpunk glow
      const pointLight = markRaw(new THREE.PointLight(0xff00ff, 0.5, 50))
      pointLight.position.set(-5, 5, 5)
      this.scene.add(pointLight)

      // Table (invisible collision surface)
      const tableGeometry = markRaw(new THREE.PlaneGeometry(20, 20))
      const tableMaterial = markRaw(new THREE.MeshLambertMaterial({
        color: 0x111111,
        transparent: true,
        opacity: 0.1
      }))
      const table = markRaw(new THREE.Mesh(tableGeometry, tableMaterial))
      table.rotation.x = -Math.PI / 2
      table.position.y = -2
      table.receiveShadow = true
      this.scene.add(table)
    },

    createDiceGeometry(edges) {
      switch (edges) {
        case 4: return markRaw(new THREE.TetrahedronGeometry(1))
        case 6: return markRaw(new THREE.BoxGeometry(2, 2, 2))
        case 8: return markRaw(new THREE.OctahedronGeometry(1.2))
        case 10: return markRaw(new THREE.ConeGeometry(1, 2, 10))
        case 12: return markRaw(new THREE.DodecahedronGeometry(1))
        case 20: return markRaw(new THREE.IcosahedronGeometry(1.2))
        default: return markRaw(new THREE.BoxGeometry(2, 2, 2))
      }
    },

    createDiceMaterial() {
      // Create cyberpunk-style material
      const canvas = document.createElement('canvas')
      canvas.width = 512
      canvas.height = 512
      const ctx = canvas.getContext('2d')

      // Base texture
      const gradient = ctx.createLinearGradient(0, 0, 512, 512)
      gradient.addColorStop(0, '#1a1a2e')
      gradient.addColorStop(0.5, '#16213e')
      gradient.addColorStop(1, '#0f3460')

      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, 512, 512)

      // Add circuit pattern
      ctx.strokeStyle = '#00ffff'
      ctx.lineWidth = 2
      ctx.globalAlpha = 0.3

      for (let i = 0; i < 20; i++) {
        ctx.beginPath()
        ctx.moveTo(Math.random() * 512, Math.random() * 512)
        ctx.lineTo(Math.random() * 512, Math.random() * 512)
        ctx.stroke()
      }

      const texture = markRaw(new THREE.CanvasTexture(canvas))

      return markRaw(new THREE.MeshPhongMaterial({
        map: texture,
        emissive: 0x001122,
        emissiveIntensity: 0.2,
        shininess: 100
      }))
    },

    clearDice() {
      // Remove all dice from the scene
      if (this.scene) {
        this.dice.forEach(die => {
          this.scene.remove(die)
        })
      }
      this.dice = []
    },

    createDice() {
      // Clear existing dice if any
      if (this.dice.length > 0) {
        this.clearDice()
      }

      for (let i = 0; i < this.numberOfDice; i++) {
        const geometry = this.createDiceGeometry(this.numberOfEdges)
        const material = this.createDiceMaterial()

        const die = markRaw(new THREE.Mesh(geometry, material))
        die.position.set(
            (i - this.numberOfDice / 2) * 3,
            5 + Math.random() * 2,
            Math.random() * 2 - 1
        )
        die.rotation.set(
            Math.random() * Math.PI,
            Math.random() * Math.PI,
            Math.random() * Math.PI
        )
        die.castShadow = true
        die.receiveShadow = true

        // Physics properties
        die.velocity = markRaw(new THREE.Vector3(
            (Math.random() - 0.5) * 0.1,
            0,
            (Math.random() - 0.5) * 0.1
        ))
        die.angularVelocity = markRaw(new THREE.Vector3(
            (Math.random() - 0.5) * 0.2,
            (Math.random() - 0.5) * 0.2,
            (Math.random() - 0.5) * 0.2
        ))
        die.bounces = 0
        die.settled = false

        this.scene.add(die)
        this.dice.push(die)
      }
    },

    rollDice() {
      if (this.isRolling) return

      this.isRolling = true
      this.results = []
      this.totalResult = 0

      // Ensure we have the correct number and type of dice
      if (this.dice.length !== this.numberOfDice ||
          (this.dice.length > 0 && this.dice[0].geometry.type !== this.createDiceGeometry(this.numberOfEdges).type)) {
        this.clearDice()
        this.createDice()
      }

      // Reset dice positions and add force
      this.dice.forEach((die, index) => {
        die.position.set(
            (index - this.numberOfDice / 2) * 3,
            5 + Math.random() * 3,
            Math.random() * 2 - 1
        )
        // If velocity doesn't exist yet, create it
        if (!die.velocity) {
            die.velocity = markRaw(new THREE.Vector3())
        }

        // If angularVelocity doesn't exist yet, create it
        if (!die.angularVelocity) {
            die.angularVelocity = markRaw(new THREE.Vector3())
        }

        die.velocity.set(
            (Math.random() - 0.5) * 0.3,
            -0.1,
            (Math.random() - 0.5) * 0.3
        )
        die.angularVelocity.set(
            (Math.random() - 0.5) * 0.5,
            (Math.random() - 0.5) * 0.5,
            (Math.random() - 0.5) * 0.5
        )
        die.bounces = 0
        die.settled = false
      })

      // Check for settled dice after delay
      setTimeout(() => {
        this.checkResults()
      }, 3000)
    },

    updatePhysics() {
      this.dice.forEach((die) => {
        if (!die.settled) {
          // Apply gravity
          die.velocity.y -= 0.015

          // Update position
          die.position.add(die.velocity)

          // Update rotation
          die.rotation.x += die.angularVelocity.x
          die.rotation.y += die.angularVelocity.y
          die.rotation.z += die.angularVelocity.z

          // Collision with table
          if (die.position.y <= -1 && die.velocity.y < 0) {
            die.position.y = -1
            die.velocity.y = -die.velocity.y * 0.6 // Bounce with energy loss
            die.velocity.x *= 0.8 // Friction
            die.velocity.z *= 0.8
            die.angularVelocity.multiplyScalar(0.8)
            die.bounces++

            // Settle if energy is low
            if (Math.abs(die.velocity.y) < 0.02 && die.bounces > 2) {
              die.velocity.set(0, 0, 0)
              die.angularVelocity.set(0, 0, 0)
              die.settled = true
            }
          }

          // Boundaries
          if (Math.abs(die.position.x) > 8) {
            die.velocity.x = -die.velocity.x * 0.7
          }
          if (Math.abs(die.position.z) > 8) {
            die.velocity.z = -die.velocity.z * 0.7
          }
        }
      })
    },

    checkResults() {
      // Simple result calculation based on dice orientation
      this.results = this.dice.map((die) => {
        // Calculate which face is up based on rotation
        const upVector = markRaw(new THREE.Vector3(0, 1, 0))
        upVector.applyQuaternion(die.quaternion)

        // Simple mapping - in a real implementation you'd want more sophisticated face detection
        let result
        if (this.numberOfEdges === 6) {
          if (upVector.y > 0.8) result = 1
          else if (upVector.y < -0.8) result = 6
          else if (upVector.x > 0.8) result = 2
          else if (upVector.x < -0.8) result = 5
          else if (upVector.z > 0.8) result = 3
          else result = 4
        } else {
          // For other dice, use random but consistent based on final position
          const seed = Math.floor(die.position.x * 100 + die.position.z * 100 + die.rotation.y * 100)
          result = (Math.abs(seed) % this.numberOfEdges) + 1
        }

        return Math.max(1, Math.min(this.numberOfEdges, result))
      })

      this.totalResult = this.results.reduce((sum, result) => sum + result, 0)
      this.isRolling = false

      this.$emit('diceRolled', {
        results: this.results,
        total: this.totalResult
      })
    },

    animate() {
      this.animationId = requestAnimationFrame(this.animate)

      if (this.isRolling) {
        this.updatePhysics()
      }

      this.renderer.render(this.scene, this.camera)
    }
  }
}
</script>

<style scoped>
.dice-roller {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #0a0a0a, #1a1a2e);
  border-radius: 10px;
  border: 1px solid #00ffff;
}

.dice-container {
  width: 400px;
  height: 300px;
  border: 2px solid #00ffff;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.dice-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.roll-button {
  padding: 12px 24px;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  color: #000;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.roll-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
}

.roll-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 0.8; }
  100% { opacity: 0.6; }
}

.results {
  text-align: center;
  color: #00ffff;
  font-family: 'Courier New', monospace;
}

.results h3 {
  margin: 0;
  font-size: 18px;
  text-shadow: 0 0 10px #00ffff;
}
</style>