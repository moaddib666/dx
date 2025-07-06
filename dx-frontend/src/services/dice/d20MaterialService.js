import * as THREE from 'three'
import { markRaw } from 'vue'

export class D20MaterialService {
    constructor() {
        this.shaderUniforms = {}
        this.customShaders = {}
        this.materialPresets = this.initializeMaterialPresets()
        this.currentMaterialType = 'metal'
        this.currentShaderType = 'none'
    }

    initializeMaterialPresets() {
        return {
            metal: {
                type: 'MeshStandardMaterial',
                properties: {
                    metalness: 0.9,
                    roughness: 0.1,
                    transparent: true,
                    opacity: 0.98,
                    envMapIntensity: 1.5
                }
            }
        }
    }

    initializeShaders() {
        // Bloom shader - only affects near-white colors
        this.customShaders.bloom = {
            uniforms: {
                map: { value: null },
                bloomStrength: { value: 0.8 },
                bloomThreshold: { value: 0.9 },
                time: { value: 0.0 }
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
                uniform sampler2D map;
                uniform float bloomStrength;
                uniform float bloomThreshold;
                uniform float time;
                varying vec2 vUv;
                varying vec3 vNormal;
                varying vec3 vViewPosition;
                
                void main() {
                    vec4 texel = texture2D(map, vUv);
                    
                    // Calculate brightness (luminance)
                    float brightness = dot(texel.rgb, vec3(0.299, 0.587, 0.114));
                    
                    // Only apply bloom to near-white colors
                    if(brightness > bloomThreshold) {
                        float bloomFactor = (brightness - bloomThreshold) / (1.0 - bloomThreshold);
                        vec3 bloom = texel.rgb * (1.0 + bloomStrength * bloomFactor);
                        
                        // Add subtle pulsing effect
                        float pulse = 1.0 + 0.1 * sin(time * 3.0);
                        bloom *= pulse;
                        
                        texel.rgb = bloom;
                    }
                    
                    // Metallic properties
                    vec3 normal = normalize(vNormal);
                    vec3 viewDir = normalize(vViewPosition);
                    float fresnel = pow(1.0 - max(dot(normal, viewDir), 0.0), 3.0);
                    
                    // Add metallic reflection
                    texel.rgb = mix(texel.rgb, texel.rgb * 1.5, fresnel * 0.3);
                    
                    gl_FragColor = vec4(texel.rgb, texel.a);
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
                material.uniforms.map = { value: texture }
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
        this.currentMaterialType = 'metal'
        this.currentShaderType = 'none'
    }
}

export default D20MaterialService