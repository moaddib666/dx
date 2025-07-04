import * as THREE from 'three'

export class DicePhysics {
    constructor() {
        this.gravity = -9.8
        this.bounceRestitution = 0.6
        this.friction = 0.95
        this.angularDamping = 0.98
        this.groundY = 0
        this.boundaries = {
            x: { min: -10, max: 10 },
            z: { min: -8, max: 8 }
        }
    }

    createPhysicsBody(mesh, diceType) {
        const body = {
            mesh: mesh,
            position: mesh.position.clone(),
            velocity: new THREE.Vector3(),
            angularVelocity: new THREE.Euler(),
            mass: this.getDiceMass(diceType),
            radius: this.getDiceRadius(diceType),
            isResting: false,
            restingTime: 0,
            lastPosition: mesh.position.clone(),
            diceType: diceType
        }

        return body
    }

    getDiceMass(diceType) {
        const masses = {
            'd4': 0.5,
            'd6': 1.0,
            'd8': 0.8,
            'd10': 0.9,
            'd12': 1.2,
            'd20': 1.1,
            'd100': 1.0
        }
        return masses[diceType] || 1.0
    }

    getDiceRadius(diceType) {
        const radii = {
            'd4': 1.0,
            'd6': 0.75,
            'd8': 1.0,
            'd10': 0.8,
            'd12': 1.0,
            'd20': 1.1,
            'd100': 1.0
        }
        return radii[diceType] || 1.0
    }

    initializeRoll(body, throwForce = 5) {
        // Reset physics state
        body.isResting = false
        body.restingTime = 0

        // Set initial position slightly above ground
        body.position.y = 3 + Math.random() * 2
        body.mesh.position.copy(body.position)

        // Apply random throw velocity
        body.velocity.set(
            (Math.random() - 0.5) * throwForce,
            Math.random() * throwForce + 2,
            (Math.random() - 0.5) * throwForce
        )

        // Apply random angular velocity
        body.angularVelocity.set(
            (Math.random() - 0.5) * 15,
            (Math.random() - 0.5) * 15,
            (Math.random() - 0.5) * 15
        )

        // Add some spin based on dice type
        const spinMultiplier = this.getSpinMultiplier(body.diceType)
        body.angularVelocity.x *= spinMultiplier
        body.angularVelocity.y *= spinMultiplier
        body.angularVelocity.z *= spinMultiplier
    }

    getSpinMultiplier(diceType) {
        const multipliers = {
            'd4': 1.5,  // Tetrahedron spins more
            'd6': 1.0,  // Standard
            'd8': 1.2,  // Octahedron spins well
            'd10': 0.8, // Less stable
            'd12': 0.9, // Heavy, spins less
            'd20': 1.1, // Good spinner
            'd100': 0.7 // Sphere, different physics
        }
        return multipliers[diceType] || 1.0
    }

    update(bodies, deltaTime) {
        bodies.forEach(body => {
            if (body.isResting) {
                this.updateRestingBody(body, deltaTime)
                return
            }

            this.updatePhysics(body, deltaTime)
            this.checkCollisions(body, bodies)
            this.updateMesh(body)
            this.checkIfResting(body, deltaTime)
        })
    }

    updatePhysics(body, deltaTime) {
        // Store last position for collision detection
        body.lastPosition.copy(body.position)

        // Apply gravity
        body.velocity.y += this.gravity * deltaTime

        // Update position
        body.position.add(body.velocity.clone().multiplyScalar(deltaTime))

        // Apply air resistance
        body.velocity.multiplyScalar(Math.pow(0.999, deltaTime * 60))

        // Update rotation
        body.mesh.rotation.x += body.angularVelocity.x * deltaTime
        body.mesh.rotation.y += body.angularVelocity.y * deltaTime
        body.mesh.rotation.z += body.angularVelocity.z * deltaTime

        // Apply angular damping
        body.angularVelocity.x *= Math.pow(this.angularDamping, deltaTime * 60)
        body.angularVelocity.y *= Math.pow(this.angularDamping, deltaTime * 60)
        body.angularVelocity.z *= Math.pow(this.angularDamping, deltaTime * 60)

        // Check ground collision
        if (body.position.y - body.radius <= this.groundY) {
            this.handleGroundCollision(body)
        }

        // Check boundary collisions
        this.handleBoundaryCollisions(body)
    }

    handleGroundCollision(body) {
        body.position.y = this.groundY + body.radius

        if (body.velocity.y < 0) {
            // Bounce with energy loss
            body.velocity.y = -body.velocity.y * this.bounceRestitution

            // Apply friction to horizontal movement
            body.velocity.x *= this.friction
            body.velocity.z *= this.friction

            // Transfer some linear momentum to angular momentum
            const impactForce = Math.abs(body.velocity.y)
            body.angularVelocity.x += (Math.random() - 0.5) * impactForce * 0.5
            body.angularVelocity.z += (Math.random() - 0.5) * impactForce * 0.5

            // Create bounce effect based on dice type
            this.createBounceEffect(body, impactForce)
        }
    }

    createBounceEffect(body, impactForce) {
        // Different bounce characteristics for different dice
        switch (body.diceType) {
            case 'd4':
                // Tetrahedron - tends to settle quickly
                body.angularVelocity.multiplyScalar(0.8)
                break
            case 'd6':
                // Cube - standard bounce
                break
            case 'd8':
                // Octahedron - more bouncy
                body.velocity.y *= 1.1
                break
            case 'd10':
                // Pentagonal - unstable, more rolling
                body.angularVelocity.y += (Math.random() - 0.5) * impactForce
                break
            case 'd12':
                // Dodecahedron - many faces, more rolling
                body.angularVelocity.multiplyScalar(1.2)
                break
            case 'd20':
                // Icosahedron - very bouncy
                body.velocity.y *= 1.2
                body.angularVelocity.multiplyScalar(1.1)
                break
            case 'd100':
                // Sphere - keeps rolling
                body.angularVelocity.y += (Math.random() - 0.5) * impactForce * 1.5
                break
        }
    }

    handleBoundaryCollisions(body) {
        let collided = false

        // X boundaries
        if (body.position.x - body.radius <= this.boundaries.x.min) {
            body.position.x = this.boundaries.x.min + body.radius
            body.velocity.x = Math.abs(body.velocity.x) * this.bounceRestitution
            collided = true
        } else if (body.position.x + body.radius >= this.boundaries.x.max) {
            body.position.x = this.boundaries.x.max - body.radius
            body.velocity.x = -Math.abs(body.velocity.x) * this.bounceRestitution
            collided = true
        }

        // Z boundaries
        if (body.position.z - body.radius <= this.boundaries.z.min) {
            body.position.z = this.boundaries.z.min + body.radius
            body.velocity.z = Math.abs(body.velocity.z) * this.bounceRestitution
            collided = true
        } else if (body.position.z + body.radius >= this.boundaries.z.max) {
            body.position.z = this.boundaries.z.max - body.radius
            body.velocity.z = -Math.abs(body.velocity.z) * this.bounceRestitution
            collided = true
        }

        if (collided) {
            // Add some random angular momentum on wall hit
            body.angularVelocity.x += (Math.random() - 0.5) * 5
            body.angularVelocity.y += (Math.random() - 0.5) * 5
            body.angularVelocity.z += (Math.random() - 0.5) * 5
        }
    }

    checkCollisions(body, allBodies) {
        allBodies.forEach(otherBody => {
            if (body === otherBody) return

            const distance = body.position.distanceTo(otherBody.position)
            const minDistance = body.radius + otherBody.radius

            if (distance < minDistance) {
                this.resolveCollision(body, otherBody, distance, minDistance)
            }
        })
    }

    resolveCollision(body1, body2, distance, minDistance) {
        // Calculate collision normal
        const normal = new THREE.Vector3()
            .subVectors(body1.position, body2.position)
            .normalize()

        // Separate overlapping dice
        const overlap = minDistance - distance
        const separation = normal.clone().multiplyScalar(overlap * 0.5)

        body1.position.add(separation)
        body2.position.sub(separation)

        // Calculate relative velocity
        const relativeVelocity = new THREE.Vector3()
            .subVectors(body1.velocity, body2.velocity)

        const velocityAlongNormal = relativeVelocity.dot(normal)

        // Don't resolve if velocities are separating
        if (velocityAlongNormal > 0) return

        // Calculate restitution (bounciness)
        const restitution = this.bounceRestitution

        // Calculate impulse scalar
        const impulseScalar = -(1 + restitution) * velocityAlongNormal
        const totalMass = body1.mass + body2.mass
        const impulse = normal.clone().multiplyScalar(impulseScalar / totalMass)

        // Apply impulse
        body1.velocity.add(impulse.clone().multiplyScalar(body2.mass))
        body2.velocity.sub(impulse.clone().multiplyScalar(body1.mass))

        // Add rotational effects
        const impactForce = Math.abs(impulseScalar)
        body1.angularVelocity.x += (Math.random() - 0.5) * impactForce * 0.3
        body1.angularVelocity.y += (Math.random() - 0.5) * impactForce * 0.3
        body1.angularVelocity.z += (Math.random() - 0.5) * impactForce * 0.3

        body2.angularVelocity.x += (Math.random() - 0.5) * impactForce * 0.3
        body2.angularVelocity.y += (Math.random() - 0.5) * impactForce * 0.3
        body2.angularVelocity.z += (Math.random() - 0.5) * impactForce * 0.3
    }

    updateMesh(body) {
        body.mesh.position.copy(body.position)
    }

    checkIfResting(body, deltaTime) {
        const velocityThreshold = 0.1
        const angularThreshold = 0.5
        const restingTimeRequired = 0.5 // seconds

        const isMovingSlow = body.velocity.length() < velocityThreshold
        const isRotatingSlow = Math.abs(body.angularVelocity.x) < angularThreshold &&
            Math.abs(body.angularVelocity.y) < angularThreshold &&
            Math.abs(body.angularVelocity.z) < angularThreshold
        const isNearGround = Math.abs(body.position.y - (this.groundY + body.radius)) < 0.1

        if (isMovingSlow && isRotatingSlow && isNearGround) {
            body.restingTime += deltaTime
            if (body.restingTime >= restingTimeRequired) {
                body.isResting = true
                body.velocity.set(0, 0, 0)
                body.angularVelocity.set(0, 0, 0)
                body.position.y = this.groundY + body.radius
                this.snapToFinalRotation(body)
            }
        } else {
            body.restingTime = 0
        }
    }

    snapToFinalRotation(body) {
        // Calculate which face is pointing up
        const upVector = new THREE.Vector3(0, 1, 0)
        const faces = this.getDiceFaces(body.diceType)

        let bestFace = null
        let bestDot = -1

        faces.forEach(face => {
            const faceNormal = face.normal.clone()
            faceNormal.applyEuler(body.mesh.rotation)
            const dot = faceNormal.dot(upVector)

            if (dot > bestDot) {
                bestDot = dot
                bestFace = face
            }
        })

        if (bestFace) {
            // Store the result
            body.result = bestFace.value

            // Smoothly rotate to show the face properly
            this.animateToFinalRotation(body, bestFace.rotation)
        }
    }

    getDiceFaces(diceType) {
        // Simplified face definitions - in a real implementation,
        // you'd have precise face normals and rotations for each dice type
        const faces = {
            'd4': [
                { value: 1, normal: new THREE.Vector3(0, 1, 0), rotation: new THREE.Euler(0, 0, 0) },
                { value: 2, normal: new THREE.Vector3(1, 1, 1).normalize(), rotation: new THREE.Euler(Math.PI/3, 0, 0) },
                { value: 3, normal: new THREE.Vector3(-1, 1, 1).normalize(), rotation: new THREE.Euler(Math.PI/3, Math.PI*2/3, 0) },
                { value: 4, normal: new THREE.Vector3(0, 1, -1).normalize(), rotation: new THREE.Euler(Math.PI/3, Math.PI*4/3, 0) }
            ],
            'd6': [
                { value: 1, normal: new THREE.Vector3(0, 1, 0), rotation: new THREE.Euler(0, 0, 0) },
                { value: 2, normal: new THREE.Vector3(0, 0, 1), rotation: new THREE.Euler(Math.PI/2, 0, 0) },
                { value: 3, normal: new THREE.Vector3(1, 0, 0), rotation: new THREE.Euler(0, 0, -Math.PI/2) },
                { value: 4, normal: new THREE.Vector3(-1, 0, 0), rotation: new THREE.Euler(0, 0, Math.PI/2) },
                { value: 5, normal: new THREE.Vector3(0, 0, -1), rotation: new THREE.Euler(-Math.PI/2, 0, 0) },
                { value: 6, normal: new THREE.Vector3(0, -1, 0), rotation: new THREE.Euler(Math.PI, 0, 0) }
            ]
            // Add other dice types as needed
        }

        return faces[diceType] || faces['d6']
    }

    animateToFinalRotation(body, targetRotation) {
        const startRotation = body.mesh.rotation.clone()
        const startTime = Date.now()
        const duration = 300 // ms

        const animate = () => {
            const elapsed = Date.now() - startTime
            const progress = Math.min(elapsed / duration, 1)
            const eased = 1 - Math.pow(1 - progress, 3) // Ease out cubic

            body.mesh.rotation.x = startRotation.x + (targetRotation.x - startRotation.x) * eased
            body.mesh.rotation.y = startRotation.y + (targetRotation.y - startRotation.y) * eased
            body.mesh.rotation.z = startRotation.z + (targetRotation.z - startRotation.z) * eased

            if (progress < 1) {
                requestAnimationFrame(animate)
            }
        }

        animate()
    }

    updateRestingBody(body, deltaTime) {
        // Keep resting dice stable
        body.position.y = this.groundY + body.radius
        body.velocity.set(0, 0, 0)
        body.angularVelocity.set(0, 0, 0)
    }

    getAllRestingBodies(bodies) {
        return bodies.filter(body => body.isResting)
    }

    areAllDiceResting(bodies) {
        return bodies.length > 0 && bodies.every(body => body.isResting)
    }

    resetBody(body) {
        body.isResting = false
        body.restingTime = 0
        body.result = null
        body.velocity.set(0, 0, 0)
        body.angularVelocity.set(0, 0, 0)
    }
}

export default DicePhysics