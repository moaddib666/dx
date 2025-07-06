import * as THREE from 'three'

class DiceRenderer {
    constructor(canvas, container) {
        this.canvas = canvas
        this.container = container
        this.scene = null
        this.camera = null
        this.renderer = null
        this.dice = []
        this.animationId = null
        this.isRolling = false

        // Dice geometries cache
        this.geometries = {}
        this.materials = {}

        // Animation parameters
        this.rollDuration = 2000 // 2 seconds
        this.rollStartTime = 0
    }

    initialize() {
        this.setupScene()
        this.setupCamera()
        this.setupRenderer()
        this.setupLighting()
        this.setupGeometries()
        this.setupMaterials()
        this.animate()
    }

    setupScene() {
        this.scene = new THREE.Scene()
        this.scene.background = null

        // Add some atmospheric fog
        // this.scene.fog = new THREE.Fog(0x0f0f23, 10, 50)
    }

    setupCamera() {
        const aspect = this.container.clientWidth / this.container.clientHeight
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000)
        this.camera.position.set(0, 5, 10)
        this.camera.lookAt(0, 0, 0)
    }

    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: true
        })
        this.renderer.setClearColor(0x000000, 0);
        this.renderer.autoClear = false;
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight)
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
        this.renderer.shadowMap.enabled = true
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping
        this.renderer.toneMappingExposure = 1.2
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4)
        this.scene.add(ambientLight)

        // Main directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
        directionalLight.position.set(10, 10, 5)
        directionalLight.castShadow = true
        directionalLight.shadow.mapSize.width = 2048
        directionalLight.shadow.mapSize.height = 2048
        directionalLight.shadow.camera.near = 0.5
        directionalLight.shadow.camera.far = 50
        this.scene.add(directionalLight)

        // Point lights for dramatic effect
        const pointLight1 = new THREE.PointLight(0x4ecdc4, 0.5, 20)
        pointLight1.position.set(-5, 3, 5)
        this.scene.add(pointLight1)

        const pointLight2 = new THREE.PointLight(0xff6b6b, 0.5, 20)
        pointLight2.position.set(5, 3, -5)
        this.scene.add(pointLight2)
    }

    setupGeometries() {
        // D4 - Tetrahedron
        this.geometries.d4 = new THREE.TetrahedronGeometry(1, 0)

        // D6 - Cube
        this.geometries.d6 = new THREE.BoxGeometry(1.5, 1.5, 1.5)

        // D8 - Octahedron
        this.geometries.d8 = new THREE.OctahedronGeometry(1.2, 0)

        // D10 - Pentagonal Trapezohedron (approximated with cylinder)
        this.geometries.d10 = new THREE.ConeGeometry(1, 2, 10)

        // D12 - Dodecahedron
        this.geometries.d12 = new THREE.DodecahedronGeometry(1, 0)

        // D20 - Icosahedron
        this.geometries.d20 = new THREE.IcosahedronGeometry(1.3, 0)

        // D100 - Sphere (representing percentile die)
        this.geometries.d100 = new THREE.SphereGeometry(1.2, 32, 16)
    }

    setupMaterials() {
        const textureLoader = new THREE.TextureLoader()

        // Create materials for each die type
        const diceTypes = [
            { type: 'd4', color: 0xff6b6b },
            { type: 'd6', color: 0x4ecdc4 },
            { type: 'd8', color: 0x45b7d1 },
            { type: 'd10', color: 0x96ceb4 },
            { type: 'd12', color: 0xfeca57 },
            { type: 'd20', color: 0xff9ff3 },
            { type: 'd100', color: 0xa8e6cf }
        ]

        diceTypes.forEach(({ type, color }) => {
            // Create material with shader for glowing effect
            this.materials[type] = new THREE.ShaderMaterial({
                uniforms: {
                    baseColor: { value: new THREE.Color(color) },
                    glowIntensity: { value: 0.0 },
                    time: { value: 0.0 },
                    isRolling: { value: 0.0 }
                },
                vertexShader: this.getVertexShader(),
                fragmentShader: this.getFragmentShader(),
                transparent: true
            })
        })
    }

    getVertexShader() {
        return `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      uniform float time;
      uniform float isRolling;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = position;
        vUv = uv;
        
        vec3 pos = position;
        
        // Add subtle wobble during rolling
        if (isRolling > 0.5) {
          pos += normal * sin(time * 10.0) * 0.02;
        }
        
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `
    }

    getFragmentShader() {
        return `
      uniform vec3 baseColor;
      uniform float glowIntensity;
      uniform float time;
      uniform float isRolling;
      
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      
      void main() {
        vec3 color = baseColor;
        
        // Fresnel effect for edge highlighting
        float fresnel = 1.0 - dot(vNormal, vec3(0.0, 0.0, 1.0));
        fresnel = pow(fresnel, 2.0);
        
        // Add glow effect
        color += fresnel * glowIntensity * vec3(1.0, 1.0, 1.0);
        
        // Add rolling shimmer effect
        if (isRolling > 0.5) {
          float shimmer = sin(vPosition.x * 5.0 + time * 8.0) * 0.1;
          color += shimmer * vec3(1.0, 1.0, 1.0);
        }
        
        // Add numbers (simplified - in real implementation would use texture)
        float numberGlow = 0.0;
        if (glowIntensity > 0.1) {
          // Simulate number highlighting
          vec2 center = vec2(0.5, 0.5);
          float dist = distance(vUv, center);
          if (dist < 0.2) {
            numberGlow = (0.2 - dist) * 2.0;
          }
        }
        
        color += numberGlow * vec3(1.0, 1.0, 0.0);
        
        gl_FragColor = vec4(color, 1.0);
      }
    `
    }

    addDie(dieData) {
        const geometry = this.geometries[dieData.type]
        const material = this.materials[dieData.type].clone()

        if (!geometry || !material) {
            console.error(`Unknown die type: ${dieData.type}`)
            return
        }

        const mesh = new THREE.Mesh(geometry, material)

        // Position dice in a row
        const spacing = 3
        const startX = -(this.dice.length * spacing) / 2
        mesh.position.set(startX + this.dice.length * spacing, 2, 0)

        // Set initial rotation to show max face
        this.setMaxFaceRotation(mesh, dieData.type, dieData.sides)

        mesh.castShadow = true
        mesh.receiveShadow = true

        // Store die data
        mesh.userData = {
            ...dieData,
            initialPosition: mesh.position.clone(),
            initialRotation: mesh.rotation.clone(),
            rollData: {
                startPosition: mesh.position.clone(),
                startRotation: mesh.rotation.clone(),
                targetPosition: mesh.position.clone(),
                targetRotation: mesh.rotation.clone(),
                velocity: new THREE.Vector3(),
                angularVelocity: new THREE.Euler()
            }
        }

        this.scene.add(mesh)
        this.dice.push(mesh)

        // Add entrance animation
        this.animateDiceEntrance(mesh)
    }

    setMaxFaceRotation(mesh, dieType, sides) {
        // Set rotation to show maximum value face towards camera
        switch (dieType) {
            case 'd4':
                mesh.rotation.set(0, 0, 0)
                break
            case 'd6':
                mesh.rotation.set(0, 0, 0) // Face with 6 towards camera
                break
            case 'd8':
                mesh.rotation.set(Math.PI / 4, Math.PI / 4, 0)
                break
            case 'd10':
                mesh.rotation.set(0, 0, 0)
                break
            case 'd12':
                mesh.rotation.set(0, Math.PI / 5, 0)
                break
            case 'd20':
                mesh.rotation.set(Math.PI / 3, Math.PI / 5, 0)
                break
            case 'd100':
                mesh.rotation.set(0, 0, 0)
                break
        }
    }

    animateDiceEntrance(mesh) {
        const startY = mesh.position.y + 5
        const targetY = mesh.position.y
        mesh.position.y = startY

        const startTime = Date.now()
        const duration = 500

        const animate = () => {
            const elapsed = Date.now() - startTime
            const progress = Math.min(elapsed / duration, 1)
            const eased = 1 - Math.pow(1 - progress, 3) // Ease out cubic

            mesh.position.y = startY + (targetY - startY) * eased
            mesh.rotation.y = (1 - progress) * Math.PI * 2

            if (progress < 1) {
                requestAnimationFrame(animate)
            }
        }

        animate()
    }

    removeDie(id) {
        const index = this.dice.findIndex(die => die.userData.id === id)
        if (index !== -1) {
            const die = this.dice[index]
            this.scene.remove(die)
            this.dice.splice(index, 1)

            // Reposition remaining dice
            this.repositionDice()
        }
    }

    repositionDice() {
        const spacing = 3
        const startX = -(this.dice.length * spacing) / 2

        this.dice.forEach((die, index) => {
            const targetX = startX + index * spacing
            const startTime = Date.now()
            const duration = 300
            const startX_pos = die.position.x

            const animate = () => {
                const elapsed = Date.now() - startTime
                const progress = Math.min(elapsed / duration, 1)
                const eased = 1 - Math.pow(1 - progress, 2) // Ease out

                die.position.x = startX_pos + (targetX - startX_pos) * eased

                if (progress < 1) {
                    requestAnimationFrame(animate)
                }
            }

            animate()
        })
    }

    clearDice() {
        this.dice.forEach(die => {
            this.scene.remove(die)
        })
        this.dice = []
    }

    async rollDice() {
        if (this.isRolling || this.dice.length === 0) return

        this.isRolling = true
        this.rollStartTime = Date.now()

        // Set rolling state for shaders
        this.dice.forEach(die => {
            die.material.uniforms.isRolling.value = 1.0
            die.material.uniforms.glowIntensity.value = 0.0

            // Set random angular velocities
            const rollData = die.userData.rollData
            rollData.angularVelocity.set(
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 20
            )

            // Add some random movement
            rollData.velocity.set(
                (Math.random() - 0.5) * 2,
                Math.random() * 3 + 1,
                (Math.random() - 0.5) * 2
            )
        })

        // Wait for roll animation to complete
        return new Promise(resolve => {
            setTimeout(() => {
                this.stopRolling()
                resolve()
            }, this.rollDuration)
        })
    }

    stopRolling() {
        this.isRolling = false

        this.dice.forEach(die => {
            die.material.uniforms.isRolling.value = 0.0

            // Return to original position and rotation
            die.position.copy(die.userData.initialPosition)
            die.rotation.copy(die.userData.initialRotation)

            // Reset roll data
            const rollData = die.userData.rollData
            rollData.velocity.set(0, 0, 0)
            rollData.angularVelocity.set(0, 0, 0)
        })
    }

    showResults(results) {
        results.forEach((result, index) => {
            if (index < this.dice.length) {
                const die = this.dice[index]

                // Update die data
                die.userData.result = result.result

                // Set glow effect for result
                die.material.uniforms.glowIntensity.value = 1.0

                // Set rotation to show result face
                this.setResultFaceRotation(die, result.type, result.result)

                // Animate result highlighting
                this.animateResultHighlight(die)
            }
        })
    }

    setResultFaceRotation(mesh, dieType, result) {
        // This is simplified - in a real implementation, you'd calculate
        // the exact rotation needed to show the specific number face
        const rotations = {
            'd4': [
                [0, 0, 0], [Math.PI/3, 0, 0], [0, Math.PI/3, 0], [Math.PI/3, Math.PI/3, 0]
            ],
            'd6': [
                [0, 0, 0], [Math.PI/2, 0, 0], [0, Math.PI/2, 0],
                [0, -Math.PI/2, 0], [-Math.PI/2, 0, 0], [Math.PI, 0, 0]
            ],
            'd8': [
                [0, 0, 0], [Math.PI/4, 0, 0], [0, Math.PI/4, 0], [Math.PI/4, Math.PI/4, 0],
                [-Math.PI/4, 0, 0], [0, -Math.PI/4, 0], [-Math.PI/4, -Math.PI/4, 0], [Math.PI/2, Math.PI/4, 0]
            ],
            'd10': Array.from({length: 10}, (_, i) => [0, (i * Math.PI * 2) / 10, 0]),
            'd12': Array.from({length: 12}, (_, i) => [
                Math.sin(i * Math.PI / 6) * Math.PI / 3,
                (i * Math.PI * 2) / 12,
                0
            ]),
            'd20': Array.from({length: 20}, (_, i) => [
                Math.sin(i * Math.PI / 10) * Math.PI / 3,
                (i * Math.PI * 2) / 20,
                Math.cos(i * Math.PI / 10) * Math.PI / 6
            ]),
            'd100': [[0, 0, 0]] // Single face for percentage
        }

        const typeRotations = rotations[dieType]
        if (typeRotations && typeRotations[result - 1]) {
            const [x, y, z] = typeRotations[result - 1]
            mesh.rotation.set(x, y, z)
        }
    }

    animateResultHighlight(die) {
        const startTime = Date.now()
        const duration = 1000

        const animate = () => {
            const elapsed = Date.now() - startTime
            const progress = elapsed / duration

            // Pulsing glow effect
            const glow = 0.5 + 0.5 * Math.sin(progress * Math.PI * 4)
            die.material.uniforms.glowIntensity.value = glow

            if (progress < 1) {
                requestAnimationFrame(animate)
            } else {
                die.material.uniforms.glowIntensity.value = 0.8 // Final glow
            }
        }

        animate()
    }

    animate() {
        this.animationId = requestAnimationFrame(() => this.animate())

        const time = Date.now() * 0.001

        // Update shader uniforms
        this.dice.forEach(die => {
            die.material.uniforms.time.value = time

            if (this.isRolling) {
                // Apply physics during rolling
                const rollData = die.userData.rollData

                // Apply velocity
                die.position.add(rollData.velocity.clone().multiplyScalar(0.016))

                // Apply angular velocity
                die.rotation.x += rollData.angularVelocity.x * 0.016
                die.rotation.y += rollData.angularVelocity.y * 0.016
                die.rotation.z += rollData.angularVelocity.z * 0.016

                // Apply gravity and dampening
                rollData.velocity.y -= 9.8 * 0.016
                rollData.velocity.multiplyScalar(0.98)
                rollData.angularVelocity.x *= 0.98
                rollData.angularVelocity.y *= 0.98
                rollData.angularVelocity.z *= 0.98

                // Bounce off ground
                if (die.position.y < 0.5) {
                    die.position.y = 0.5
                    rollData.velocity.y = Math.abs(rollData.velocity.y) * 0.6
                }
            }
        })

        this.renderer.render(this.scene, this.camera)
    }

    handleResize() {
        if (!this.camera || !this.renderer) return

        const width = this.container.clientWidth
        const height = this.container.clientHeight

        this.camera.aspect = width / height
        this.camera.updateProjectionMatrix()
        this.renderer.setSize(width, height)
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId)
        }

        // Clean up Three.js objects
        this.clearDice()

        if (this.renderer) {
            this.renderer.dispose()
        }

        // Clean up geometries and materials
        Object.values(this.geometries).forEach(geometry => geometry.dispose())
        Object.values(this.materials).forEach(material => material.dispose())

        this.scene = null
        this.camera = null
        this.renderer = null
    }
}

export default DiceRenderer