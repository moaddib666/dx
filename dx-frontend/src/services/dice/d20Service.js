import * as THREE from 'three'
import { markRaw } from 'vue'

export class D20Service {
    constructor() {
        this.scene = null
        this.camera = null
        this.renderer = null
        this.dice = null
        this.userTextureImg = null
        this.isInitialized = false
        
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
            this.scene.background = new THREE.Color(0x1a1a1a)

            // Camera setup - start with top view
            this.camera = markRaw(new THREE.PerspectiveCamera(75, width / height, 0.1, 1000))
            this.camera.position.set(0, 12, 0)
            this.camera.lookAt(0, 0, 0)

            // Renderer setup
            this.renderer = markRaw(new THREE.WebGLRenderer({ canvas, antialias: true }))
            this.renderer.setSize(width, height)
            this.renderer.shadowMap.enabled = true
            this.renderer.shadowMap.type = THREE.PCFSoftShadowMap

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
        // Brighter ambient light
        const ambientLight = new THREE.AmbientLight(0x606060, 0.6)
        this.scene.add(ambientLight)

        // Main directional light (stronger)
        const dirLight = new THREE.DirectionalLight(0xffffff, 1.5)
        dirLight.position.set(5, 15, 5)
        dirLight.castShadow = true
        dirLight.shadow.mapSize.width = 2048
        dirLight.shadow.mapSize.height = 2048
        dirLight.shadow.camera.near = 0.1
        dirLight.shadow.camera.far = 50
        dirLight.shadow.camera.left = -10
        dirLight.shadow.camera.right = 10
        dirLight.shadow.camera.top = 10
        dirLight.shadow.camera.bottom = -10
        this.scene.add(dirLight)

        // Add fill lights for better visibility
        const fillLight1 = new THREE.DirectionalLight(0xffffff, 0.3)
        fillLight1.position.set(-5, 10, -5)
        this.scene.add(fillLight1)

        const fillLight2 = new THREE.DirectionalLight(0xffffff, 0.2)
        fillLight2.position.set(0, 5, 10)
        this.scene.add(fillLight2)

        // Top light for better visibility from above
        const topLight = new THREE.DirectionalLight(0xffffff, 0.4)
        topLight.position.set(0, 20, 0)
        this.scene.add(topLight)
    }

    createSurface() {
        const surface = new THREE.Mesh(
            new THREE.PlaneGeometry(20, 20),
            new THREE.MeshPhongMaterial({ 
                color: 0x444444, 
                transparent: true, 
                opacity: 0.8 
            })
        )
        surface.rotation.x = -Math.PI / 2
        surface.position.y = -0.1
        surface.receiveShadow = true
        this.scene.add(surface)
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
            
            // UVs
            uvs.push(0.1, 0.2, 0.9, 0.2, 0.5, 0.85)

            // Create texture for this face
            const texture = this.createNumberTexture(
                this.faceNumbers[faceIndex],
                "#4444ff",
                "#fff",
                faceIndex === highlightFace
            )
            
            materials.push(
                new THREE.MeshPhongMaterial({ 
                    map: texture, 
                    transparent: true, 
                    opacity: 0.95, 
                    shininess: 100 
                })
            )
            
            groups.push({ start: faceIndex * 3, count: 3, materialIndex: faceIndex })
        })

        geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3))
        geometry.setAttribute("normal", new THREE.Float32BufferAttribute(normals, 3))
        geometry.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2))
        groups.forEach((g) => geometry.addGroup(g.start, g.count, g.materialIndex))

        return markRaw(new THREE.Mesh(geometry, materials))
    }

    calculateTargetRotation(faceIndex) {
        const quaternion = new THREE.Quaternion().setFromUnitVectors(
            this.faceNormals[faceIndex].clone(),
            new THREE.Vector3(0, 1, 0)
        )
        const euler = new THREE.Euler().setFromQuaternion(quaternion)
        return new THREE.Vector3(euler.x, euler.y, euler.z)
    }

    createDice(highlightFace = -1) {
        if (this.dice) {
            this.scene.remove(this.dice)
            this.dice.geometry.dispose()
            this.dice.material.forEach((m) => m.dispose())
        }

        this.dice = this.buildD20Mesh(highlightFace)
        this.dice.castShadow = this.dice.receiveShadow = true
        this.dice.position.set(0, 1, 0)
        this.scene.add(this.dice)
        
        return this.dice
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
        if (this.dice && this.dice.material) {
            const isWireframe = this.dice.material[0].wireframe
            this.dice.material.forEach((material) => {
                material.wireframe = !isWireframe
            })
            return !isWireframe
        }
        return false
    }

    updateDiceRotation(rotation) {
        if (this.dice) {
            this.dice.rotation.set(rotation.x, rotation.y, rotation.z)
        }
    }

    updateDicePosition(position) {
        if (this.dice) {
            this.dice.position.copy(position)
        }
    }

    render() {
        if (this.renderer && this.scene && this.camera) {
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

    findTopFace() {
        if (!this.dice) return 1

        let bestIndex = 0
        let maxY = -Infinity

        this.faces.forEach((face, index) => {
            const normal = this.faceNormals[index].clone()
            normal.applyMatrix3(new THREE.Matrix3().getNormalMatrix(this.dice.matrixWorld))
            if (normal.y > maxY) {
                maxY = normal.y
                bestIndex = index
            }
        })

        return this.faceNumbers[bestIndex]
    }

    dispose() {
        if (this.dice) {
            this.scene.remove(this.dice)
            this.dice.geometry.dispose()
            this.dice.material.forEach((m) => m.dispose())
        }
        
        if (this.renderer) {
            this.renderer.dispose()
        }
        
        this.scene = null
        this.camera = null
        this.renderer = null
        this.dice = null
        this.isInitialized = false
    }
}

export default D20Service