<template>
  <div class="dice-roller">
    <div ref="diceContainer" class="dice-container">
      <!-- No overlay - results are shown directly in 3D view -->
    </div>
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
    },
    // Prop to force specific dice results (for weighted dice)
    forcedResults: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      scene: null,
      camera: null,
      topCamera: null, // Camera for top-down view
      closeupCamera: null, // Camera for closeup view of dice results
      activeCamera: null, // Reference to the currently active camera
      renderer: null,
      dice: [],
      results: [],
      totalResult: 0,
      isRolling: false,
      animationId: null,
      showingResults: false, // Flag to indicate if we're showing the results view
      allDiceSettled: false, // Flag to indicate if all dice have settled
      tubeMesh: null, // Reference to the tube/glass container
      tubeRadius: 5, // Radius of the tube
      tubeHeight: 15, // Height of the tube
      waitingForSettling: false // Flag to indicate if we're waiting for dice to settle
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

      // Main camera (side view)
      this.camera = markRaw(new THREE.PerspectiveCamera(75, width / height, 0.1, 1000))
      this.camera.position.set(0, 8, 10)
      this.camera.lookAt(0, 0, 0)

      // Top camera (for results view)
      this.topCamera = markRaw(new THREE.PerspectiveCamera(75, width / height, 0.1, 1000))
      this.topCamera.position.set(0, 10, 0)
      this.topCamera.lookAt(0, 0, 0)

      // Closeup camera (for detailed dice results)
      this.closeupCamera = markRaw(new THREE.PerspectiveCamera(75, width / height, 0.1, 1000))
      this.closeupCamera.position.set(0, 3, 5)
      this.closeupCamera.lookAt(0, 0, 0)

      // Set active camera to main camera by default
      this.activeCamera = this.camera

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

      // Create glass tube/container for dice
      this.createGlassTube()
    },

    createGlassTube() {
      // Create a cylindrical tube to contain the dice
      const tubeGeometry = markRaw(new THREE.CylinderGeometry(
        this.tubeRadius, // top radius
        this.tubeRadius, // bottom radius
        this.tubeHeight, // height
        32, // radial segments
        1, // height segments
        true // open-ended
      ))

      // Create a glass-like material
      const tubeMaterial = markRaw(new THREE.MeshPhysicalMaterial({
        color: 0x00ffff,
        transparent: true,
        opacity: 0.2,
        roughness: 0.1,
        metalness: 0.8,
        clearcoat: 1.0,
        clearcoatRoughness: 0.1,
        side: THREE.DoubleSide
      }))

      this.tubeMesh = markRaw(new THREE.Mesh(tubeGeometry, tubeMaterial))
      this.tubeMesh.position.y = this.tubeHeight / 2 - 2 // Position the tube so its bottom is at the table
      this.tubeMesh.receiveShadow = true
      this.scene.add(this.tubeMesh)

      // Add a circular base for the tube
      const baseGeometry = markRaw(new THREE.CircleGeometry(this.tubeRadius, 32))
      const baseMaterial = markRaw(new THREE.MeshPhongMaterial({
        color: 0x00ffff,
        transparent: true,
        opacity: 0.3,
        shininess: 100
      }))

      const base = markRaw(new THREE.Mesh(baseGeometry, baseMaterial))
      base.rotation.x = -Math.PI / 2
      base.position.y = -1.99 // Just above the table
      base.receiveShadow = true
      this.scene.add(base)
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

    // Create a texture with a glowing number
    createNumberTexture(number) {
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

      for (let i = 0; i < 10; i++) {
        ctx.beginPath()
        ctx.moveTo(Math.random() * 512, Math.random() * 512)
        ctx.lineTo(Math.random() * 512, Math.random() * 512)
        ctx.stroke()
      }

      // Add glowing number
      ctx.globalAlpha = 1
      ctx.font = 'bold 280px Arial'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'

      // Glow effect
      ctx.shadowColor = '#00ffff'
      ctx.shadowBlur = 30
      ctx.fillStyle = '#00ffff'

      // Draw the number
      ctx.fillText(number.toString(), 256, 256)

      return markRaw(new THREE.CanvasTexture(canvas))
    },

    createDiceMaterial(faceNumber) {
      // Create a material with the number texture
      const texture = this.createNumberTexture(faceNumber)

      return markRaw(new THREE.MeshPhongMaterial({
        map: texture,
        emissive: 0x00ffff,
        emissiveIntensity: 0.3,
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
        let die

        if (this.numberOfEdges === 6) {
          // For cubes (d6), create a different material for each face
          // The order of materials must match the face detection logic in checkResults
          // +X (right), -X (left), +Y (top), -Y (bottom), +Z (front), -Z (back)
          const materials = [
            this.createDiceMaterial(2), // +X (right) face
            this.createDiceMaterial(5), // -X (left) face
            this.createDiceMaterial(6), // +Y (top) face
            this.createDiceMaterial(1), // -Y (bottom) face
            this.createDiceMaterial(3), // +Z (front) face
            this.createDiceMaterial(4)  // -Z (back) face
          ]

          const geometry = this.createDiceGeometry(this.numberOfEdges)
          die = markRaw(new THREE.Mesh(geometry, materials))
        } else {
          // For other dice types, use a single material with the appropriate number
          // This is a simplification - in a real implementation, you'd want to create
          // materials for each face based on the geometry
          const geometry = this.createDiceGeometry(this.numberOfEdges)

          // Create an array of materials for the number of faces
          const materials = []
          for (let face = 1; face <= this.numberOfEdges; face++) {
            materials.push(this.createDiceMaterial(face))
          }

          // Use the first material as a fallback for non-cube dice
          die = markRaw(new THREE.Mesh(geometry, materials[0]))

          // Store the materials array for result visualization
          die.allMaterials = materials
        }

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
        die.dieType = this.numberOfEdges // Store the die type

        this.scene.add(die)
        this.dice.push(die)
      }
    },

    rollDice() {
      if (this.isRolling) return

      this.isRolling = true
      this.results = []
      this.totalResult = 0
      this.allDiceSettled = false
      this.waitingForSettling = true

      // Switch back to main camera for rolling view
      this.activeCamera = this.camera
      this.showingResults = false

      // Ensure we have the correct number and type of dice
      if (this.dice.length !== this.numberOfDice ||
          (this.dice.length > 0 && this.dice[0].geometry.type !== this.createDiceGeometry(this.numberOfEdges).type)) {
        this.clearDice()
        this.createDice()
      }

      // Store the forced results for later use
      const forcedResults = [...this.forcedResults];

      // Reset dice positions and add force
      this.dice.forEach((die, index) => {
        // Store the target result for this die if provided
        if (forcedResults.length > index) {
          die.targetResult = forcedResults[index];
        } else {
          die.targetResult = null;
        }

        // Position dice at the top of the tube with slight randomness
        const angle = Math.random() * Math.PI * 2;
        const radius = Math.random() * (this.tubeRadius * 0.7);

        die.position.set(
            Math.cos(angle) * radius,
            this.tubeHeight - 4 - index * 0.5, // Stack dice at different heights
            Math.sin(angle) * radius
        )

        // If velocity doesn't exist yet, create it
        if (!die.velocity) {
            die.velocity = markRaw(new THREE.Vector3())
        }

        // If angularVelocity doesn't exist yet, create it
        if (!die.angularVelocity) {
            die.angularVelocity = markRaw(new THREE.Vector3())
        }

        // Add initial velocities for a dramatic roll
        die.velocity.set(
            (Math.random() - 0.5) * 0.3, // Horizontal movement
            -0.1 - Math.random() * 0.2, // Downward force
            (Math.random() - 0.5) * 0.3  // Horizontal movement
        )

        // Set initial rotation based on target result if provided
        if (die.targetResult) {
          this.setInitialRotationForResult(die, die.targetResult);
        } else {
          die.angularVelocity.set(
              (Math.random() - 0.5) * 0.6, // Rotation
              (Math.random() - 0.5) * 0.6, // Rotation
              (Math.random() - 0.5) * 0.6  // Rotation
          )
        }

        die.bounces = 0
        die.settled = false
      })

      // We'll check for results when all dice have settled in updatePhysics
      // But also set a maximum wait time as a fallback
      setTimeout(() => {
        if (this.isRolling && !this.allDiceSettled) {
          this.checkResults()
        }
      }, 5000)
    },

    // Helper method to set initial rotation for a specific result
    setInitialRotationForResult(die, targetResult) {
      // For d6 (cube), we can be more precise with the rotation
      if (this.numberOfEdges === 6) {
        // Set rotation to make the target face likely to end up on top
        // The rotation values are aligned with the checkResults method's face detection
        // For a standard six-sided die, opposite faces sum to 7
        switch(targetResult) {
          case 1: // 1 should be on top (negative Y)
            die.rotation.set(0, 0, 0); // Inverted from case 6
            die.angularVelocity.set(
              -0.05 + Math.random() * 0.1, // Reduced randomness for more predictable results
              Math.random() * 0.1,
              -0.05 + Math.random() * 0.1
            );
            break;
          case 6: // 6 should be on top (positive Y)
            die.rotation.set(Math.PI, 0, 0); // Inverted from case 1
            die.angularVelocity.set(
              -0.05 + Math.random() * 0.1,
              Math.random() * 0.1,
              -0.05 + Math.random() * 0.1
            );
            break;
          case 2: // 2 should be on top (positive X)
            die.rotation.set(0, 0, Math.PI/2); // Inverted from case 5
            die.angularVelocity.set(
              Math.random() * 0.1,
              Math.random() * 0.1,
              -0.05 + Math.random() * 0.1
            );
            break;
          case 5: // 5 should be on top (negative X)
            die.rotation.set(0, 0, -Math.PI/2); // Inverted from case 2
            die.angularVelocity.set(
              Math.random() * 0.1,
              Math.random() * 0.1,
              -0.05 + Math.random() * 0.1
            );
            break;
          case 3: // 3 should be on top (positive Z)
            die.rotation.set(-Math.PI/2, 0, 0); // Inverted from case 4
            die.angularVelocity.set(
              -0.05 + Math.random() * 0.1,
              Math.random() * 0.1,
              Math.random() * 0.1
            );
            break;
          case 4: // 4 should be on top (negative Z)
            die.rotation.set(Math.PI/2, 0, 0); // Inverted from case 3
            die.angularVelocity.set(
              -0.05 + Math.random() * 0.1,
              Math.random() * 0.1,
              Math.random() * 0.1
            );
            break;
        }

        // Store the target result for verification during settling
        die.targetResult = targetResult;

        // Reduce initial velocities for more controlled landing
        die.velocity.multiplyScalar(0.7);
      } else if (this.numberOfEdges === 4) {
        // For tetrahedron (d4), we need special handling
        // Tetrahedron has 4 faces, each face is a triangle
        // We'll use a simplified approach for now
        die.angularVelocity.set(
          (Math.random() - 0.5) * 0.3,
          (Math.random() - 0.5) * 0.3,
          (Math.random() - 0.5) * 0.3
        );
        die.targetResult = targetResult;
      } else {
        // For other dice types, use reduced randomness
        die.angularVelocity.set(
          (Math.random() - 0.5) * 0.3,
          (Math.random() - 0.5) * 0.3,
          (Math.random() - 0.5) * 0.3
        );
        die.targetResult = targetResult;
      }
    },

    updatePhysics() {
      let allSettled = true;

      // First update positions and handle non-dice collisions
      this.dice.forEach((die) => {
        if (!die.settled) {
          allSettled = false;

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

          // Collision with tube walls
          const distanceFromCenter = Math.sqrt(die.position.x * die.position.x + die.position.z * die.position.z);
          const dieSize = this.numberOfEdges === 6 ? 1.0 : 0.8; // Approximate die radius

          if (distanceFromCenter + dieSize > this.tubeRadius) {
            // Calculate normal vector from center to die
            const nx = die.position.x / distanceFromCenter;
            const nz = die.position.z / distanceFromCenter;

            // Reflect velocity vector off the wall
            const dot = die.velocity.x * nx + die.velocity.z * nz;
            die.velocity.x = die.velocity.x - 2 * dot * nx;
            die.velocity.z = die.velocity.z - 2 * dot * nz;

            // Apply energy loss and add some angular velocity for realistic bounce
            die.velocity.multiplyScalar(0.7);
            die.angularVelocity.x += (Math.random() - 0.5) * 0.2;
            die.angularVelocity.z += (Math.random() - 0.5) * 0.2;

            // Move die away from wall to prevent sticking
            die.position.x = nx * (this.tubeRadius - dieSize - 0.1);
            die.position.z = nz * (this.tubeRadius - dieSize - 0.1);

            die.bounces++;
          }

          // Collision with tube top (prevent dice from flying out)
          if (die.position.y > this.tubeHeight - 2) {
            die.position.y = this.tubeHeight - 2;
            die.velocity.y = -Math.abs(die.velocity.y) * 0.5;
          }
        }
      });

      // Then handle dice-to-dice collisions
      if (this.dice.length > 1) {
        for (let i = 0; i < this.dice.length; i++) {
          const die1 = this.dice[i];
          if (die1.settled) continue;

          for (let j = i + 1; j < this.dice.length; j++) {
            const die2 = this.dice[j];
            if (die2.settled) continue;

            // Calculate distance between dice centers
            const dx = die2.position.x - die1.position.x;
            const dy = die2.position.y - die1.position.y;
            const dz = die2.position.z - die1.position.z;
            const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);

            // Determine collision based on dice type
            const die1Size = this.numberOfEdges === 6 ? 1.0 : 0.8;
            const die2Size = this.numberOfEdges === 6 ? 1.0 : 0.8;
            const minDistance = die1Size + die2Size;

            // Check for collision
            if (distance < minDistance) {
              // Calculate collision normal
              const nx = dx / distance;
              const ny = dy / distance;
              const nz = dz / distance;

              // Calculate relative velocity
              const vx = die2.velocity.x - die1.velocity.x;
              const vy = die2.velocity.y - die1.velocity.y;
              const vz = die2.velocity.z - die1.velocity.z;

              // Calculate relative velocity along normal
              const relativeVelocity = vx * nx + vy * ny + vz * nz;

              // Only resolve if dice are moving toward each other
              if (relativeVelocity < 0) {
                // Calculate impulse scalar
                const restitution = 0.7; // Bounciness
                const impulseScalar = -(1 + restitution) * relativeVelocity;

                // Apply impulse to both dice
                die1.velocity.x -= impulseScalar * nx * 0.5;
                die1.velocity.y -= impulseScalar * ny * 0.5;
                die1.velocity.z -= impulseScalar * nz * 0.5;

                die2.velocity.x += impulseScalar * nx * 0.5;
                die2.velocity.y += impulseScalar * ny * 0.5;
                die2.velocity.z += impulseScalar * nz * 0.5;

                // Add some random angular velocity for realistic collision
                die1.angularVelocity.x += (Math.random() - 0.5) * 0.2;
                die1.angularVelocity.y += (Math.random() - 0.5) * 0.2;
                die1.angularVelocity.z += (Math.random() - 0.5) * 0.2;

                die2.angularVelocity.x += (Math.random() - 0.5) * 0.2;
                die2.angularVelocity.y += (Math.random() - 0.5) * 0.2;
                die2.angularVelocity.z += (Math.random() - 0.5) * 0.2;

                // Move dice apart to prevent sticking
                const penetrationDepth = minDistance - distance;
                const percent = 0.2; // Penetration resolution percentage
                const separationX = nx * penetrationDepth * percent;
                const separationY = ny * penetrationDepth * percent;
                const separationZ = nz * penetrationDepth * percent;

                die1.position.x -= separationX;
                die1.position.y -= separationY;
                die1.position.z -= separationZ;

                die2.position.x += separationX;
                die2.position.y += separationY;
                die2.position.z += separationZ;

                // Increment bounce counter for both dice
                die1.bounces++;
                die2.bounces++;
              }
            }
          }
        }
      }

      // Check if all dice have settled
      if (allSettled && this.isRolling && !this.allDiceSettled) {
        this.allDiceSettled = true;
        this.checkResults();
      }
    },

    checkResults() {
      // Result calculation based on dice orientation or forced results
      this.results = this.dice.map((die) => {
        // If this die has a target result and we're using weighted dice, use that result
        if (die.targetResult && this.forcedResults.length > 0) {
          // Store the result on the die object for visualization
          die.resultValue = die.targetResult;

          // For d6 dice, adjust the rotation to ensure the correct face is shown
          if (this.numberOfEdges === 6) {
            this.adjustDieRotationToShowResult(die, die.targetResult);
          }

          return die.targetResult;
        }

        // Otherwise, calculate which face is up based on rotation
        const upVector = markRaw(new THREE.Vector3(0, 1, 0))
        upVector.applyQuaternion(die.quaternion)

        // Improved mapping for d6 dice
        let result
        if (this.numberOfEdges === 6) {
          // Use more precise thresholds for better face detection
          if (upVector.y > 0.7) result = 6
          else if (upVector.y < -0.7) result = 1
          else if (upVector.x > 0.7) result = 2
          else if (upVector.x < -0.7) result = 5
          else if (upVector.z > 0.7) result = 3
          else if (upVector.z < -0.7) result = 4
          else {
            // If no clear face is up, use the one closest to being up
            const absY = Math.abs(upVector.y);
            const absX = Math.abs(upVector.x);
            const absZ = Math.abs(upVector.z);

            if (absY >= absX && absY >= absZ) {
              result = upVector.y > 0 ? 6 : 1;
            } else if (absX >= absY && absX >= absZ) {
              result = upVector.x > 0 ? 2 : 5;
            } else {
              result = upVector.z > 0 ? 3 : 4;
            }
          }
        } else if (this.numberOfEdges === 4) {
          // For tetrahedron (d4), use a simplified approach
          // In a real implementation, you'd want to check which face is pointing down
          const seed = Math.floor(die.position.x * 100 + die.position.z * 100 + die.rotation.y * 100);
          result = (Math.abs(seed) % 4) + 1;
        } else {
          // For other dice, use a more deterministic approach based on final orientation
          const seed = Math.floor(
            die.position.x * 100 +
            die.position.y * 100 +
            die.position.z * 100 +
            die.rotation.x * 100 +
            die.rotation.y * 100 +
            die.rotation.z * 100
          );
          result = (Math.abs(seed) % this.numberOfEdges) + 1;
        }

        // Store the result on the die object for visualization
        die.resultValue = Math.max(1, Math.min(this.numberOfEdges, result));
        return die.resultValue;
      });

      this.totalResult = this.results.reduce((sum, result) => sum + result, 0);
      this.isRolling = false;
      this.waitingForSettling = false;

      // Show results with a sequence of camera transitions
      this.showResultsSequence();

      this.$emit('diceRolled', {
        results: this.results,
        total: this.totalResult
      });
    },

    // Helper method to adjust die rotation to show the correct result
    adjustDieRotationToShowResult(die, targetResult) {
      if (this.numberOfEdges === 6) {
        // Set rotation to ensure the target face is on top
        // For a standard six-sided die, opposite faces sum to 7
        switch(targetResult) {
          case 1: // 1 on top (negative Y)
            die.rotation.set(0, 0, 0); // Inverted from case 6
            break;
          case 6: // 6 on top (positive Y)
            die.rotation.set(Math.PI, 0, 0); // Inverted from case 1
            break;
          case 2: // 2 on top (positive X)
            die.rotation.set(0, 0, Math.PI/2); // Inverted from case 5
            break;
          case 5: // 5 on top (negative X)
            die.rotation.set(0, 0, -Math.PI/2); // Inverted from case 2
            break;
          case 3: // 3 on top (positive Z)
            die.rotation.set(-Math.PI/2, 0, 0); // Inverted from case 4
            break;
          case 4: // 4 on top (negative Z)
            die.rotation.set(Math.PI/2, 0, 0); // Inverted from case 3
            break;
        }

        // Stop all movement
        die.velocity.set(0, 0, 0);
        die.angularVelocity.set(0, 0, 0);
      }
    },

    // Show results with a sequence of camera transitions
    showResultsSequence() {
      // First show a top-down view of all dice
      this.showTopView()

      // Then after a delay, show closeup of each die
      setTimeout(() => {
        this.showCloseupView()
      }, 1500)
    },

    // Show top-down view of all dice
    showTopView() {
      // Position top camera to focus on dice
      const center = new THREE.Vector3(0, 0, 0)

      // Calculate center of all dice
      if (this.dice.length > 0) {
        this.dice.forEach(die => {
          center.add(die.position)
        })
        center.divideScalar(this.dice.length)
      }

      // Position camera above the dice
      this.topCamera.position.set(center.x, 8, center.z)
      this.topCamera.lookAt(center)

      // Switch to top camera
      this.activeCamera = this.topCamera
      this.showingResults = false // Don't show UI overlay
    },

    // Show closeup view of dice results
    showCloseupView() {
      if (this.dice.length === 0) return;

      // Find the die with the highest result to focus on first
      let highestDie = this.dice[0];
      let highestResult = highestDie.resultValue || 1;

      this.dice.forEach(die => {
        if ((die.resultValue || 1) > highestResult) {
          highestDie = die;
          highestResult = die.resultValue || 1;
        }
      });

      // Position closeup camera to focus on the highest die
      const diePosition = highestDie.position.clone();

      // Calculate camera position for a good view of the die's top face
      const cameraOffset = new THREE.Vector3(2, 2, 2);
      this.closeupCamera.position.copy(diePosition).add(cameraOffset);
      this.closeupCamera.lookAt(diePosition);

      // Switch to closeup camera
      this.activeCamera = this.closeupCamera;

      // If there are multiple dice, cycle through them
      if (this.dice.length > 1) {
        let currentDieIndex = this.dice.indexOf(highestDie);

        const cycleDice = () => {
          currentDieIndex = (currentDieIndex + 1) % this.dice.length;
          const nextDie = this.dice[currentDieIndex];

          // Smoothly move camera to next die
          const nextPosition = nextDie.position.clone();
          const nextCameraPosition = nextPosition.clone().add(cameraOffset);

          // Animate camera movement (simple linear interpolation)
          const startPosition = this.closeupCamera.position.clone();
          const startTarget = this.closeupCamera.target || diePosition.clone();
          const steps = 30;
          let step = 0;

          const animateCamera = () => {
            step++;
            const t = step / steps;

            // Interpolate position
            this.closeupCamera.position.lerpVectors(startPosition, nextCameraPosition, t);

            // Interpolate target
            const currentTarget = new THREE.Vector3();
            currentTarget.lerpVectors(startTarget, nextPosition, t);
            this.closeupCamera.lookAt(currentTarget);

            // Store current target for next animation
            this.closeupCamera.target = currentTarget.clone();

            if (step < steps) {
              requestAnimationFrame(animateCamera);
            }
          };

          animateCamera();

          // Schedule next die if not the last one
          if (currentDieIndex < this.dice.length - 1) {
            setTimeout(cycleDice, 2000);
          }
        };

        // Start cycling after a delay
        setTimeout(cycleDice, 2000);
      }
    },

    animate() {
      this.animationId = requestAnimationFrame(this.animate)

      if (this.isRolling) {
        this.updatePhysics()
      }

      // Use the active camera for rendering
      this.renderer.render(this.scene, this.activeCamera)
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
  position: relative; /* For positioning the overlay */
  overflow: hidden; /* Keep the overlay within bounds */
}

/* Results overlay styling */
.results-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.results-content {
  background: rgba(10, 10, 30, 0.9);
  border: 2px solid #00ffff;
  border-radius: 10px;
  padding: 1.5rem;
  width: 80%;
  max-width: 300px;
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
  text-align: center;
}

.results-title {
  color: #00ffff;
  font-size: 24px;
  margin-top: 0;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 0 10px #00ffff;
}

.dice-results {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.dice-result {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  border: 2px solid #00ffff;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.dice-value {
  color: #00ffff;
  font-size: 28px;
  font-weight: bold;
  text-shadow: 0 0 8px #00ffff;
}

.total-result {
  color: #ff00ff;
  font-size: 18px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(0, 255, 255, 0.3);
}

.total-value {
  color: #00ffff;
  font-size: 24px;
  text-shadow: 0 0 8px #00ffff;
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