import * as THREE from 'three'

export class DiceShaders {
    static getDiceVertexShader() {
        return `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      varying vec3 vWorldPosition;
      varying vec3 vViewPosition;
      
      uniform float time;
      uniform float isRolling;
      uniform float resultGlow;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = position;
        vUv = uv;
        
        vec4 worldPosition = modelMatrix * vec4(position, 1.0);
        vWorldPosition = worldPosition.xyz;
        
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        vViewPosition = -mvPosition.xyz;
        
        vec3 pos = position;
        
        // Add subtle wobble during rolling
        if (isRolling > 0.5) {
          float wobble = sin(time * 15.0 + worldPosition.x * 5.0) * 0.01;
          pos += normal * wobble;
        }
        
        // Result highlight expansion
        if (resultGlow > 0.1) {
          pos += normal * resultGlow * 0.02;
        }
        
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `
    }

    static getDiceFragmentShader() {
        return `
      uniform vec3 baseColor;
      uniform float glowIntensity;
      uniform float time;
      uniform float isRolling;
      uniform float resultGlow;
      uniform sampler2D numberTexture;
      uniform float currentNumber;
      uniform float maxNumber;
      
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      varying vec3 vWorldPosition;
      varying vec3 vViewPosition;
      
      // Noise function for procedural effects
      float random(vec2 st) {
        return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
      }
      
      float noise(vec2 st) {
        vec2 i = floor(st);
        vec2 f = fract(st);
        
        float a = random(i);
        float b = random(i + vec2(1.0, 0.0));
        float c = random(i + vec2(0.0, 1.0));
        float d = random(i + vec2(1.0, 1.0));
        
        vec2 u = f * f * (3.0 - 2.0 * f);
        
        return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
      }
      
      // Create procedural numbers
      float createNumber(vec2 uv, float number) {
        vec2 center = vec2(0.5, 0.5);
        vec2 pos = uv - center;
        float dist = length(pos);
        
        // Base circle for number background
        float circle = 1.0 - smoothstep(0.15, 0.25, dist);
        
        // Create number patterns based on value
        float numberPattern = 0.0;
        
        if (number >= 1.0 && number < 2.0) {
          // Number 1 - vertical line
          numberPattern = 1.0 - smoothstep(0.02, 0.06, abs(pos.x));
        } else if (number >= 2.0 && number < 3.0) {
          // Number 2 - S curve
          float curve = sin(pos.y * 8.0 + pos.x * 4.0) * 0.1;
          numberPattern = 1.0 - smoothstep(0.02, 0.06, abs(pos.x - curve));
        } else if (number >= 3.0 && number < 4.0) {
          // Number 3 - double curve
          float curve1 = sin(pos.y * 6.0) * 0.08;
          float curve2 = sin(pos.y * 6.0 + 3.14159) * 0.08;
          numberPattern = max(
            1.0 - smoothstep(0.02, 0.05, abs(pos.x - curve1)),
            1.0 - smoothstep(0.02, 0.05, abs(pos.x - curve2))
          );
        } else if (number >= 4.0 && number < 5.0) {
          // Number 4 - two lines forming 4
          float vertical = 1.0 - smoothstep(0.02, 0.05, abs(pos.x + 0.1));
          float horizontal = 1.0 - smoothstep(0.02, 0.05, abs(pos.y));
          numberPattern = max(vertical, horizontal * step(-0.1, pos.x));
        } else if (number >= 5.0 && number < 6.0) {
          // Number 5 - complex shape
          float top = 1.0 - smoothstep(0.02, 0.05, abs(pos.y - 0.1)) * step(-0.15, pos.x) * step(pos.x, 0.15);
          float middle = 1.0 - smoothstep(0.02, 0.05, abs(pos.y)) * step(-0.15, pos.x) * step(pos.x, 0.0);
          float vertical = 1.0 - smoothstep(0.02, 0.05, abs(pos.x + 0.1)) * step(0.0, pos.y);
          numberPattern = max(max(top, middle), vertical);
        } else if (number >= 6.0 && number < 7.0) {
          // Number 6 - circle with gap
          float mainCircle = 1.0 - smoothstep(0.12, 0.18, dist);
          float innerCircle = smoothstep(0.06, 0.10, dist);
          float gap = step(0.0, pos.y) * step(pos.x, 0.05);
          numberPattern = mainCircle * innerCircle * (1.0 - gap);
        } else {
          // Default pattern for higher numbers
          float pattern = sin(pos.x * 20.0) * sin(pos.y * 20.0);
          numberPattern = smoothstep(0.3, 0.7, pattern) * circle;
        }
        
        return numberPattern * circle;
      }
      
      void main() {
        vec3 color = baseColor;
        vec3 normal = normalize(vNormal);
        vec3 viewDir = normalize(vViewPosition);
        
        // Fresnel effect for edge highlighting
        float fresnel = 1.0 - abs(dot(normal, viewDir));
        fresnel = pow(fresnel, 2.0);
        
        // Base lighting
        vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
        float diff = max(dot(normal, lightDir), 0.0);
        color *= (0.3 + 0.7 * diff);
        
        // Add base material properties
        color += fresnel * 0.2 * vec3(1.0, 1.0, 1.0);
        
        // Rolling shimmer effect
        if (isRolling > 0.5) {
          float shimmer = noise(vUv * 20.0 + time * 2.0) * 0.3;
          shimmer += sin(vWorldPosition.x * 10.0 + time * 8.0) * 0.2;
          color += shimmer * vec3(0.8, 0.9, 1.0);
          
          // Add energy crackling during roll
          float energy = noise(vUv * 50.0 + time * 5.0);
          energy = smoothstep(0.7, 1.0, energy);
          color += energy * vec3(0.5, 0.8, 1.0);
        }
        
        // Number rendering
        float numberGlow = 0.0;
        if (currentNumber > 0.0) {
          float numberMask = createNumber(vUv, currentNumber);
          
          // Fade numbers during rolling
          float numberOpacity = isRolling > 0.5 ? 0.2 : 1.0;
          
          // Glow effect for result numbers
          if (resultGlow > 0.1) {
            numberGlow = numberMask * resultGlow;
            color += numberGlow * vec3(1.0, 1.0, 0.3);
            
            // Add pulsing effect
            float pulse = sin(time * 6.0) * 0.5 + 0.5;
            color += numberMask * pulse * resultGlow * vec3(1.0, 0.8, 0.0);
          }
          
          // Regular number visibility
          color = mix(color, vec3(0.1, 0.1, 0.1), numberMask * numberOpacity * 0.8);
          color += numberMask * numberOpacity * vec3(1.0, 1.0, 1.0) * 0.6;
        }
        
        // Global glow effect
        if (glowIntensity > 0.1) {
          color += fresnel * glowIntensity * vec3(1.0, 1.0, 1.0);
          
          // Add rim lighting
          float rim = 1.0 - abs(dot(normal, viewDir));
          rim = pow(rim, 4.0);
          color += rim * glowIntensity * baseColor * 2.0;
        }
        
        // Result highlight
        if (resultGlow > 0.1) {
          // Add golden highlight
          vec3 goldColor = vec3(1.0, 0.8, 0.2);
          color = mix(color, goldColor, resultGlow * 0.3);
          
          // Add sparkle effect
          float sparkle = noise(vUv * 100.0 + time * 3.0);
          sparkle = smoothstep(0.8, 1.0, sparkle);
          color += sparkle * resultGlow * vec3(1.0, 1.0, 0.5);
        }
        
        // Atmospheric perspective
        float fogFactor = 1.0 - exp(-0.01 * length(vViewPosition));
        color = mix(color, vec3(0.05, 0.05, 0.15), fogFactor * 0.3);
        
        gl_FragColor = vec4(color, 1.0);
      }
    `
    }

    static getPostProcessingVertexShader() {
        return `
      varying vec2 vUv;
      
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `
    }

    static getPostProcessingFragmentShader() {
        return `
      uniform sampler2D tDiffuse;
      uniform float bloomStrength;
      uniform float exposure;
      uniform vec2 resolution;
      
      varying vec2 vUv;
      
      vec3 bloom(vec2 uv, sampler2D tex) {
        vec3 color = vec3(0.0);
        float total = 0.0;
        
        for (int i = -4; i <= 4; i++) {
          for (int j = -4; j <= 4; j++) {
            vec2 offset = vec2(float(i), float(j)) / resolution;
            float weight = exp(-float(i*i + j*j) / 8.0);
            color += texture2D(tex, uv + offset).rgb * weight;
            total += weight;
          }
        }
        
        return color / total;
      }
      
      void main() {
        vec3 color = texture2D(tDiffuse, vUv).rgb;
        
        // Extract bright areas
        vec3 bright = max(color - vec3(0.8), vec3(0.0));
        
        // Apply bloom
        vec3 bloomColor = bloom(vUv, tDiffuse);
        color += bloomColor * bright * bloomStrength;
        
        // Tone mapping
        color = vec3(1.0) - exp(-color * exposure);
        
        // Gamma correction
        color = pow(color, vec3(1.0 / 2.2));
        
        gl_FragColor = vec4(color, 1.0);
      }
    `
    }

    static createDiceMaterial(diceType, color) {
        const material = new THREE.ShaderMaterial({
            uniforms: {
                baseColor: { value: new THREE.Color(color) },
                glowIntensity: { value: 0.0 },
                time: { value: 0.0 },
                isRolling: { value: 0.0 },
                resultGlow: { value: 0.0 },
                currentNumber: { value: 0.0 },
                maxNumber: { value: this.getMaxNumber(diceType) },
                numberTexture: { value: null }
            },
            vertexShader: this.getDiceVertexShader(),
            fragmentShader: this.getDiceFragmentShader(),
            transparent: true,
            side: THREE.DoubleSide
        })

        return material
    }

    static getMaxNumber(diceType) {
        const maxNumbers = {
            'd4': 4,
            'd6': 6,
            'd8': 8,
            'd10': 10,
            'd12': 12,
            'd20': 20,
            'd100': 100
        }
        return maxNumbers[diceType] || 6
    }

    static createNumberTexture(number, size = 256) {
        const canvas = document.createElement('canvas')
        canvas.width = size
        canvas.height = size
        const ctx = canvas.getContext('2d')

        // Clear background
        ctx.fillStyle = 'rgba(0, 0, 0, 0)'
        ctx.fillRect(0, 0, size, size)

        // Draw number
        ctx.fillStyle = 'white'
        ctx.font = `bold ${size * 0.6}px Arial`
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(number.toString(), size / 2, size / 2)

        // Add glow effect
        ctx.shadowColor = 'white'
        ctx.shadowBlur = 20
        ctx.fillText(number.toString(), size / 2, size / 2)

        const texture = new THREE.CanvasTexture(canvas)
        texture.needsUpdate = true
        return texture
    }

    static createParticleSystem() {
        const particleCount = 100
        const geometry = new THREE.BufferGeometry()
        const positions = new Float32Array(particleCount * 3)
        const colors = new Float32Array(particleCount * 3)
        const sizes = new Float32Array(particleCount)

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 20
            positions[i * 3 + 1] = Math.random() * 10
            positions[i * 3 + 2] = (Math.random() - 0.5) * 20

            colors[i * 3] = Math.random()
            colors[i * 3 + 1] = Math.random()
            colors[i * 3 + 2] = Math.random()

            sizes[i] = Math.random() * 2 + 1
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1))

        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0.0 }
            },
            vertexShader: `
        uniform float time;
        attribute float size;
        varying vec3 vColor;
        
        void main() {
          vColor = color;
          vec3 pos = position;
          pos.y += sin(time + position.x) * 2.0;
          
          vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
          gl_PointSize = size * (300.0 / -mvPosition.z);
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
            fragmentShader: `
        varying vec3 vColor;
        
        void main() {
          float dist = distance(gl_PointCoord, vec2(0.5));
          if (dist > 0.5) discard;
          
          float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
          gl_FragColor = vec4(vColor, alpha * 0.6);
        }
      `,
            transparent: true,
            vertexColors: true
        })

        return new THREE.Points(geometry, material)
    }
}

export default DiceShaders