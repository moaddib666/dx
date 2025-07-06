import * as THREE from 'three'
import { markRaw } from 'vue'

export class D20MaterialService {
    constructor() {
        this.shaderUniforms = {}
        this.customShaders = {}
        this.materialPresets = this.initializeMaterialPresets()
        this.currentMaterialType = 'plastic'
        this.currentShaderType = 'none'
    }

    initializeMaterialPresets() {
        return {
            plastic: {
                type: 'MeshPhongMaterial',
                properties: {
                    shininess: 100,
                    transparent: true,
                    opacity: 0.95,
                    reflectivity: 0.3,
                    specular: 0x222222
                }
            },
            metal: {
                type: 'MeshStandardMaterial',
                properties: {
                    metalness: 0.8,
                    roughness: 0.2,
                    transparent: true,
                    opacity: 1.0,
                    envMapIntensity: 1.0
                }
            },
            glass: {
                type: 'MeshPhysicalMaterial',
                properties: {
                    metalness: 0.0,
                    roughness: 0.1,
                    transparent: true,
                    opacity: 0.7,
                    transmission: 0.8,
                    thickness: 0.5,
                    ior: 1.5
                }
            },
            stone: {
                type: 'MeshStandardMaterial',
                properties: {
                    metalness: 0.1,
                    roughness: 0.9,
                    transparent: false,
                    opacity: 1.0
                }
            }
        }
    }

    initializeShaders() {
        // Bloom shader
        this.customShaders.bloom = {
            uniforms: {
                tDiffuse: { value: null },
                bloomStrength: { value: 1.5 },
                bloomRadius: { value: 0.4 },
                bloomThreshold: { value: 0.85 }
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform sampler2D tDiffuse;
                uniform float bloomStrength;
                uniform float bloomRadius;
                uniform float bloomThreshold;
                varying vec2 vUv;
                
                void main() {
                    vec4 texel = texture2D(tDiffuse, vUv);
                    float brightness = dot(texel.rgb, vec3(0.2126, 0.7152, 0.0722));
                    
                    if(brightness > bloomThreshold) {
                        vec3 bloom = texel.rgb * bloomStrength;
                        gl_FragColor = vec4(bloom, texel.a);
                    } else {
                        gl_FragColor = texel;
                    }
                }
            `
        }

        // Fire shader
        this.customShaders.fire = {
            uniforms: {
                time: { value: 0.0 },
                intensity: { value: 1.0 },
                fireColor1: { value: new THREE.Color(0xff4500) },
                fireColor2: { value: new THREE.Color(0xffff00) },
                noiseScale: { value: 3.0 }
            },
            vertexShader: `
                varying vec2 vUv;
                varying vec3 vPosition;
                uniform float time;
                
                // Simple noise function
                float noise(vec2 p) {
                    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
                }
                
                void main() {
                    vUv = uv;
                    vPosition = position;
                    
                    // Add slight movement to vertices for fire effect
                    vec3 pos = position;
                    pos += normal * sin(time * 2.0 + position.y * 10.0) * 0.02;
                    
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                uniform float time;
                uniform float intensity;
                uniform vec3 fireColor1;
                uniform vec3 fireColor2;
                uniform float noiseScale;
                varying vec2 vUv;
                varying vec3 vPosition;
                
                float noise(vec2 p) {
                    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
                }
                
                void main() {
                    vec2 uv = vUv * noiseScale;
                    float n = noise(uv + time * 0.5);
                    n += 0.5 * noise(uv * 2.0 + time * 0.8);
                    n += 0.25 * noise(uv * 4.0 + time * 1.2);
                    n /= 1.75;
                    
                    vec3 color = mix(fireColor1, fireColor2, n);
                    color *= intensity * (0.8 + 0.4 * sin(time * 3.0 + vPosition.y * 5.0));
                    
                    gl_FragColor = vec4(color, 0.9);
                }
            `
        }

        // Metallic shader
        this.customShaders.metallic = {
            uniforms: {
                time: { value: 0.0 },
                metalness: { value: 0.9 },
                roughness: { value: 0.1 },
                reflectivity: { value: 1.0 },
                envMap: { value: null }
            },
            vertexShader: `
                varying vec2 vUv;
                varying vec3 vNormal;
                varying vec3 vViewPosition;
                
                void main() {
                    vUv = uv;
                    vNormal = normalize(normalMatrix * normal);
                    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                    vViewPosition = -mvPosition.xyz;
                    gl_Position = projectionMatrix * mvPosition;
                }
            `,
            fragmentShader: `
                uniform float time;
                uniform float metalness;
                uniform float roughness;
                uniform float reflectivity;
                varying vec2 vUv;
                varying vec3 vNormal;
                varying vec3 vViewPosition;
                
                void main() {
                    vec3 normal = normalize(vNormal);
                    vec3 viewDir = normalize(vViewPosition);
                    
                    // Simple metallic reflection
                    float fresnel = pow(1.0 - dot(normal, viewDir), 2.0);
                    vec3 reflection = reflect(-viewDir, normal);
                    
                    vec3 baseColor = vec3(0.7, 0.7, 0.8);
                    vec3 metallicColor = baseColor * (1.0 - roughness) + vec3(1.0) * roughness;
                    
                    float spec = pow(max(dot(normal, normalize(vec3(1.0, 1.0, 1.0))), 0.0), 32.0);
                    vec3 finalColor = metallicColor * metalness + spec * reflectivity;
                    
                    gl_FragColor = vec4(finalColor, 1.0);
                }
            `
        }
    }

    createMaterial(materialType, texture = null, shaderType = 'none') {
        const preset = this.materialPresets[materialType] || this.materialPresets.plastic
        let material

        // Handle shader materials
        if (shaderType !== 'none' && this.customShaders[shaderType]) {
            const shader = this.customShaders[shaderType]
            material = new THREE.ShaderMaterial({
                uniforms: { ...shader.uniforms },
                vertexShader: shader.vertexShader,
                fragmentShader: shader.fragmentShader,
                transparent: true
            })

            if (texture) {
                material.uniforms.tDiffuse = { value: texture }
            }
        } else {
            // Standard materials
            switch (preset.type) {
                case 'MeshStandardMaterial':
                    material = new THREE.MeshStandardMaterial(preset.properties)
                    break
                case 'MeshPhysicalMaterial':
                    material = new THREE.MeshPhysicalMaterial(preset.properties)
                    break
                case 'MeshPhongMaterial':
                default:
                    material = new THREE.MeshPhongMaterial(preset.properties)
                    break
            }

            if (texture) {
                material.map = texture
            }
        }

        return markRaw(material)
    }

    updateShaderUniforms(deltaTime) {
        // Update time-based shader uniforms
        Object.values(this.customShaders).forEach(shader => {
            if (shader.uniforms.time) {
                shader.uniforms.time.value += deltaTime
            }
        })
    }

    setMaterialType(type) {
        if (this.materialPresets[type]) {
            this.currentMaterialType = type
            return true
        }
        return false
    }

    setShaderType(type) {
        if (type === 'none' || this.customShaders[type]) {
            this.currentShaderType = type
            return true
        }
        return false
    }

    getMaterialTypes() {
        return Object.keys(this.materialPresets)
    }

    getShaderTypes() {
        return ['none', ...Object.keys(this.customShaders)]
    }

    getCurrentMaterialType() {
        return this.currentMaterialType
    }

    getCurrentShaderType() {
        return this.currentShaderType
    }

    // Create environment map for metallic materials
    createEnvironmentMap(renderer) {
        const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256, {
            format: THREE.RGBFormat,
            generateMipmaps: true,
            minFilter: THREE.LinearMipmapLinearFilter
        })

        const cubeCamera = new THREE.CubeCamera(1, 1000, cubeRenderTarget)
        return markRaw(cubeCamera.renderTarget.texture)
    }

    dispose() {
        // Dispose of any created textures or materials
        this.shaderUniforms = {}
        this.customShaders = {}
        this.currentMaterialType = 'plastic'
        this.currentShaderType = 'none'
    }
}

export default D20MaterialService