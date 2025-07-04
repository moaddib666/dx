<template>
  <div class="dice-roller-container">
    <div ref="canvasContainer" class="canvas-container">
      <canvas ref="canvas" class="dice-canvas"></canvas>

      <!-- Loading overlay -->
      <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner">
          <div class="spinner"></div>
          <p>Loading Dimension-X Dice...</p>
        </div>
      </div>

      <!-- Dice Controls -->
      <div class="dice-controls" v-if="!loading && showControls">
        <div class="control-panel">
          <h3 class="panel-title">🎲 Dice Roller</h3>

          <div class="dice-buttons">
            <button
                v-for="die in availableDice"
                :key="die"
                @click="rollDice(die)"
                :disabled="isRolling"
                class="dice-button"
                :class="{ rolling: isRolling }"
            >
              d{{ die }}
            </button>
          </div>

          <div class="quick-actions">
            <button @click="rollMultiple(6, 2)" :disabled="isRolling" class="action-button">
              2d6
            </button>
            <button @click="rollAdvantage()" :disabled="isRolling" class="action-button">
              Advantage
            </button>
            <button @click="clearDice()" class="action-button clear">
              Clear All
            </button>
          </div>
        </div>

        <!-- Results Panel -->
        <div class="results-panel">
          <h3 class="panel-title">🎯 Results</h3>
          <div class="results-list">
            <div
                v-for="result in recentResults"
                :key="result.id"
                class="result-item"
                :class="{ 'critical': isCritical(result) }"
            >
              <span class="dice-type">d{{ result.sides }}</span>
              <span class="result-value">{{ result.value }}</span>
              <span v-if="result.modifier" class="modifier">
                {{ result.modifier > 0 ? '+' : '' }}{{ result.modifier }}
              </span>
            </div>
          </div>

          <div v-if="rollSummary" class="roll-summary">
            <strong>Total: {{ rollSummary.total }}</strong>
            <span v-if="rollSummary.count > 1">({{ rollSummary.count }} dice)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three'
import * as CANNON from 'cannon'
import { markRaw } from 'vue'

export default {
  name: 'DiceRoller',

  props: {
    width: {
      type: Number,
      default: 800
    },
    height: {
      type: Number,
      default: 600
    },
    theme: {
      type: String,
      default: 'cyberpunk' // 'cyberpunk', 'classic', 'fantasy'
    },
    autoRoll: {
      type: Boolean,
      default: false
    },
    showControls: {
      type: Boolean,
      default: true
    }
  },

  data() {
    return {
      loading: true,
      isRolling: false,
      scene: null,
      camera: null,
      renderer: null,
      world: null,
      dice: [],
      results: [],
      availableDice: [4, 6, 8, 10, 12, 20, 100],
      diceMaterials: {},
      nextResultId: 1
    }
  },

  computed: {
    recentResults() {
      return this.results.slice(-10).reverse()
    },

    rollSummary() {
      if (this.results.length === 0) return null

      // Get results from the last 5 seconds
      const now = Date.now()
      const recentRolls = this.results.filter(r => now - r.timestamp < 5000)

      if (recentRolls.length === 0) return null

      const total = recentRolls.reduce((sum, r) => sum + r.value + (r.modifier || 0), 0)

      return {
        total,
        count: recentRolls.length
      }
    },

    diceColors() {
      const themes = {
        cyberpunk: {
          4: 0x00ffff,   // Cyan
          6: 0xff6600,   // Orange
          8: 0x00ff00,   // Green
          10: 0xff0066,  // Pink
          12: 0x6600ff,  // Purple
          20: 0xffff00,  // Yellow
          100: 0xff0000  // Red
        },
        classic: {
          4: 0xffffff,   // White
          6: 0xff0000,   // Red
          8: 0x0000ff,   // Blue
          10: 0x00ff00,  // Green
          12: 0xffff00,  // Yellow
          20: 0xff00ff,  // Magenta
          100: 0x000000  // Black
        },
        fantasy: {
          4: 0x8b4513,   // Brown
          6: 0xdaa520,   // Goldenrod
          8: 0x228b22,   // Forest Green
          10: 0x4169e1,  // Royal Blue
          12: 0x9932cc,  // Dark Orchid
          20: 0xdc143c,  // Crimson
          100: 0x2f4f4f   // Dark Slate Gray
        }
      }

      return themes[this.theme] || themes.cyberpunk
    }
  },

  mounted() {
    this.initThreeJS()
  },

  beforeUnmount() {
    this.cleanup()
  },

  methods: {
    async initThreeJS() {
      try {
        await this.setupScene()
        await this.setupPhysics()
        await this.setupLighting()
        await this.createTable()
        await this.createMaterials()

        this.animate()
        this.loading = false

        this.$emit('ready')
      } catch (error) {
        console.error('Failed to initialize dice roller:', error)
        this.$emit('error', error)
      }
    },

    async setupScene() {
      // Scene - using markRaw to prevent proxy issues
      this.scene = markRaw(new THREE.Scene())
      this.scene.fog = new THREE.Fog(0x0a0a0a, 10, 50)

      // Camera - using markRaw to prevent proxy issues
      this.camera = markRaw(new THREE.PerspectiveCamera(
          75,
          this.width / this.height,
          0.1,
          1000
      ))
      this.camera.position.set(0, 8, 12)
      this.camera.lookAt(0, 0, 0)

      // Renderer - using markRaw to prevent proxy issues
      this.renderer = markRaw(new THREE.WebGLRenderer({
        canvas: this.$refs.canvas,
        antialias: true
      }))
      this.renderer.setSize(this.width, this.height)
      this.renderer.shadowMap.enabled = true
      this.renderer.shadowMap.type = THREE.PCFSoftShadowMap
      this.renderer.setClearColor(0x0a0a0a)
    },

    async setupPhysics() {
      // Using markRaw to prevent proxy issues
      this.world = markRaw(new CANNON.World())
      this.world.gravity.set(0, -9.82, 0)
      this.world.broadphase = new CANNON.NaiveBroadphase()

      // Add material properties for realistic bouncing
      const diceMaterial = new CANNON.Material('dice')
      const tableMaterial = new CANNON.Material('table')

      const diceTableContact = new CANNON.ContactMaterial(
          diceMaterial,
          tableMaterial,
          {
            friction: 0.4,
            restitution: 0.3
          }
      )

      this.world.addContactMaterial(diceTableContact)
    },

    async setupLighting() {
      // Ambient light
      const ambientLight = new THREE.AmbientLight(0x404040, 0.3)
      this.scene.add(ambientLight)

      // Main directional light
      const mainLight = new THREE.DirectionalLight(0xffffff, 0.8)
      mainLight.position.set(5, 10, 5)
      mainLight.castShadow = true
      mainLight.shadow.mapSize.width = 2048
      mainLight.shadow.mapSize.height = 2048
      this.scene.add(mainLight)

      // Theme-specific accent lighting
      if (this.theme === 'cyberpunk') {
        const cyanLight = new THREE.PointLight(0x00ffff, 0.5, 20)
        cyanLight.position.set(-5, 5, 5)
        this.scene.add(cyanLight)

        const orangeLight = new THREE.PointLight(0xff6600, 0.3, 15)
        orangeLight.position.set(5, 3, -5)
        this.scene.add(orangeLight)
      }
    },

    async createTable() {
      // Visual table
      const tableGeometry = new THREE.BoxGeometry(20, 0.5, 20)
      const tableMaterial = new THREE.MeshLambertMaterial({
        color: this.theme === 'cyberpunk' ? 0x2a2a2a : 0x8b4513,
        transparent: true,
        opacity: 0.8
      })
      const table = new THREE.Mesh(tableGeometry, tableMaterial)
      table.position.y = -2
      table.receiveShadow = true
      this.scene.add(table)

      // Physics table
      const tableShape = new CANNON.Plane()
      const tableBody = new CANNON.Body({ mass: 0 })
      tableBody.addShape(tableShape)
      tableBody.quaternion.setFromAxisAngle(new CANNON.Vec3(1, 0, 0), -Math.PI / 2)
      tableBody.position.set(0, -2, 0)
      this.world.add(tableBody)

      // Table walls
      this.createTableWalls()
    },

    createTableWalls() {
      const wallHeight = 5
      const wallThickness = 0.5
      const tableSize = 10

      const walls = [
        { pos: [tableSize, wallHeight/2, 0], size: [wallThickness, wallHeight, tableSize] },
        { pos: [-tableSize, wallHeight/2, 0], size: [wallThickness, wallHeight, tableSize] },
        { pos: [0, wallHeight/2, tableSize], size: [tableSize, wallHeight, wallThickness] },
        { pos: [0, wallHeight/2, -tableSize], size: [tableSize, wallHeight, wallThickness] }
      ]

      walls.forEach(wall => {
        const wallShape = new CANNON.Box(new CANNON.Vec3(...wall.size))
        const wallBody = new CANNON.Body({ mass: 0 })
        wallBody.addShape(wallShape)
        wallBody.position.set(...wall.pos)
        this.world.add(wallBody)
      })
    },

    async createMaterials() {
      Object.keys(this.diceColors).forEach(sides => {
        const color = this.diceColors[sides]
        // Using markRaw to prevent proxy issues
        this.diceMaterials[sides] = markRaw(new THREE.MeshPhongMaterial({
          color: color,
          shininess: 100,
          transparent: true,
          opacity: 0.9
        }))
      })
    },

    createDiceGeometry(sides) {
      const geometries = {
        4: () => new THREE.TetrahedronGeometry(1.5),
        6: () => new THREE.BoxGeometry(2, 2, 2),
        8: () => new THREE.OctahedronGeometry(1.5),
        10: () => new THREE.ConeGeometry(1.5, 2, 10),
        12: () => new THREE.DodecahedronGeometry(1.5),
        20: () => new THREE.IcosahedronGeometry(1.5),
        100: () => new THREE.SphereGeometry(1.5, 16, 16)
      }

      return geometries[sides] ? geometries[sides]() : geometries[6]()
    },

    createDicePhysics(sides) {
      const shapes = {
        4: () => new CANNON.Sphere(1.5),
        6: () => new CANNON.Box(new CANNON.Vec3(1, 1, 1)),
        8: () => new CANNON.Sphere(1.5),
        10: () => new CANNON.Sphere(1.5),
        12: () => new CANNON.Sphere(1.5),
        20: () => new CANNON.Sphere(1.5),
        100: () => new CANNON.Sphere(1.5)
      }

      return shapes[sides] ? shapes[sides]() : shapes[6]()
    },

    async rollDice(sides, modifier = 0) {
      if (this.isRolling) return

      this.isRolling = true

      try {
        // Create visual dice - using markRaw to prevent proxy issues
        const diceGeometry = this.createDiceGeometry(sides)
        const diceMesh = markRaw(new THREE.Mesh(diceGeometry, this.diceMaterials[sides]))
        diceMesh.castShadow = true
        diceMesh.receiveShadow = true

        // Random position and rotation
        const x = (Math.random() - 0.5) * 6
        const z = (Math.random() - 0.5) * 6
        diceMesh.position.set(x, 8, z)
        diceMesh.rotation.set(
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2
        )

        this.scene.add(diceMesh)

        // Create physics body - using markRaw to prevent proxy issues
        const diceShape = this.createDicePhysics(sides)
        const diceBody = markRaw(new CANNON.Body({ mass: 1 }))
        diceBody.addShape(diceShape)
        diceBody.position.set(x, 8, z)

        // Add random spin and velocity
        diceBody.angularVelocity.set(
            (Math.random() - 0.5) * 20,
            (Math.random() - 0.5) * 20,
            (Math.random() - 0.5) * 20
        )

        diceBody.velocity.set(
            (Math.random() - 0.5) * 4,
            0,
            (Math.random() - 0.5) * 4
        )

        this.world.add(diceBody)

        // Store dice info
        const diceInfo = {
          mesh: diceMesh,
          body: diceBody,
          sides: sides,
          settled: false,
          id: this.nextResultId++
        }

        this.dice.push(diceInfo)

        // Wait for dice to settle and calculate result
        setTimeout(() => {
          const result = this.calculateDiceResult(diceInfo)
          this.addResult(sides, result, modifier, diceInfo.id)
          this.isRolling = false
        }, 3000)

        // Emit roll event
        this.$emit('roll', { sides, modifier })

      } catch (error) {
        console.error('Error rolling dice:', error)
        this.isRolling = false
      }
    },

    calculateDiceResult(diceInfo) {
      // For now, return random result
      // In production, you'd analyze the dice orientation
      return Math.floor(Math.random() * diceInfo.sides) + 1
    },

    addResult(sides, value, modifier = 0, id) {
      const result = {
        id,
        sides,
        value,
        modifier,
        timestamp: Date.now()
      }

      this.results.push(result)

      // Keep only last 50 results
      if (this.results.length > 50) {
        this.results = this.results.slice(-50)
      }

      // Emit result event
      this.$emit('result', result)
    },

    isCritical(result) {
      return result.value === 1 || result.value === result.sides
    },

    async rollMultiple(sides, count = 2) {
      for (let i = 0; i < count; i++) {
        await new Promise(resolve => setTimeout(resolve, i * 200))
        this.rollDice(sides)
      }
    },

    async rollAdvantage() {
      this.rollDice(20)
      setTimeout(() => this.rollDice(20), 200)
    },

    clearDice() {
      this.dice.forEach(diceInfo => {
        this.scene.remove(diceInfo.mesh)
        this.world.remove(diceInfo.body)
      })

      this.dice = []
      this.results = []
      this.isRolling = false

      this.$emit('clear')
    },

    animate() {
      requestAnimationFrame(this.animate)

      // Step physics
      this.world.step(1/60)

      // Update dice positions
      this.dice.forEach(diceInfo => {
        diceInfo.mesh.position.copy(diceInfo.body.position)
        diceInfo.mesh.quaternion.copy(diceInfo.body.quaternion)
      })

      // Render scene
      this.renderer.render(this.scene, this.camera)
    },

    cleanup() {
      if (this.renderer) {
        this.renderer.dispose()
      }

      // Clean up geometries and materials
      this.dice.forEach(diceInfo => {
        if (diceInfo.mesh) {
          diceInfo.mesh.geometry.dispose()
          diceInfo.mesh.material.dispose()
        }
      })
    },

    // Public API methods
    roll(sides, modifier = 0) {
      return this.rollDice(sides, modifier)
    },

    getResults() {
      return [...this.results]
    },

    getLastResult() {
      return this.results[this.results.length - 1] || null
    }
  }
}
</script>

<style scoped>
.dice-roller-container {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
  border-radius: 10px;
  overflow: hidden;
}

.canvas-container {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 5;
}

.dice-canvas {
  width: 100%;
  height: 100%;
  display: block;
  position: relative;
  z-index: 5;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.loading-spinner {
  text-align: center;
  color: #00ffff;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #333;
  border-top: 4px solid #00ffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.dice-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  display: flex;
  justify-content: space-between;
  z-index: 10;
  pointer-events: none;
}

.control-panel,
.results-panel {
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #00ffff;
  border-radius: 10px;
  padding: 20px;
  pointer-events: auto;
  backdrop-filter: blur(10px);
}

.control-panel {
  max-width: 300px;
}

.results-panel {
  max-width: 250px;
  border-color: #00ff00;
}

.panel-title {
  margin: 0 0 15px 0;
  color: #00ffff;
  font-size: 18px;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.results-panel .panel-title {
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.dice-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 15px;
}

.dice-button {
  background: linear-gradient(45deg, #0066cc, #004499);
  border: 2px solid #00ffff;
  color: white;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

.dice-button:hover:not(:disabled) {
  background: linear-gradient(45deg, #0088ff, #0066cc);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  transform: translateY(-2px);
}

.dice-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dice-button.rolling {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.quick-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-button {
  background: linear-gradient(45deg, #cc6600, #994400);
  border: 2px solid #ffaa00;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 60px;
}

.action-button:hover:not(:disabled) {
  background: linear-gradient(45deg, #ff8800, #cc6600);
  box-shadow: 0 0 10px rgba(255, 170, 0, 0.5);
}

.action-button.clear {
  background: linear-gradient(45deg, #cc0000, #990000);
  border-color: #ff4444;
}

.action-button.clear:hover:not(:disabled) {
  background: linear-gradient(45deg, #ff0000, #cc0000);
  box-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
}

.results-list {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 15px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 255, 0, 0.1);
  border: 1px solid #00ff00;
  border-radius: 5px;
  padding: 8px;
  margin: 5px 0;
  font-family: 'Courier New', monospace;
  transition: all 0.3s ease;
}

.result-item.critical {
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.dice-type {
  font-size: 12px;
  opacity: 0.8;
}

.result-value {
  font-weight: bold;
  font-size: 16px;
}

.modifier {
  font-size: 12px;
  color: #ffaa00;
}

.roll-summary {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid #00ffff;
  border-radius: 5px;
  padding: 10px;
  text-align: center;
  font-family: 'Courier New', monospace;
}

/* Responsive design */
@media (max-width: 768px) {
  .dice-controls {
    flex-direction: column;
    gap: 15px;
  }

  .control-panel,
  .results-panel {
    max-width: none;
  }

  .dice-buttons {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>