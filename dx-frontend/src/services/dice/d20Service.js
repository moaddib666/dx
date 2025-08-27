import * as THREE from 'three'
import { markRaw } from 'vue'
import D20MaterialService from './d20MaterialService.js'

export class D20Service {
    constructor() {
        this.scene = null
        this.camera = null
        this.renderer = null
        this.dice = null
        this.diceArray = [] // Array to hold multiple dice
        this.diceCount = 1
        this.userTextureImg = null
        this.isInitialized = false
        this.materialService = markRaw(new D20MaterialService())

        // D20 geometry data
        this.t = (1 + Math.sqrt(5)) / 2
        this.vertices = [
            [-1, this.t, 0], [1, this.t, 0], [-1, -this.t, 0], [1, -this.t, 0],
            [0, -1, this.t], [0, 1, this.t], [0, -1, -this.t], [0, 1, -this.t],
            [this.t, 0, -1], [this.t, 0, 1], [-this.t, 0, -1], [-this.t, 0, 1]
        ]

        this.faces = [
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
        ]

        this.faceNumbers = Array.from({ length: 20 }, (_, i) => i + 1)
        this.faceNormals = this.calculateFaceNormals()
    }

    calculateFaceNormals() {
        return this.faces.map((f) => {
            const [a, b, c] = f.map((i) => new THREE.Vector3(...this.vertices[i]))
            return new THREE.Vector3()
                .crossVectors(b.clone().sub(a), c.clone().sub(a))
                .normalize()
        })
    }

    async initializeScene(canvas, width, height) {
        try {
            // Scene setup
            this.scene = markRaw(new THREE.Scene())

            // Camera setup - direct top-down view for clear dice face visibility
            this.camera = markRaw(new THREE.PerspectiveCamera(50, width / height, 2, 8))
            this.camera.position.set(0, 6, 0)
            this.camera.lookAt(0, 0, 0)

            // Renderer setup - exact same as dice6.html
            this.renderer = markRaw(new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true }))
            this.renderer.setSize(width, height)
            this.renderer.shadowMap.enabled = true
            this.renderer.shadowMap.type = THREE.PCFSoftShadowMap

            // Ensure proper color output
            this.renderer.outputColorSpace = THREE.SRGBColorSpace
            this.renderer.toneMapping = THREE.LinearToneMapping
            this.renderer.toneMappingExposure = 1.0

            // Initialize material service shaders
            this.materialService.initializeShaders()

            // Setup lighting
            this.setupLighting()

            // Create surface
            this.createSurface()

            this.isInitialized = true
            return true
        } catch (error) {
            console.error('Failed to initialize D20 scene:', error)
            return false
        }
    }

    setupLighting() {
        // Ambient light for basic illumination
        // this.scene.add(new THREE.AmbientLight(0x404040, 40.5))
        this.scene.add(new THREE.AmbientLight(0xffffff, 2.5))

        // Main directional light for strong reflections
        // const dirLight = new THREE.DirectionalLight(0xffffff, 0.2)
        // dirLight.position.set(15, 20, 20)
        // dirLight.castShadow = true
        // dirLight.shadow.mapSize.width = 2048
        // dirLight.shadow.mapSize.height = 2048
        // this.scene.add(dirLight)

        // // Additional lights for metallic reflections
        // const fillLight1 = new THREE.DirectionalLight(0xffffff, 1.6)
        // fillLight1.position.set(-10, 15, -10)
        // this.scene.add(fillLight1)
        //
        // const fillLight2 = new THREE.DirectionalLight(0xffffff, 1.4)
        // fillLight2.position.set(10, 8, 10)
        // this.scene.add(fillLight2)

        // Top light for better visibility
        // const topLight = new THREE.DirectionalLight(0xffffff, 1.3)
        // topLight.position.set(0.1, 1, 0.1)
        // this.scene.add(topLight)

        const rearLight = new THREE.SpotLight(0xffffff, 105)
        rearLight.position.set(0, 4.5, 0)
        rearLight.castShadow = false
        rearLight.penumbra = 0.3
        this.scene.add(rearLight)

        // let a = "#ffcc00"
        const orange = 0xFFCC00
        const cyan = 0x00ffff
        // Background Right Orange Light
        const rightLight = new THREE.DirectionalLight(orange, 15.5)
        rightLight.position.set(15, 1, -3)
        rightLight.castShadow = false
        this.scene.add(rightLight)
        // Background Left Cyan Light
        const leftLight = new THREE.DirectionalLight(cyan, 15.5)
        leftLight.position.set(-15, 1, 3)
        this.scene.add(leftLight)

    }

    createSurface() {
        // Non required, use transparent surface
    }

    setUserTexture(imageFile) {
        return new Promise((resolve) => {
            if (!imageFile) {
                this.userTextureImg = null
                resolve(true)
                return
            }

            const reader = new FileReader()
            reader.onload = (event) => {
                const img = new Image()
                img.onload = () => {
                    console.log('Custom texture loaded successfully:', img.width, 'x', img.height)
                    this.userTextureImg = img
                    resolve(true)
                }
                img.onerror = (error) => {
                    console.error('Failed to load custom texture:', error)
                    resolve(false)
                }
                // Set crossOrigin before src for CORS issues
                img.crossOrigin = 'anonymous'
                img.src = event.target.result
            }
            reader.onerror = (error) => {
                console.error('Failed to read file:', error)
                resolve(false)
            }
            reader.readAsDataURL(imageFile)
        })
    }

    createNumberTexture(num, base = "#4444ff", text = "#fff", highlight = false) {
        const canvas = document.createElement("canvas")
        canvas.width = canvas.height = 512
        const ctx = canvas.getContext("2d")

        // Background
        if (this.userTextureImg) {
            ctx.drawImage(this.userTextureImg, 0, 0, 512, 512)
            ctx.fillStyle = "rgba(0,0,0,.25)"
            ctx.fillRect(0, 0, 512, 512)
        } else {
            const gradient = ctx.createRadialGradient(256, 256, 0, 256, 256, 256)
            gradient.addColorStop(0, base)
            gradient.addColorStop(1, "#333366")
            ctx.fillStyle = gradient
            ctx.fillRect(0, 0, 512, 512)
        }

        // Number styling
        ctx.shadowColor = "rgba(0,0,0,.7)"
        ctx.shadowBlur = 8
        ctx.shadowOffsetX = ctx.shadowOffsetY = 3

        if (num <= 1) {
            ctx.fillStyle = highlight ? "#ff0505" : text
        } else if (num < 20) {
            ctx.fillStyle = highlight ? "#16eaff" : text
        } else {
            ctx.fillStyle = highlight ? "#ff0" : text
        }

        ctx.font = "bold 140px Arial"
        ctx.textAlign = "center"
        ctx.textBaseline = "middle"
        ctx.fillText(num.toString(), 256, 296)

        return new THREE.CanvasTexture(canvas)
    }

    buildD20Mesh(highlightFace = -1) {
        const geometry = new THREE.BufferGeometry()
        const positions = []
        const normals = []
        const uvs = []
        const groups = []
        const materials = []

        this.faces.forEach((face, faceIndex) => {
            const [v1, v2, v3] = face.map((idx) => new THREE.Vector3(...this.vertices[idx]))

            // Positions
            positions.push(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, v3.x, v3.y, v3.z)

            // Normals
            const normal = new THREE.Vector3()
                .crossVectors(v2.clone().sub(v1), v3.clone().sub(v1))
                .normalize()
            normals.push(normal.x, normal.y, normal.z, normal.x, normal.y, normal.z, normal.x, normal.y, normal.z)

            // UVs - simple uniform mapping that preserves text readability
            uvs.push(0.1, 0.2, 0.9, 0.2, 0.5, 0.85)

            // Create texture for this face
            const texture = this.createNumberTexture(
                this.faceNumbers[faceIndex],
                "#4444ff",
                "#fff",
                faceIndex === highlightFace
            )

            // Use material service to create material
            const material = this.materialService.createMaterial(
                this.materialService.getCurrentMaterialType(),
                texture,
                this.materialService.getCurrentShaderType()
            )

            materials.push(material)
            groups.push({ start: faceIndex * 3, count: 3, materialIndex: faceIndex })
        })

        geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3))
        geometry.setAttribute("normal", new THREE.Float32BufferAttribute(normals, 3))
        geometry.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2))
        groups.forEach((g) => geometry.addGroup(g.start, g.count, g.materialIndex))

        return markRaw(new THREE.Mesh(geometry, materials))
    }

    calculateTargetRotation(faceIndex) {
        // Align face normal toward camera (upward)
        // Face 3 displays perfectly as the reference for proper triangle orientation
        const quaternion = new THREE.Quaternion().setFromUnitVectors(
            this.faceNormals[faceIndex].clone(),
            new THREE.Vector3(0, 1, 0)  // Point upward toward camera
        )
        const euler = new THREE.Euler().setFromQuaternion(quaternion)
        return new THREE.Vector3(euler.x, euler.y, euler.z)
    }

    createDice(highlightFace = -1) {
        // Clean up existing dice
        this.clearAllDice()

        if (this.diceCount === 1) {
            // Single dice mode - original behavior
            this.dice = this.buildD20Mesh(highlightFace)
            this.dice.castShadow = this.dice.receiveShadow = true
            this.dice.position.set(0, 1, 0)
            this.scene.add(this.dice)
            this.diceArray = [this.dice]
        } else {
            // Multiple dice mode
            this.createMultipleDice(this.diceCount, highlightFace)
        }

        return this.diceArray
    }

    createDiceWithIndividualHighlights(highlightFaces = [], preserveRotations = true) {
        // Store current rotations before clearing dice
        const currentRotations = []
        if (preserveRotations && this.diceArray.length > 0) {
            this.diceArray.forEach(dice => {
                if (dice) {
                    currentRotations.push({
                        x: dice.rotation.x,
                        y: dice.rotation.y,
                        z: dice.rotation.z
                    })
                }
            })
        }

        // Clean up existing dice
        this.clearAllDice()

        if (this.diceCount === 1) {
            // Single dice mode - convert face number to face index
            const highlight = Array.isArray(highlightFaces) ? highlightFaces[0] : highlightFaces
            const faceIndex = (highlight !== undefined && highlight !== -1)
                ? this.faceNumbers.indexOf(highlight)
                : -1
            this.dice = this.buildD20Mesh(faceIndex)
            this.dice.castShadow = this.dice.receiveShadow = true
            this.dice.position.set(0, 1, 0)

            // Restore rotation if available
            if (currentRotations.length > 0) {
                const rot = currentRotations[0]
                this.dice.rotation.set(rot.x, rot.y, rot.z)
            }

            this.scene.add(this.dice)
            this.diceArray = [this.dice]
        } else {
            // Multiple dice mode with individual highlights
            this.createMultipleDiceWithHighlights(this.diceCount, highlightFaces, currentRotations)
        }

        return this.diceArray
    }

    createMultipleDice(count, highlightFace = -1) {
        this.diceCount = count
        this.clearAllDice()

        const spacing = 3.5 // Distance between dice
        // Center the dice around origin point (0,0,0)
        const totalWidth = (count - 1) * spacing
        const startOffset = -totalWidth / 2

        for (let i = 0; i < count; i++) {
            const diceObject = this.buildD20Mesh(highlightFace)
            diceObject.castShadow = diceObject.receiveShadow = true

            // Position dice centered around origin
            const xOffset = startOffset + (i * spacing)
            diceObject.position.set(xOffset, 1, 0)

            this.scene.add(diceObject)
            this.diceArray.push(diceObject)
        }

        // Keep reference to first dice for backward compatibility
        this.dice = this.diceArray[0]

        return this.diceArray
    }

    createMultipleDiceWithHighlights(count, highlightFaces = [], preservedRotations = []) {
        this.diceCount = count
        this.clearAllDice()

        const spacing = 3.5 // Distance between dice
        // Center the dice around origin point (0,0,0)
        const totalWidth = (count - 1) * spacing
        const startOffset = -totalWidth / 2

        for (let i = 0; i < count; i++) {
            // Get highlight face for this specific dice
            const highlightFace = Array.isArray(highlightFaces) ? highlightFaces[i] : highlightFaces
            const faceIndex = (highlightFace !== undefined && highlightFace !== -1)
                ? this.faceNumbers.indexOf(highlightFace)
                : -1

            const diceObject = this.buildD20Mesh(faceIndex)
            diceObject.castShadow = diceObject.receiveShadow = true

            // Position dice centered around origin
            const xOffset = startOffset + (i * spacing)
            diceObject.position.set(xOffset, 1, 0)

            // Restore rotation if available
            if (preservedRotations.length > i) {
                const rot = preservedRotations[i]
                diceObject.rotation.set(rot.x, rot.y, rot.z)
            }

            this.scene.add(diceObject)
            this.diceArray.push(diceObject)
        }

        // Keep reference to first dice for backward compatibility
        this.dice = this.diceArray[0]

        return this.diceArray
    }

    clearAllDice() {
        // Clean up existing dice array
        this.diceArray.forEach(diceObj => {
            if (diceObj) {
                this.scene.remove(diceObj)
                diceObj.geometry.dispose()
                diceObj.material.forEach((m) => m.dispose())
            }
        })
        this.diceArray = []

        // Clean up single dice reference
        if (this.dice) {
            this.scene.remove(this.dice)
            this.dice.geometry.dispose()
            this.dice.material.forEach((m) => m.dispose())
            this.dice = null
        }
    }

    setCameraView(viewType) {
        switch (viewType) {
            case 'top':
                this.camera.position.set(0, 12, 0)
                this.camera.lookAt(0, 0, 0)
                break
            case 'side':
                this.camera.position.set(12, 2, 0)
                this.camera.lookAt(0, 1, 0)
                break
            case 'angle':
            default:
                this.camera.position.set(8, 6, 8)
                this.camera.lookAt(0, 0, 0)
                break
        }
    }

    toggleWireframe() {
        if (this.diceArray.length > 0) {
            const isWireframe = this.diceArray[0].material[0].wireframe
            this.diceArray.forEach(diceObj => {
                if (diceObj && diceObj.material) {
                    diceObj.material.forEach((material) => {
                        material.wireframe = !isWireframe
                    })
                }
            })
            return !isWireframe
        }
        return false
    }

    updateDiceRotation(rotation, diceIndex = 0) {
        if (this.diceArray[diceIndex]) {
            this.diceArray[diceIndex].rotation.set(rotation.x, rotation.y, rotation.z)
        }
        // Update first dice for backward compatibility
        if (diceIndex === 0 && this.dice) {
            this.dice.rotation.set(rotation.x, rotation.y, rotation.z)
        }
    }

    updateDicePosition(position, diceIndex = 0) {
        if (this.diceArray[diceIndex]) {
            if (this.diceCount === 1) {
                // Single dice - allow full position animation
                this.diceArray[diceIndex].position.copy(position)
            } else {
                // Multiple dice - keep dice at their fixed spawn positions, ignore animation position
                // Do nothing - dice stay at their spawn positions
            }
        }
        // Update first dice for backward compatibility
        if (diceIndex === 0 && this.dice) {
            this.dice.position.copy(position)
        }
    }

    getDiceOriginalPosition(diceIndex) {
        if (this.diceCount === 1) {
            return { x: 0, y: 1, z: 0 }
        }

        const spacing = 3.5
        const totalWidth = (this.diceCount - 1) * spacing
        const startOffset = -totalWidth / 2
        const xOffset = startOffset + (diceIndex * spacing)

        return { x: xOffset, y: 1, z: 0 }
    }

    updateAllDiceRotation(rotations) {
        if (Array.isArray(rotations)) {
            rotations.forEach((rotation, index) => {
                this.updateDiceRotation(rotation, index)
            })
        } else {
            // Single rotation for all dice
            this.diceArray.forEach((diceObj, index) => {
                this.updateDiceRotation(rotations, index)
            })
        }
    }

    updateAllDicePosition(positions) {
        if (Array.isArray(positions)) {
            positions.forEach((position, index) => {
                this.updateDicePosition(position, index)
            })
        } else {
            // Single position for all dice (not recommended but supported)
            this.diceArray.forEach((diceObj, index) => {
                this.updateDicePosition(positions, index)
            })
        }
    }

    render(deltaTime = 0) {
        if (this.renderer && this.scene && this.camera) {
            // Update shader uniforms
            this.materialService.updateShaderUniforms(deltaTime)
            this.renderer.render(this.scene, this.camera)
        }
    }

    resize(width, height) {
        if (this.camera && this.renderer) {
            this.camera.aspect = width / height
            this.camera.updateProjectionMatrix()
            this.renderer.setSize(width, height)
        }
    }

    findTopFace(diceIndex = 0) {
        const targetDice = this.diceArray[diceIndex] || this.dice
        if (!targetDice) return 1

        let bestIndex = 0
        let maxY = -Infinity

        this.faces.forEach((face, index) => {
            const normal = this.faceNormals[index].clone()
            normal.applyMatrix3(new THREE.Matrix3().getNormalMatrix(targetDice.matrixWorld))
            if (normal.y > maxY) {
                maxY = normal.y
                bestIndex = index
            }
        })

        return this.faceNumbers[bestIndex]
    }

    findAllTopFaces() {
        return this.diceArray.map((diceObj, index) => this.findTopFace(index))
    }

    // Material and shader control methods
    setMaterialType(materialType) {
        if (this.materialService.setMaterialType(materialType)) {
            // Recreate dice with new material
            if (this.dice) {
                this.createDice()
            }
            return true
        }
        return false
    }

    setShaderType(shaderType) {
        if (this.materialService.setShaderType(shaderType)) {
            // Recreate dice with new shader
            if (this.dice) {
                this.createDice()
            }
            return true
        }
        return false
    }

    getMaterialTypes() {
        return this.materialService.getMaterialTypes()
    }

    getShaderTypes() {
        return this.materialService.getShaderTypes()
    }

    getCurrentMaterialType() {
        return this.materialService.getCurrentMaterialType()
    }

    getCurrentShaderType() {
        return this.materialService.getCurrentShaderType()
    }

    dispose() {
        // Clean up all dice using the existing method
        this.clearAllDice()

        if (this.renderer) {
            this.renderer.dispose()
        }

        this.scene = null
        this.camera = null
        this.renderer = null
        this.dice = null
        this.diceArray = []
        this.isInitialized = false
    }
}

export default D20Service