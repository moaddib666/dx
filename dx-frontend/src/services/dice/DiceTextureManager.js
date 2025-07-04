import * as THREE from 'three'

export class DiceTextureManager {
    constructor() {
        this.textures = new Map()
        this.numberTextures = new Map()
        this.themes = new Map()
        this.currentTheme = 'default'
        this.textureLoader = new THREE.TextureLoader()
        this.canvas = document.createElement('canvas')
        this.ctx = this.canvas.getContext('2d')

        this.initializeThemes()
        this.generateDefaultTextures()
    }

    initializeThemes() {
        // Default theme
        this.themes.set('default', {
            name: 'Default',
            diceColors: {
                'd4': '#ff6b6b',
                'd6': '#4ecdc4',
                'd8': '#45b7d1',
                'd10': '#96ceb4',
                'd12': '#feca57',
                'd20': '#ff9ff3',
                'd100': '#a8e6cf'
            },
            numberColor: '#ffffff',
            numberStyle: 'modern',
            roughness: 0.3,
            metalness: 0.1,
            emissive: 0.1
        })

        // Medieval theme
        this.themes.set('medieval', {
            name: 'Medieval',
            diceColors: {
                'd4': '#8B4513',
                'd6': '#DAA520',
                'd8': '#CD853F',
                'd10': '#A0522D',
                'd12': '#B8860B',
                'd20': '#D2691E',
                'd100': '#DEB887'
            },
            numberColor: '#FFD700',
            numberStyle: 'runic',
            roughness: 0.8,
            metalness: 0.2,
            emissive: 0.05
        })

        // Cyberpunk theme
        this.themes.set('cyberpunk', {
            name: 'Cyberpunk',
            diceColors: {
                'd4': '#00ffff',
                'd6': '#ff00ff',
                'd8': '#ffff00',
                'd10': '#00ff00',
                'd12': '#ff0080',
                'd20': '#8000ff',
                'd100': '#ff8000'
            },
            numberColor: '#000000',
            numberStyle: 'digital',
            roughness: 0.1,
            metalness: 0.9,
            emissive: 0.3
        })

        // Ice theme
        this.themes.set('ice', {
            name: 'Ice Crystal',
            diceColors: {
                'd4': '#E0F6FF',
                'd6': '#B3E5FC',
                'd8': '#81D4FA',
                'd10': '#4FC3F7',
                'd12': '#29B6F6',
                'd20': '#03A9F4',
                'd100': '#0288D1'
            },
            numberColor: '#003366',
            numberStyle: 'crystal',
            roughness: 0.0,
            metalness: 0.0,
            emissive: 0.2,
            transparent: true,
            opacity: 0.8
        })

        // Fire theme
        this.themes.set('fire', {
            name: 'Flame',
            diceColors: {
                'd4': '#FF6B35',
                'd6': '#FF4500',
                'd8': '#FF2500',
                'd10': '#DC143C',
                'd12': '#B22222',
                'd20': '#8B0000',
                'd100': '#660000'
            },
            numberColor: '#FFFF00',
            numberStyle: 'flame',
            roughness: 0.4,
            metalness: 0.3,
            emissive: 0.4
        })

        // Nature theme
        this.themes.set('nature', {
            name: 'Nature',
            diceColors: {
                'd4': '#90EE90',
                'd6': '#32CD32',
                'd8': '#228B22',
                'd10': '#006400',
                'd12': '#8FBC8F',
                'd20': '#2E8B57',
                'd100': '#556B2F'
            },
            numberColor: '#FFFFFF',
            numberStyle: 'organic',
            roughness: 0.7,
            metalness: 0.0,
            emissive: 0.1
        })
    }

    generateDefaultTextures() {
        const diceTypes = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100']

        diceTypes.forEach(diceType => {
            this.generateDiceTextures(diceType)
        })
    }

    generateDiceTextures(diceType) {
        const theme = this.themes.get(this.currentTheme)
        const maxNumber = this.getMaxNumber(diceType)

        // Generate number textures for each face
        for (let i = 1; i <= maxNumber; i++) {
            const textureKey = `${diceType}_${i}_${this.currentTheme}`
            this.numberTextures.set(textureKey, this.createNumberTexture(i, theme))
        }

        // Generate base material texture
        const materialKey = `${diceType}_material_${this.currentTheme}`
        this.textures.set(materialKey, this.createMaterialTexture(diceType, theme))
    }

    createNumberTexture(number, theme, size = 512) {
        this.canvas.width = size
        this.canvas.height = size

        // Clear canvas
        this.ctx.clearRect(0, 0, size, size)

        // Set up rendering context
        this.ctx.imageSmoothingEnabled = true
        this.ctx.imageSmoothingQuality = 'high'

        switch (theme.numberStyle) {
            case 'modern':
                this.drawModernNumber(number, theme, size)
                break
            case 'runic':
                this.drawRunicNumber(number, theme, size)
                break
            case 'digital':
                this.drawDigitalNumber(number, theme, size)
                break
            case 'crystal':
                this.drawCrystalNumber(number, theme, size)
                break
            case 'flame':
                this.drawFlameNumber(number, theme, size)
                break
            case 'organic':
                this.drawOrganicNumber(number, theme, size)
                break
            default:
                this.drawModernNumber(number, theme, size)
        }

        const texture = new THREE.CanvasTexture(this.canvas)
        texture.needsUpdate = true
        texture.wrapS = THREE.RepeatWrapping
        texture.wrapT = THREE.RepeatWrapping
        return texture
    }

    drawModernNumber(number, theme, size) {
        const center = size / 2
        const fontSize = size * 0.6

        // Set font
        this.ctx.font = `bold ${fontSize}px 'Arial', sans-serif`
        this.ctx.textAlign = 'center'
        this.ctx.textBaseline = 'middle'

        // Draw glow effect
        this.ctx.shadowColor = theme.numberColor
        this.ctx.shadowBlur = 20
        this.ctx.shadowOffsetX = 0
        this.ctx.shadowOffsetY = 0

        // Draw main number
        this.ctx.fillStyle = theme.numberColor
        this.ctx.fillText(number.toString(), center, center)

        // Draw border
        this.ctx.shadowBlur = 0
        this.ctx.strokeStyle = this.darkenColor(theme.numberColor, 0.3)
        this.ctx.lineWidth = 4
        this.ctx.strokeText(number.toString(), center, center)
    }

    drawRunicNumber(number, theme, size) {
        const center = size / 2

        // Create runic-style numbers using custom paths
        this.ctx.strokeStyle = theme.numberColor
        this.ctx.fillStyle = theme.numberColor
        this.ctx.lineWidth = 8
        this.ctx.lineCap = 'round'
        this.ctx.lineJoin = 'round'

        // Add glow
        this.ctx.shadowColor = theme.numberColor
        this.ctx.shadowBlur = 15

        this.drawRunicSymbol(number, center, size * 0.3)
    }

    drawDigitalNumber(number, theme, size) {
        const segments = this.getDigitalSegments(number)
        const segmentSize = size * 0.35
        const center = size / 2

        this.ctx.fillStyle = theme.numberColor
        this.ctx.strokeStyle = theme.numberColor
        this.ctx.lineWidth = size * 0.08
        this.ctx.lineCap = 'round'

        // Add digital glow
        this.ctx.shadowColor = theme.numberColor
        this.ctx.shadowBlur = 25

        this.drawDigitalSegments(segments, center, segmentSize)
    }

    drawCrystalNumber(number, theme, size) {
        const center = size / 2
        const fontSize = size * 0.5

        // Create crystalline effect
        this.ctx.font = `bold ${fontSize}px 'Arial', sans-serif`
        this.ctx.textAlign = 'center'
        this.ctx.textBaseline = 'middle'

        // Multiple layers for crystal effect
        const layers = [
            { offset: 3, color: this.lightenColor(theme.numberColor, 0.6), alpha: 0.3 },
            { offset: 2, color: this.lightenColor(theme.numberColor, 0.4), alpha: 0.5 },
            { offset: 1, color: this.lightenColor(theme.numberColor, 0.2), alpha: 0.7 },
            { offset: 0, color: theme.numberColor, alpha: 1.0 }
        ]

        layers.forEach(layer => {
            this.ctx.fillStyle = layer.color
            this.ctx.globalAlpha = layer.alpha
            this.ctx.fillText(number.toString(), center + layer.offset, center + layer.offset)
        })

        this.ctx.globalAlpha = 1.0
    }

    drawFlameNumber(number, theme, size) {
        const center = size / 2
        const fontSize = size * 0.6

        this.ctx.font = `bold ${fontSize}px 'Arial', sans-serif`
        this.ctx.textAlign = 'center'
        this.ctx.textBaseline = 'middle'

        // Create flame-like distortion
        const gradient = this.ctx.createLinearGradient(0, 0, 0, size)
        gradient.addColorStop(0, '#FF4500')
        gradient.addColorStop(0.5, '#FF6B35')
        gradient.addColorStop(1, '#FFFF00')

        this.ctx.fillStyle = gradient
        this.ctx.shadowColor = '#FF4500'
        this.ctx.shadowBlur = 30

        // Add flickering effect with multiple draws
        for (let i = 0; i < 3; i++) {
            const offset = (Math.random() - 0.5) * 4
            this.ctx.fillText(number.toString(), center + offset, center + offset)
        }
    }

    drawOrganicNumber(number, theme, size) {
        const center = size / 2
        const radius = size * 0.3

        // Draw organic, branch-like representation
        this.ctx.strokeStyle = theme.numberColor
        this.ctx.lineWidth = 6
        this.ctx.lineCap = 'round'
        this.ctx.shadowColor = theme.numberColor
        this.ctx.shadowBlur = 10

        this.drawOrganicPattern(number, center, radius)
    }

    createMaterialTexture(diceType, theme, size = 512) {
        this.canvas.width = size
        this.canvas.height = size

        // Create base color
        const baseColor = theme.diceColors[diceType]
        this.ctx.fillStyle = baseColor
        this.ctx.fillRect(0, 0, size, size)

        // Add texture patterns based on theme
        switch (theme.name) {
            case 'Medieval':
                this.addMetalTexture(size, baseColor)
                break
            case 'Cyberpunk':
                this.addCircuitTexture(size, baseColor)
                break
            case 'Ice Crystal':
                this.addIceTexture(size, baseColor)
                break
            case 'Flame':
                this.addFlameTexture(size, baseColor)
                break
            case 'Nature':
                this.addWoodTexture(size, baseColor)
                break
            default:
                this.addPlasticTexture(size, baseColor)
        }

        const texture = new THREE.CanvasTexture(this.canvas)
        texture.needsUpdate = true
        texture.wrapS = THREE.RepeatWrapping
        texture.wrapT = THREE.RepeatWrapping
        return texture
    }

    addPlasticTexture(size, baseColor) {
        // Add subtle noise for plastic texture
        const imageData = this.ctx.getImageData(0, 0, size, size)
        const data = imageData.data

        for (let i = 0; i < data.length; i += 4) {
            const noise = (Math.random() - 0.5) * 20
            data[i] = Math.max(0, Math.min(255, data[i] + noise))
            data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + noise))
            data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + noise))
        }

        this.ctx.putImageData(imageData, 0, 0)
    }

    addMetalTexture(size, baseColor) {
        // Add scratches and metal grain
        this.ctx.globalCompositeOperation = 'overlay'

        for (let i = 0; i < 50; i++) {
            this.ctx.strokeStyle = `rgba(255, 255, 255, ${Math.random() * 0.3})`
            this.ctx.lineWidth = Math.random() * 2
            this.ctx.beginPath()
            this.ctx.moveTo(Math.random() * size, Math.random() * size)
            this.ctx.lineTo(Math.random() * size, Math.random() * size)
            this.ctx.stroke()
        }

        this.ctx.globalCompositeOperation = 'source-over'
    }

    addCircuitTexture(size, baseColor) {
        // Add circuit board patterns
        this.ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)'
        this.ctx.lineWidth = 2

        // Draw grid
        const gridSize = size / 16
        for (let x = 0; x < size; x += gridSize) {
            for (let y = 0; y < size; y += gridSize) {
                if (Math.random() > 0.7) {
                    this.ctx.strokeRect(x, y, gridSize, gridSize)
                }
            }
        }

        // Add random circuit paths
        for (let i = 0; i < 10; i++) {
            this.ctx.beginPath()
            this.ctx.moveTo(Math.random() * size, Math.random() * size)
            for (let j = 0; j < 5; j++) {
                this.ctx.lineTo(Math.random() * size, Math.random() * size)
            }
            this.ctx.stroke()
        }
    }

    addIceTexture(size, baseColor) {
        // Add frost patterns
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)'
        this.ctx.lineWidth = 1

        for (let i = 0; i < 100; i++) {
            const centerX = Math.random() * size
            const centerY = Math.random() * size
            const branches = 6

            for (let j = 0; j < branches; j++) {
                const angle = (j / branches) * Math.PI * 2
                const length = Math.random() * 30 + 10

                this.ctx.beginPath()
                this.ctx.moveTo(centerX, centerY)
                this.ctx.lineTo(
                    centerX + Math.cos(angle) * length,
                    centerY + Math.sin(angle) * length
                )
                this.ctx.stroke()
            }
        }
    }

    addFlameTexture(size, baseColor) {
        // Add flame-like patterns
        const gradient = this.ctx.createRadialGradient(size/2, size, 0, size/2, size/2, size/2)
        gradient.addColorStop(0, 'rgba(255, 255, 0, 0.3)')
        gradient.addColorStop(0.5, 'rgba(255, 69, 0, 0.2)')
        gradient.addColorStop(1, 'rgba(139, 0, 0, 0.1)')

        this.ctx.globalCompositeOperation = 'overlay'
        this.ctx.fillStyle = gradient
        this.ctx.fillRect(0, 0, size, size)
        this.ctx.globalCompositeOperation = 'source-over'
    }

    addWoodTexture(size, baseColor) {
        // Add wood grain
        this.ctx.globalCompositeOperation = 'multiply'

        for (let y = 0; y < size; y++) {
            const wave = Math.sin(y * 0.1) * 10 + Math.sin(y * 0.05) * 5
            this.ctx.strokeStyle = `rgba(101, 67, 33, ${0.1 + Math.random() * 0.2})`
            this.ctx.lineWidth = 1 + Math.random() * 2
            this.ctx.beginPath()
            this.ctx.moveTo(0, y)
            this.ctx.lineTo(size, y + wave)
            this.ctx.stroke()
        }

        this.ctx.globalCompositeOperation = 'source-over'
    }

    // Helper methods for drawing different number styles
    drawRunicSymbol(number, centerX, radius) {
        // Simplified runic symbols
        const symbols = {
            1: () => this.drawVerticalLine(centerX, radius),
            2: () => this.drawDoubleLines(centerX, radius),
            3: () => this.drawTriple(centerX, radius),
            4: () => this.drawSquare(centerX, radius),
            5: () => this.drawPentagram(centerX, radius),
            6: () => this.drawHexagon(centerX, radius)
        }

        const drawFunc = symbols[number] || symbols[1]
        drawFunc()
    }

    drawVerticalLine(centerX, radius) {
        this.ctx.beginPath()
        this.ctx.moveTo(centerX, centerX - radius)
        this.ctx.lineTo(centerX, centerX + radius)
        this.ctx.stroke()
    }

    drawDigitalSegments(segments, center, size) {
        // Implementation for 7-segment display style numbers
        const segmentPaths = {
            a: [[0, -size], [size*0.8, -size]],
            b: [[size*0.8, -size], [size*0.8, 0]],
            c: [[size*0.8, 0], [size*0.8, size]],
            d: [[size*0.8, size], [0, size]],
            e: [[0, size], [0, 0]],
            f: [[0, 0], [0, -size]],
            g: [[0, 0], [size*0.8, 0]]
        }

        segments.forEach(segment => {
            if (segmentPaths[segment]) {
                const path = segmentPaths[segment]
                this.ctx.beginPath()
                this.ctx.moveTo(center + path[0][0], center + path[0][1])
                this.ctx.lineTo(center + path[1][0], center + path[1][1])
                this.ctx.stroke()
            }
        })
    }

    drawOrganicPattern(number, center, radius) {
        // Draw branch-like patterns for organic style
        const branches = number
        for (let i = 0; i < branches; i++) {
            const angle = (i / branches) * Math.PI * 2
            const branchLength = radius * (0.7 + Math.random() * 0.3)

            this.ctx.beginPath()
            this.ctx.moveTo(center, center)

            // Draw wavy branch
            const steps = 10
            for (let j = 0; j <= steps; j++) {
                const t = j / steps
                const x = center + Math.cos(angle) * branchLength * t
                const y = center + Math.sin(angle) * branchLength * t
                const wave = Math.sin(t * Math.PI * 3) * 5

                this.ctx.lineTo(
                    x + Math.cos(angle + Math.PI/2) * wave,
                    y + Math.sin(angle + Math.PI/2) * wave
                )
            }

            this.ctx.stroke()
        }
    }

    getDigitalSegments(number) {
        const segmentMap = {
            0: ['a', 'b', 'c', 'd', 'e', 'f'],
            1: ['b', 'c'],
            2: ['a', 'b', 'g', 'e', 'd'],
            3: ['a', 'b', 'g', 'c', 'd'],
            4: ['f', 'g', 'b', 'c'],
            5: ['a', 'f', 'g', 'c', 'd'],
            6: ['a', 'f', 'g', 'e', 'd', 'c'],
            7: ['a', 'b', 'c'],
            8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            9: ['a', 'b', 'c', 'd', 'f', 'g']
        }
        return segmentMap[number] || segmentMap[0]
    }

    getMaxNumber(diceType) {
        const maxNumbers = {
            'd4': 4, 'd6': 6, 'd8': 8, 'd10': 10,
            'd12': 12, 'd20': 20, 'd100': 100
        }
        return maxNumbers[diceType] || 6
    }

    // Utility color functions
    lightenColor(color, factor) {
        const hex = color.replace('#', '')
        const r = parseInt(hex.substr(0, 2), 16)
        const g = parseInt(hex.substr(2, 2), 16)
        const b = parseInt(hex.substr(4, 2), 16)

        const newR = Math.min(255, Math.floor(r + (255 - r) * factor))
        const newG = Math.min(255, Math.floor(g + (255 - g) * factor))
        const newB = Math.min(255, Math.floor(b + (255 - b) * factor))

        return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
    }

    darkenColor(color, factor) {
        const hex = color.replace('#', '')
        const r = parseInt(hex.substr(0, 2), 16)
        const g = parseInt(hex.substr(2, 2), 16)
        const b = parseInt(hex.substr(4, 2), 16)

        const newR = Math.floor(r * (1 - factor))
        const newG = Math.floor(g * (1 - factor))
        const newB = Math.floor(b * (1 - factor))

        return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
    }

    // Public methods
    setTheme(themeName) {
        if (this.themes.has(themeName)) {
            this.currentTheme = themeName
            this.generateDefaultTextures()
        }
    }

    getThemeNames() {
        return Array.from(this.themes.keys())
    }

    getCurrentTheme() {
        return this.themes.get(this.currentTheme)
    }

    getNumberTexture(diceType, number) {
        const key = `${diceType}_${number}_${this.currentTheme}`
        return this.numberTextures.get(key)
    }

    getMaterialTexture(diceType) {
        const key = `${diceType}_material_${this.currentTheme}`
        return this.textures.get(key)
    }

    createCustomTheme(name, config) {
        this.themes.set(name, {
            name,
            diceColors: config.diceColors || this.themes.get('default').diceColors,
            numberColor: config.numberColor || '#ffffff',
            numberStyle: config.numberStyle || 'modern',
            roughness: config.roughness || 0.3,
            metalness: config.metalness || 0.1,
            emissive: config.emissive || 0.1,
            transparent: config.transparent || false,
            opacity: config.opacity || 1.0
        })
    }

    preloadTheme(themeName) {
        const oldTheme = this.currentTheme
        this.setTheme(themeName)
        this.setTheme(oldTheme)
    }

    dispose() {
        this.textures.forEach(texture => texture.dispose())
        this.numberTextures.forEach(texture => texture.dispose())
        this.textures.clear()
        this.numberTextures.clear()
    }
}

export default DiceTextureManager