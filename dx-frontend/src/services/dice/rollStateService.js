import * as THREE from 'three'
import { markRaw } from 'vue'

export class RollStateService {
    constructor() {
        this.reset()
        this.callbacks = {
            onStateChange: null,
            onRollComplete: null,
            onNumberChange: null
        }
    }

    reset() {
        this.state = {
            position: markRaw(new THREE.Vector3(0, 1, 0)),
            rotation: markRaw(new THREE.Vector3()),
            angularVelocity: markRaw(new THREE.Vector3()),
            isRolling: false,
            rollTime: 0,
            minRollTime: 3.5,
            targetNumber: 20,
            isDeterministic: true,
            currentDisplayNumber: 1,
            numberChangeInterval: 0.15,
            lastNumberChange: 0,
            topFaceIndex: -1,
            baseSpeed: 1,
            currentSpeed: 1,
            canSettle: false,
            isSettling: false,
            settleStartTime: 0,
            status: 'Ready to roll'
        }
    }

    setCallbacks(callbacks) {
        this.callbacks = { ...this.callbacks, ...callbacks }
    }

    startRoll(targetNumber, isDeterministic = true) {
        this.state.targetNumber = targetNumber
        this.state.isDeterministic = isDeterministic
        this.state.rollTime = 0
        this.state.isRolling = true
        this.state.canSettle = false
        this.state.isSettling = false
        this.state.topFaceIndex = -1

        // Set initial rotation and velocity
        this.state.rotation.set(
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2
        )
        this.state.angularVelocity.set(8, 10, 6)
        this.state.lastNumberChange = 0
        this.state.currentDisplayNumber = Math.floor(Math.random() * 20) + 1
        this.state.numberChangeInterval = 0.12

        this.state.status = isDeterministic
            ? `Rolling for ${targetNumber}…`
            : "Rolling randomly…"

        this.notifyStateChange()
        return this.state
    }

    update(deltaTime, faceNumbers, faceNormals, calculateTargetRotation) {
        if (!this.state.isRolling) return this.state

        this.state.rollTime += deltaTime

        // Phase 1: Visual excitement phase
        if (this.state.rollTime < this.state.minRollTime) {
            this.updateExcitementPhase(deltaTime)
        } else {
            // Phase 2: Settling phase
            this.updateSettlingPhase(deltaTime, faceNumbers, faceNormals, calculateTargetRotation)
        }

        // Apply rotation
        this.state.rotation.add(
            this.state.angularVelocity.clone().multiplyScalar(deltaTime)
        )

        this.notifyStateChange()
        return this.state
    }

    updateExcitementPhase(deltaTime) {
        // Maintain high angular velocity for visual excitement
        this.state.angularVelocity.set(8, 10, 6)

        // Change displayed number rapidly
        if (this.state.rollTime - this.state.lastNumberChange > this.state.numberChangeInterval) {
            this.state.currentDisplayNumber = Math.floor(Math.random() * 20) + 1
            this.state.lastNumberChange = this.state.rollTime
            this.notifyNumberChange()
        }
    }

    updateSettlingPhase(deltaTime, faceNumbers, faceNormals, calculateTargetRotation) {
        if (!this.state.canSettle) {
            this.state.canSettle = true
            this.state.settleStartTime = this.state.rollTime
        }

        const settleTime = this.state.rollTime - this.state.settleStartTime

        // Gradually slow down
        const slowdown = Math.max(0.05, 1 - settleTime * 0.4)
        this.state.currentSpeed = this.state.baseSpeed * slowdown
        this.state.angularVelocity.multiplyScalar(slowdown)

        // Update display number with increasing bias toward target
        if (this.state.rollTime - this.state.lastNumberChange > this.state.numberChangeInterval) {
            const targetProbability = Math.min(0.9, settleTime * 0.6)
            this.state.currentDisplayNumber = Math.random() < targetProbability
                ? this.state.targetNumber
                : Math.floor(Math.random() * 20) + 1

            this.state.lastNumberChange = this.state.rollTime
            this.state.numberChangeInterval = 0.15 + settleTime * 0.1
            this.notifyNumberChange()
        }

        // Apply deterministic settling
        if (this.state.isDeterministic && settleTime > 0.3) {
            this.applyDeterministicSettling(settleTime, faceNumbers, calculateTargetRotation)
        }

        // Check for completion
        this.checkRollCompletion(settleTime)
    }

    applyDeterministicSettling(settleTime, faceNumbers, calculateTargetRotation) {
        const targetIndex = faceNumbers.indexOf(this.state.targetNumber)
        if (targetIndex !== -1) {
            const targetRotation = calculateTargetRotation(targetIndex)

            // Aggressive interpolation for complete settling
            // Use higher interpolation factor to ensure dice reach target rotation
            const lerpFactor = Math.min(0.3, settleTime * 0.2)  // Much more aggressive convergence

            this.state.rotation.x += (targetRotation.x - this.state.rotation.x) * lerpFactor
            this.state.rotation.y += (targetRotation.y - this.state.rotation.y) * lerpFactor
            this.state.rotation.z += (targetRotation.z - this.state.rotation.z) * lerpFactor
        }
    }

    checkRollCompletion(settleTime) {
        const slowEnough = this.state.currentSpeed < 0.3 && this.state.angularVelocity.length() < 2
        const timeout = settleTime > 5

        if (slowEnough || timeout) {
            this.completeRoll()
        }
    }

    completeRoll() {
        this.state.isRolling = false
        this.state.angularVelocity.set(0, 0, 0)

        const finalNumber = this.state.isDeterministic
            ? this.state.targetNumber
            : this.state.currentDisplayNumber

        this.state.currentDisplayNumber = finalNumber
        this.state.status = `Landed on ${finalNumber}`

        this.notifyRollComplete(finalNumber)
        this.notifyStateChange()
    }

    forceComplete() {
        if (this.state.isRolling) {
            this.completeRoll()
        }
    }

    getCurrentState() {
        return { ...this.state }
    }

    isCurrentlyRolling() {
        return this.state.isRolling
    }

    getCurrentNumber() {
        return this.state.currentDisplayNumber
    }

    getStatus() {
        return this.state.status
    }

    setMinRollTime(time) {
        this.state.minRollTime = Math.max(1.0, time)
    }

    notifyStateChange() {
        if (this.callbacks.onStateChange) {
            this.callbacks.onStateChange(this.state)
        }
    }

    notifyRollComplete(result) {
        if (this.callbacks.onRollComplete) {
            this.callbacks.onRollComplete({
                number: result,
                isDeterministic: this.state.isDeterministic,
                targetNumber: this.state.targetNumber,
                rollTime: this.state.rollTime
            })
        }
    }

    notifyNumberChange() {
        if (this.callbacks.onNumberChange) {
            this.callbacks.onNumberChange(this.state.currentDisplayNumber)
        }
    }

    dispose() {
        this.reset()
        this.callbacks = {
            onStateChange: null,
            onRollComplete: null,
            onNumberChange: null
        }
    }
}

export default RollStateService