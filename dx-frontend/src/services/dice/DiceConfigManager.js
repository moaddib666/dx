export class DiceConfigManager {
    constructor() {
        this.config = {
            // Visual settings
            graphics: {
                quality: 'high', // 'low', 'medium', 'high', 'ultra'
                shadows: true,
                bloom: true,
                antialiasing: true,
                particleEffects: true,
                frameRate: 60,
                renderScale: 1.0
            },

            // Physics settings
            physics: {
                gravity: -9.8,
                restitution: 0.6,
                friction: 0.95,
                angularDamping: 0.98,
                throwForce: 5.0,
                autoSettle: true,
                settleTime: 2.0
            },

            // Audio settings
            audio: {
                enabled: true,
                masterVolume: 0.7,
                effectsVolume: 0.8,
                ambientVolume: 0.3,
                uiVolume: 0.5,
                enable3DAudio: true
            },

            // Theme and appearance
            appearance: {
                theme: 'default',
                customColors: null,
                backgroundType: 'gradient', // 'gradient', 'starfield', 'solid'
                backgroundColor: '#0f0f23',
                tableTexture: 'felt',
                lightingPreset: 'dramatic'
            },

            // Animation settings
            animation: {
                rollDuration: 2000,
                enablePhysics: true,
                enableBounce: true,
                showTrails: false,
                highlightResults: true,
                smoothCamera: true,
                cameraFollow: false
            },

            // Dice behavior
            dice: {
                autoRemoveOnRoll: false,
                highlightCriticals: true,
                showProbabilities: false,
                enableModifiers: true,
                defaultDiceSet: ['d20'],
                maxDiceCount: 20,
                favoriteRolls: []
            },

            // UI preferences
            interface: {
                modalSize: 'large', // 'small', 'medium', 'large', 'fullscreen'
                showTooltips: true,
                enableKeyboardShortcuts: true,
                compactMode: false,
                showStatistics: true,
                autoClose: false
            },

            // Performance settings
            performance: {
                maxParticles: 500,
                lodDistance: 20,
                cullingEnabled: true,
                adaptiveQuality: true,
                reducedMotion: false,
                batteryOptimization: false
            },

            // Accessibility
            accessibility: {
                highContrast: false,
                largeText: false,
                reduceFlashing: false,
                colorBlindMode: 'none', // 'none', 'protanopia', 'deuteranopia', 'tritanopia'
                screenReaderSupport: false,
                keyboardNavigation: true
            },

            // Developer settings
            debug: {
                showFPS: false,
                showPhysicsDebug: false,
                enableConsoleLogging: false,
                showBoundingBoxes: false,
                wireframeMode: false
            }
        }

        this.presets = {
            // Quality presets
            quality: {
                potato: {
                    graphics: { quality: 'low', shadows: false, bloom: false, antialiasing: false, particleEffects: false, renderScale: 0.5 },
                    performance: { maxParticles: 50, adaptiveQuality: true, batteryOptimization: true },
                    animation: { enablePhysics: false, showTrails: false }
                },
                low: {
                    graphics: { quality: 'low', shadows: false, bloom: false, antialiasing: false, particleEffects: true, renderScale: 0.75 },
                    performance: { maxParticles: 100, adaptiveQuality: true }
                },
                medium: {
                    graphics: { quality: 'medium', shadows: true, bloom: false, antialiasing: true, particleEffects: true, renderScale: 1.0 },
                    performance: { maxParticles: 250, adaptiveQuality: true }
                },
                high: {
                    graphics: { quality: 'high', shadows: true, bloom: true, antialiasing: true, particleEffects: true, renderScale: 1.0 },
                    performance: { maxParticles: 500, adaptiveQuality: false }
                },
                ultra: {
                    graphics: { quality: 'ultra', shadows: true, bloom: true, antialiasing: true, particleEffects: true, renderScale: 1.5 },
                    performance: { maxParticles: 1000, adaptiveQuality: false }
                }
            },

            // Theme presets
            themes: {
                classic: {
                    appearance: { theme: 'default', backgroundType: 'gradient', tableTexture: 'felt' }
                },
                cyberpunk: {
                    appearance: { theme: 'cyberpunk', backgroundType: 'starfield', tableTexture: 'metal' }
                },
                medieval: {
                    appearance: { theme: 'medieval', backgroundType: 'solid', backgroundColor: '#2c1810', tableTexture: 'wood' }
                },
                ice: {
                    appearance: { theme: 'ice', backgroundType: 'gradient', backgroundColor: '#e0f6ff', tableTexture: 'ice' }
                }
            },

            // Accessibility presets
            accessibility: {
                highContrast: {
                    accessibility: { highContrast: true, largeText: true },
                    appearance: { theme: 'highContrast' }
                },
                colorBlind: {
                    accessibility: { colorBlindMode: 'deuteranopia' },
                    appearance: { theme: 'colorBlindFriendly' }
                },
                motorImpaired: {
                    interface: { showTooltips: true, enableKeyboardShortcuts: true },
                    accessibility: { keyboardNavigation: true },
                    animation: { rollDuration: 3000 }
                }
            }
        }

        this.eventHandlers = new Map()
        this.loadFromStorage()
    }

    // Core configuration methods
    get(path) {
        return this.getNestedValue(this.config, path)
    }

    set(path, value) {
        this.setNestedValue(this.config, path, value)
        this.saveToStorage()
        this.notifyChange(path, value)
    }

    reset() {
        this.config = this.getDefaultConfig()
        this.saveToStorage()
        this.notifyChange('*', this.config)
    }

    // Preset management
    applyPreset(category, presetName) {
        const preset = this.presets[category]?.[presetName]
        if (!preset) {
            console.warn(`Preset ${category}.${presetName} not found`)
            return false
        }

        Object.keys(preset).forEach(section => {
            Object.keys(preset[section]).forEach(key => {
                this.set(`${section}.${key}`, preset[section][key])
            })
        })

        return true
    }

    getAvailablePresets(category) {
        return Object.keys(this.presets[category] || {})
    }

    createCustomPreset(category, name, config) {
        if (!this.presets[category]) {
            this.presets[category] = {}
        }
        this.presets[category][name] = config
        this.saveToStorage()
    }

    // Auto-detection and optimization
    autoDetectSettings() {
        const capabilities = this.detectCapabilities()

        // Auto-set quality based on device capabilities
        if (capabilities.isMobile) {
            this.applyPreset('quality', 'low')
        } else if (capabilities.isLowEnd) {
            this.applyPreset('quality', 'medium')
        } else if (capabilities.isHighEnd) {
            this.applyPreset('quality', 'ultra')
        } else {
            this.applyPreset('quality', 'high')
        }

        // Adjust for battery
        if (capabilities.isBatteryLow) {
            this.set('performance.batteryOptimization', true)
        }

        // Adjust for reduced motion preference
        if (capabilities.prefersReducedMotion) {
            this.set('accessibility.reducedMotion', true)
            this.set('animation.rollDuration', 1000)
        }
    }

    detectCapabilities() {
        const canvas = document.createElement('canvas')
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')

        const capabilities = {
            webglSupported: !!gl,
            isMobile: /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
            isLowEnd: false,
            isHighEnd: false,
            isBatteryLow: false,
            prefersReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
            supportsWebAudio: !!(window.AudioContext || window.webkitAudioContext),
            devicePixelRatio: window.devicePixelRatio || 1
        }

        // Detect performance tier
        if (gl) {
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info')
            if (debugInfo) {
                const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
                capabilities.isLowEnd = /integrated|intel hd|iris/i.test(renderer)
                capabilities.isHighEnd = /rtx|gtx|radeon rx|geforce/i.test(renderer)
            }
        }

        // Battery API (experimental)
        if ('getBattery' in navigator) {
            navigator.getBattery().then(battery => {
                capabilities.isBatteryLow = battery.level < 0.2
            })
        }

        return capabilities
    }

    // Profile management
    saveProfile(name) {
        const profiles = this.getStoredProfiles()
        profiles[name] = { ...this.config, createdAt: Date.now() }
        localStorage.setItem('diceRoller_profiles', JSON.stringify(profiles))
    }

    loadProfile(name) {
        const profiles = this.getStoredProfiles()
        if (profiles[name]) {
            this.config = { ...profiles[name] }
            delete this.config.createdAt
            this.saveToStorage()
            this.notifyChange('*', this.config)
            return true
        }
        return false
    }

    deleteProfile(name) {
        const profiles = this.getStoredProfiles()
        delete profiles[name]
        localStorage.setItem('diceRoller_profiles', JSON.stringify(profiles))
    }

    getAvailableProfiles() {
        return Object.keys(this.getStoredProfiles())
    }

    getStoredProfiles() {
        try {
            return JSON.parse(localStorage.getItem('diceRoller_profiles') || '{}')
        } catch {
            return {}
        }
    }

    // Validation and constraints
    validateConfig(path, value) {
        const constraints = {
            'graphics.quality': ['low', 'medium', 'high', 'ultra'],
            'graphics.frameRate': { min: 15, max: 144 },
            'graphics.renderScale': { min: 0.25, max: 2.0 },
            'physics.gravity': { min: -20, max: 0 },
            'physics.restitution': { min: 0, max: 1 },
            'physics.friction': { min: 0, max: 1 },
            'physics.throwForce': { min: 1, max: 20 },
            'audio.masterVolume': { min: 0, max: 1 },
            'audio.effectsVolume': { min: 0, max: 1 },
            'audio.ambientVolume': { min: 0, max: 1 },
            'animation.rollDuration': { min: 500, max: 10000 },
            'dice.maxDiceCount': { min: 1, max: 50 },
            'performance.maxParticles': { min: 0, max: 2000 }
        }

        const constraint = constraints[path]
        if (!constraint) return true

        if (Array.isArray(constraint)) {
            return constraint.includes(value)
        }

        if (typeof constraint === 'object' && constraint.min !== undefined) {
            return value >= constraint.min && value <= constraint.max
        }

        return true
    }

    // Event system
    onChange(path, handler) {
        if (!this.eventHandlers.has(path)) {
            this.eventHandlers.set(path, [])
        }
        this.eventHandlers.get(path).push(handler)
    }

    offChange(path, handler) {
        const handlers = this.eventHandlers.get(path)
        if (handlers) {
            const index = handlers.indexOf(handler)
            if (index > -1) {
                handlers.splice(index, 1)
            }
        }
    }

    notifyChange(path, value) {
        // Notify specific path handlers
        const handlers = this.eventHandlers.get(path) || []
        handlers.forEach(handler => handler(value, path))

        // Notify wildcard handlers
        const wildcardHandlers = this.eventHandlers.get('*') || []
        wildcardHandlers.forEach(handler => handler(value, path))
    }

    // Import/Export
    exportConfig() {
        return JSON.stringify({
            config: this.config,
            version: '1.0.0',
            exportedAt: new Date().toISOString()
        }, null, 2)
    }

    importConfig(jsonString) {
        try {
            const imported = JSON.parse(jsonString)
            if (imported.config) {
                this.config = { ...this.getDefaultConfig(), ...imported.config }
                this.saveToStorage()
                this.notifyChange('*', this.config)
                return true
            }
        } catch (error) {
            console.error('Failed to import config:', error)
        }
        return false
    }

    // Storage management
    saveToStorage() {
        try {
            localStorage.setItem('diceRoller_config', JSON.stringify(this.config))
        } catch (error) {
            console.warn('Failed to save config to localStorage:', error)
        }
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem('diceRoller_config')
            if (stored) {
                const parsedConfig = JSON.parse(stored)
                this.config = { ...this.getDefaultConfig(), ...parsedConfig }
            }
        } catch (error) {
            console.warn('Failed to load config from localStorage:', error)
            this.config = this.getDefaultConfig()
        }
    }

    clearStorage() {
        localStorage.removeItem('diceRoller_config')
        localStorage.removeItem('diceRoller_profiles')
    }

    // Utility methods
    getNestedValue(obj, path) {
        return path.split('.').reduce((current, key) => current?.[key], obj)
    }

    setNestedValue(obj, path, value) {
        const keys = path.split('.')
        const lastKey = keys.pop()
        const target = keys.reduce((current, key) => {
            if (!current[key] || typeof current[key] !== 'object') {
                current[key] = {}
            }
            return current[key]
        }, obj)

        if (this.validateConfig(path, value)) {
            target[lastKey] = value
        } else {
            console.warn(`Invalid value for ${path}:`, value)
        }
    }

    getDefaultConfig() {
        // Return a deep copy of the default configuration
        return JSON.parse(JSON.stringify({
            graphics: {
                quality: 'high',
                shadows: true,
                bloom: true,
                antialiasing: true,
                particleEffects: true,
                frameRate: 60,
                renderScale: 1.0
            },
            physics: {
                gravity: -9.8,
                restitution: 0.6,
                friction: 0.95,
                angularDamping: 0.98,
                throwForce: 5.0,
                autoSettle: true,
                settleTime: 2.0
            },
            audio: {
                enabled: true,
                masterVolume: 0.7,
                effectsVolume: 0.8,
                ambientVolume: 0.3,
                uiVolume: 0.5,
                enable3DAudio: true
            },
            appearance: {
                theme: 'default',
                customColors: null,
                backgroundType: 'gradient',
                backgroundColor: '#0f0f23',
                tableTexture: 'felt',
                lightingPreset: 'dramatic'
            },
            animation: {
                rollDuration: 2000,
                enablePhysics: true,
                enableBounce: true,
                showTrails: false,
                highlightResults: true,
                smoothCamera: true,
                cameraFollow: false
            },
            dice: {
                autoRemoveOnRoll: false,
                highlightCriticals: true,
                showProbabilities: false,
                enableModifiers: true,
                defaultDiceSet: ['d20'],
                maxDiceCount: 20,
                favoriteRolls: []
            },
            interface: {
                modalSize: 'large',
                showTooltips: true,
                enableKeyboardShortcuts: true,
                compactMode: false,
                showStatistics: true,
                autoClose: false
            },
            performance: {
                maxParticles: 500,
                lodDistance: 20,
                cullingEnabled: true,
                adaptiveQuality: true,
                reducedMotion: false,
                batteryOptimization: false
            },
            accessibility: {
                highContrast: false,
                largeText: false,
                reduceFlashing: false,
                colorBlindMode: 'none',
                screenReaderSupport: false,
                keyboardNavigation: true
            },
            debug: {
                showFPS: false,
                showPhysicsDebug: false,
                enableConsoleLogging: false,
                showBoundingBoxes: false,
                wireframeMode: false
            }
        }))
    }

    // Performance monitoring
    getPerformanceRecommendations() {
        const recommendations = []

        if (this.get('graphics.quality') === 'ultra' && this.get('performance.adaptiveQuality')) {
            recommendations.push({
                type: 'performance',
                message: 'Consider lowering graphics quality for better performance',
                action: () => this.set('graphics.quality', 'high')
            })
        }

        if (this.get('graphics.shadows') && this.get('performance.batteryOptimization')) {
            recommendations.push({
                type: 'battery',
                message: 'Disable shadows to improve battery life',
                action: () => this.set('graphics.shadows', false)
            })
        }

        return recommendations
    }

    // Statistics and analytics
    getUsageStatistics() {
        return {
            configVersion: '1.0.0',
            lastModified: new Date().toISOString(),
            totalSettings: this.countSettings(this.config),
            customizedSettings: this.countCustomizedSettings(),
            currentPreset: this.detectCurrentPreset()
        }
    }

    countSettings(obj, prefix = '') {
        let count = 0
        for (const [key, value] of Object.entries(obj)) {
            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                count += this.countSettings(value, `${prefix}${key}.`)
            } else {
                count++
            }
        }
        return count
    }

    countCustomizedSettings() {
        const defaults = this.getDefaultConfig()
        return this.countDifferences(this.config, defaults)
    }

    countDifferences(obj1, obj2, count = 0) {
        for (const key in obj1) {
            if (typeof obj1[key] === 'object' && obj1[key] !== null && !Array.isArray(obj1[key])) {
                count = this.countDifferences(obj1[key], obj2[key] || {}, count)
            } else if (obj1[key] !== obj2[key]) {
                count++
            }
        }
        return count
    }

    detectCurrentPreset() {
        // Try to match current config with known presets
        for (const [category, presets] of Object.entries(this.presets)) {
            for (const [name, preset] of Object.entries(presets)) {
                if (this.matchesPreset(preset)) {
                    return `${category}.${name}`
                }
            }
        }
        return 'custom'
    }

    matchesPreset(preset) {
        for (const [section, settings] of Object.entries(preset)) {
            for (const [key, value] of Object.entries(settings)) {
                if (this.get(`${section}.${key}`) !== value) {
                    return false
                }
            }
        }
        return true
    }
}

export default DiceConfigManager