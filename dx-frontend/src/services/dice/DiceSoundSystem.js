export class DiceSoundSystem {
    constructor() {
        this.audioContext = null
        this.sounds = new Map()
        this.volume = 0.7
        this.isEnabled = true
        this.isInitialized = false

        // Sound URLs - you would replace these with actual sound files
        this.soundFiles = {
            diceRoll: '/sounds/dice-roll.mp3',
            diceHit: '/sounds/dice-hit.mp3',
            diceSettle: '/sounds/dice-settle.mp3',
            criticalHit: '/sounds/critical-hit.mp3',
            criticalMiss: '/sounds/critical-miss.mp3',
            modalOpen: '/sounds/modal-open.mp3',
            modalClose: '/sounds/modal-close.mp3',
            diceAdd: '/sounds/dice-add.mp3',
            diceRemove: '/sounds/dice-remove.mp3',
            rollComplete: '/sounds/roll-complete.mp3',
            uiClick: '/sounds/ui-click.mp3',
            uiHover: '/sounds/ui-hover.mp3',
            ambientMagic: '/sounds/ambient-magic.mp3'
        }

        // Procedural sound parameters
        this.oscillatorParams = {
            diceHit: { frequency: 200, type: 'square', duration: 0.1 },
            diceRoll: { frequency: 150, type: 'sawtooth', duration: 0.3 },
            diceSettle: { frequency: 100, type: 'sine', duration: 0.2 },
            criticalHit: { frequency: 440, type: 'sine', duration: 0.5 },
            criticalMiss: { frequency: 110, type: 'square', duration: 0.3 },
            uiClick: { frequency: 800, type: 'sine', duration: 0.05 },
            uiHover: { frequency: 600, type: 'sine', duration: 0.03 }
        }

        this.initialize()
    }

    async initialize() {
        try {
            // Initialize Web Audio API
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)()

            // Create master gain node for volume control
            this.masterGain = this.audioContext.createGain()
            this.masterGain.gain.value = this.volume
            this.masterGain.connect(this.audioContext.destination)

            // Create effects chain
            this.createEffectsChain()

            // Load sound files
            await this.loadSounds()

            this.isInitialized = true
        } catch (error) {
            console.warn('Audio initialization failed:', error)
            this.isEnabled = false
        }
    }

    createEffectsChain() {
        // Reverb effect for ambient sounds
        this.reverbGain = this.audioContext.createGain()
        this.reverbGain.gain.value = 0.3
        this.reverbGain.connect(this.masterGain)

        // Create impulse response for reverb
        this.createReverbImpulse()

        // Compressor for dynamic range
        this.compressor = this.audioContext.createDynamicsCompressor()
        this.compressor.threshold.value = -20
        this.compressor.knee.value = 40
        this.compressor.ratio.value = 12
        this.compressor.attack.value = 0.003
        this.compressor.release.value = 0.25
        this.compressor.connect(this.masterGain)
    }

    createReverbImpulse() {
        const length = this.audioContext.sampleRate * 2 // 2 seconds
        const impulse = this.audioContext.createBuffer(2, length, this.audioContext.sampleRate)

        for (let channel = 0; channel < 2; channel++) {
            const channelData = impulse.getChannelData(channel)
            for (let i = 0; i < length; i++) {
                const decay = Math.pow(1 - i / length, 2)
                channelData[i] = (Math.random() * 2 - 1) * decay
            }
        }

        this.convolver = this.audioContext.createConvolver()
        this.convolver.buffer = impulse
        this.convolver.connect(this.reverbGain)
    }

    async loadSounds() {
        const loadPromises = Object.entries(this.soundFiles).map(async ([key, url]) => {
            try {
                const response = await fetch(url)
                const arrayBuffer = await response.arrayBuffer()
                const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer)
                this.sounds.set(key, audioBuffer)
            } catch (error) {
                console.warn(`Failed to load sound ${key}:`, error)
                // Fallback to procedural sound
                this.sounds.set(key, null)
            }
        })

        await Promise.allSettled(loadPromises)
    }

    playSound(soundKey, options = {}) {
        if (!this.isEnabled || !this.isInitialized) return

        // Resume audio context if suspended (required by browser policies)
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume()
        }

        const {
            volume = 1.0,
            pitch = 1.0,
            delay = 0,
            loop = false,
            fadeIn = 0,
            fadeOut = 0,
            useReverb = false,
            pan = 0
        } = options

        const soundBuffer = this.sounds.get(soundKey)

        if (soundBuffer) {
            this.playBufferedSound(soundBuffer, {
                volume, pitch, delay, loop, fadeIn, fadeOut, useReverb, pan
            })
        } else {
            // Fallback to procedural sound
            this.playProceduralSound(soundKey, { volume, pitch, delay })
        }
    }

    playBufferedSound(buffer, options) {
        const source = this.audioContext.createBufferSource()
        source.buffer = buffer
        source.playbackRate.value = options.pitch

        // Create gain node for volume
        const gainNode = this.audioContext.createGain()
        gainNode.gain.value = options.volume * this.volume

        // Create panner for 3D positioning
        const panner = this.audioContext.createStereoPanner()
        panner.pan.value = Math.max(-1, Math.min(1, options.pan))

        // Connect audio graph
        source.connect(gainNode)
        gainNode.connect(panner)

        if (options.useReverb) {
            panner.connect(this.convolver)
        } else {
            panner.connect(this.compressor)
        }

        // Handle fade effects
        if (options.fadeIn > 0) {
            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime + options.delay)
            gainNode.gain.linearRampToValueAtTime(
                options.volume * this.volume,
                this.audioContext.currentTime + options.delay + options.fadeIn
            )
        }

        if (options.fadeOut > 0) {
            const fadeStartTime = this.audioContext.currentTime + options.delay + buffer.duration - options.fadeOut
            gainNode.gain.setValueAtTime(options.volume * this.volume, fadeStartTime)
            gainNode.gain.linearRampToValueAtTime(0, fadeStartTime + options.fadeOut)
        }

        // Set loop
        source.loop = options.loop

        // Start playback
        source.start(this.audioContext.currentTime + options.delay)

        return source
    }

    playProceduralSound(soundKey, options) {
        const params = this.oscillatorParams[soundKey]
        if (!params) return

        const oscillator = this.audioContext.createOscillator()
        const gainNode = this.audioContext.createGain()
        const filter = this.audioContext.createBiquadFilter()

        // Configure oscillator
        oscillator.type = params.type
        oscillator.frequency.setValueAtTime(
            params.frequency * options.pitch,
            this.audioContext.currentTime
        )

        // Configure filter
        filter.type = 'lowpass'
        filter.frequency.setValueAtTime(2000, this.audioContext.currentTime)
        filter.Q.setValueAtTime(1, this.audioContext.currentTime)

        // Configure envelope
        const startTime = this.audioContext.currentTime + options.delay
        const endTime = startTime + params.duration

        gainNode.gain.setValueAtTime(0, startTime)
        gainNode.gain.linearRampToValueAtTime(options.volume * this.volume, startTime + 0.01)
        gainNode.gain.exponentialRampToValueAtTime(0.001, endTime)

        // Connect audio graph
        oscillator.connect(filter)
        filter.connect(gainNode)
        gainNode.connect(this.compressor)

        // Start and stop
        oscillator.start(startTime)
        oscillator.stop(endTime)

        return oscillator
    }

    // Specific methods for dice events
    playDiceRoll(diceCount = 1) {
        // Play roll sound with variations based on dice count
        const baseVolume = Math.min(1.0, 0.3 + diceCount * 0.1)

        this.playSound('diceRoll', {
            volume: baseVolume,
            pitch: 0.8 + Math.random() * 0.4,
            useReverb: true
        })

        // Add ambient rolling sounds
        for (let i = 0; i < Math.min(diceCount, 5); i++) {
            this.playSound('diceRoll', {
                volume: baseVolume * 0.5,
                pitch: 0.7 + Math.random() * 0.6,
                delay: Math.random() * 0.5,
                useReverb: true
            })
        }
    }

    playDiceHit(intensity = 1.0, material = 'plastic') {
        const materialParams = {
            plastic: { pitch: 1.0, volume: 0.8 },
            metal: { pitch: 1.5, volume: 1.0 },
            wood: { pitch: 0.7, volume: 0.9 },
            stone: { pitch: 0.5, volume: 1.1 }
        }

        const params = materialParams[material] || materialParams.plastic

        this.playSound('diceHit', {
            volume: params.volume * intensity * 0.6,
            pitch: params.pitch + (Math.random() - 0.5) * 0.3,
            pan: (Math.random() - 0.5) * 0.5
        })
    }

    playDiceSettle(diceType) {
        // Different settle sounds for different dice
        const diceParams = {
            'd4': { pitch: 1.2, volume: 0.7 },
            'd6': { pitch: 1.0, volume: 0.8 },
            'd8': { pitch: 1.1, volume: 0.75 },
            'd10': { pitch: 0.9, volume: 0.8 },
            'd12': { pitch: 0.8, volume: 0.85 },
            'd20': { pitch: 0.7, volume: 0.9 },
            'd100': { pitch: 0.6, volume: 0.8 }
        }

        const params = diceParams[diceType] || diceParams['d6']

        this.playSound('diceSettle', {
            volume: params.volume * 0.5,
            pitch: params.pitch,
            fadeIn: 0.1,
            fadeOut: 0.2
        })
    }

    playRollComplete(results) {
        this.playSound('rollComplete', {
            volume: 0.8,
            pitch: 1.0,
            useReverb: true
        })

        // Check for critical results
        results.forEach(result => {
            if (result.result === result.sides) {
                // Maximum roll
                this.playSound('criticalHit', {
                    volume: 0.9,
                    delay: 0.2,
                    useReverb: true
                })
            } else if (result.result === 1 && result.sides === 20) {
                // Natural 1 on d20
                this.playSound('criticalMiss', {
                    volume: 0.7,
                    delay: 0.2
                })
            }
        })
    }

    playUISound(action) {
        const uiSounds = {
            click: { sound: 'uiClick', volume: 0.3 },
            hover: { sound: 'uiHover', volume: 0.2 },
            modalOpen: { sound: 'modalOpen', volume: 0.6 },
            modalClose: { sound: 'modalClose', volume: 0.5 },
            diceAdd: { sound: 'diceAdd', volume: 0.4 },
            diceRemove: { sound: 'diceRemove', volume: 0.4 }
        }

        const config = uiSounds[action]
        if (config) {
            this.playSound(config.sound, {
                volume: config.volume,
                pitch: 0.9 + Math.random() * 0.2
            })
        }
    }

    play3DSound(soundKey, position, listenerPosition = { x: 0, y: 0, z: 0 }, options = {}) {
        if (!this.isEnabled || !this.isInitialized) return

        // Calculate 3D audio parameters
        const distance = Math.sqrt(
            Math.pow(position.x - listenerPosition.x, 2) +
            Math.pow(position.y - listenerPosition.y, 2) +
            Math.pow(position.z - listenerPosition.z, 2)
        )

        // Calculate volume based on distance
        const maxDistance = 20
        const volumeMultiplier = Math.max(0, 1 - distance / maxDistance)

        // Calculate pan based on horizontal position
        const pan = Math.max(-1, Math.min(1, (position.x - listenerPosition.x) / 10))

        this.playSound(soundKey, {
            ...options,
            volume: (options.volume || 1.0) * volumeMultiplier,
            pan: pan
        })
    }

    startAmbientLoop() {
        if (this.ambientSource) {
            this.stopAmbientLoop()
        }

        this.ambientSource = this.playSound('ambientMagic', {
            volume: 0.1,
            loop: true,
            fadeIn: 2.0,
            useReverb: true
        })
    }

    stopAmbientLoop() {
        if (this.ambientSource) {
            const gainNode = this.audioContext.createGain()
            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime)
            gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + 1.0)

            setTimeout(() => {
                if (this.ambientSource) {
                    this.ambientSource.stop()
                    this.ambientSource = null
                }
            }, 1000)
        }
    }

    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume))
        if (this.masterGain) {
            this.masterGain.gain.value = this.volume
        }
    }

    setEnabled(enabled) {
        this.isEnabled = enabled
        if (!enabled) {
            this.stopAmbientLoop()
        }
    }

    // Utility method to create custom sound effects
    createCustomEffect(params) {
        const {
            type = 'sine',
            frequency = 440,
            duration = 0.5,
            volume = 0.5,
            envelope = 'linear',
            filterType = 'lowpass',
            filterFreq = 2000
        } = params

        if (!this.isInitialized) return

        const oscillator = this.audioContext.createOscillator()
        const gainNode = this.audioContext.createGain()
        const filter = this.audioContext.createBiquadFilter()

        oscillator.type = type
        oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime)

        filter.type = filterType
        filter.frequency.setValueAtTime(filterFreq, this.audioContext.currentTime)

        const startTime = this.audioContext.currentTime
        const endTime = startTime + duration

        // Apply envelope
        if (envelope === 'linear') {
            gainNode.gain.setValueAtTime(0, startTime)
            gainNode.gain.linearRampToValueAtTime(volume, startTime + 0.01)
            gainNode.gain.linearRampToValueAtTime(0, endTime)
        } else if (envelope === 'exponential') {
            gainNode.gain.setValueAtTime(volume, startTime)
            gainNode.gain.exponentialRampToValueAtTime(0.001, endTime)
        }

        oscillator.connect(filter)
        filter.connect(gainNode)
        gainNode.connect(this.compressor)

        oscillator.start(startTime)
        oscillator.stop(endTime)

        return oscillator
    }

    destroy() {
        this.stopAmbientLoop()

        if (this.audioContext) {
            this.audioContext.close()
        }

        this.sounds.clear()
        this.isInitialized = false
    }
}

export default DiceSoundSystem