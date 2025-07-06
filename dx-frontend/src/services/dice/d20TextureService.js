import * as THREE from 'three'

export class D20TextureService {
    constructor() {
        this.userTexture = null
        this.textureCache = new Map()
        this.canvas = document.createElement('canvas')
        this.ctx = this.canvas.getContext('2d')
        this.canvas.width = this.canvas.height = 512
    }

    setUserTexture(imageFile) {
        return new Promise((resolve) => {
            if (!imageFile) {
                this.userTexture = null
                this.clearCache()
                resolve(true)
                return
            }

            const reader = new FileReader()
            reader.onload = (event) => {
                const img = new Image()
                img.onload = () => {
                    this.userTexture = img
                    this.clearCache() // Clear cache when texture changes
                    resolve(true)
                }
                img.onerror = () => resolve(false)
                img.src = event.target.result
            }
            reader.onerror = () => resolve(false)
            reader.readAsDataURL(imageFile)
        })
    }

    createNumberTexture(number, options = {}) {
        const {
            baseColor = "#4444ff",
            textColor = "#fff",
            highlight = false,
            size = 512
        } = options

        // Create cache key
        const cacheKey = `${number}_${baseColor}_${textColor}_${highlight}_${size}_${this.userTexture ? 'custom' : 'default'}`
        
        // Return cached texture if available
        if (this.textureCache.has(cacheKey)) {
            return this.textureCache.get(cacheKey)
        }

        // Set canvas size
        this.canvas.width = this.canvas.height = size
        this.ctx.clearRect(0, 0, size, size)

        // Draw background
        this.drawBackground(baseColor, size)

        // Draw number
        this.drawNumber(number, textColor, highlight, size)

        // Create and cache texture
        const texture = new THREE.CanvasTexture(this.canvas)
        texture.needsUpdate = true
        this.textureCache.set(cacheKey, texture)

        return texture
    }

    drawBackground(baseColor, size) {
        if (this.userTexture) {
            // Draw user texture
            this.ctx.drawImage(this.userTexture, 0, 0, size, size)
            
            // Add overlay for better number visibility
            this.ctx.fillStyle = "rgba(0, 0, 0, 0.25)"
            this.ctx.fillRect(0, 0, size, size)
        } else {
            // Create gradient background
            const gradient = this.ctx.createRadialGradient(
                size / 2, size / 2, 0,
                size / 2, size / 2, size / 2
            )
            gradient.addColorStop(0, baseColor)
            gradient.addColorStop(1, "#333366")
            
            this.ctx.fillStyle = gradient
            this.ctx.fillRect(0, 0, size, size)
        }
    }

    drawNumber(number, textColor, highlight, size) {
        const center = size / 2
        const fontSize = size * 0.27 // Slightly smaller for better fit

        // Setup text rendering
        this.ctx.font = `bold ${fontSize}px Arial`
        this.ctx.textAlign = "center"
        this.ctx.textBaseline = "middle"

        // Add shadow
        this.ctx.shadowColor = "rgba(0, 0, 0, 0.7)"
        this.ctx.shadowBlur = 8
        this.ctx.shadowOffsetX = 3
        this.ctx.shadowOffsetY = 3

        // Set color based on number and highlight
        if (highlight) {
            if (number === 1) {
                this.ctx.fillStyle = "#ff0505" // Critical fail
            } else if (number === 20) {
                this.ctx.fillStyle = "#ffff00" // Critical success
            } else {
                this.ctx.fillStyle = "#16eaff" // Highlighted
            }
        } else {
            if (number === 1) {
                this.ctx.fillStyle = "#ff6666" // Muted fail
            } else if (number === 20) {
                this.ctx.fillStyle = "#ffff88" // Muted success
            } else {
                this.ctx.fillStyle = textColor // Normal
            }
        }

        // Draw the number
        this.ctx.fillText(number.toString(), center, center)

        // Add border for better contrast
        this.ctx.shadowBlur = 0
        this.ctx.shadowOffsetX = 0
        this.ctx.shadowOffsetY = 0
        this.ctx.strokeStyle = this.darkenColor(this.ctx.fillStyle, 0.5)
        this.ctx.lineWidth = 3
        this.ctx.strokeText(number.toString(), center, center)
    }

    createPresetTextures(highlightFace = -1) {
        const textures = []
        
        for (let i = 1; i <= 20; i++) {
            const isHighlighted = i - 1 === highlightFace
            const texture = this.createNumberTexture(i, {
                highlight: isHighlighted
            })
            textures.push(texture)
        }

        return textures
    }

    // Utility methods
    darkenColor(color, factor) {
        // Simple color darkening - works with hex colors
        if (color.startsWith('#')) {
            const hex = color.replace('#', '')
            const r = parseInt(hex.substr(0, 2), 16)
            const g = parseInt(hex.substr(2, 2), 16)
            const b = parseInt(hex.substr(4, 2), 16)

            const newR = Math.floor(r * (1 - factor))
            const newG = Math.floor(g * (1 - factor))
            const newB = Math.floor(b * (1 - factor))

            return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
        }
        
        // For rgba/rgb colors, return a dark version
        return 'rgba(0, 0, 0, 0.8)'
    }

    lightenColor(color, factor) {
        if (color.startsWith('#')) {
            const hex = color.replace('#', '')
            const r = parseInt(hex.substr(0, 2), 16)
            const g = parseInt(hex.substr(2, 2), 16)
            const b = parseInt(hex.substr(4, 2), 16)

            const newR = Math.min(255, Math.floor(r + (255 - r) * factor))
            const newG = Math.min(255, Math.floor(g + (255 - g) * factor))
            const newB = Math.min(255, Math.floor(b + (255 - b) * factor))

            return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
        }
        
        return 'rgba(255, 255, 255, 0.8)'
    }

    clearCache() {
        // Dispose of all cached textures
        this.textureCache.forEach(texture => {
            if (texture && texture.dispose) {
                texture.dispose()
            }
        })
        this.textureCache.clear()
    }

    getUserTexture() {
        return this.userTexture
    }

    hasUserTexture() {
        return this.userTexture !== null
    }

    dispose() {
        this.clearCache()
        this.userTexture = null
        
        // Clean up canvas
        this.ctx = null
        this.canvas = null
    }
}

export default D20TextureService