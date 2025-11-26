/**
 * Perlin Noise implementation for fog of war masking
 * Creates seamless noise patterns for infinite map appearance
 */

export class PerlinNoise {
  private permutation: number[]
  private p: number[]

  constructor(seed?: number) {
    // Initialize permutation table
    this.permutation = []
    for (let i = 0; i < 256; i++) {
      this.permutation[i] = i
    }

    // Shuffle the permutation table using seed
    if (seed !== undefined) {
      this.seedRandom(seed)
    }

    // Shuffle array
    for (let i = this.permutation.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[this.permutation[i], this.permutation[j]] = [this.permutation[j], this.permutation[i]]
    }

    // Duplicate the permutation table
    this.p = new Array(512)
    for (let i = 0; i < 512; i++) {
      this.p[i] = this.permutation[i % 256]
    }
  }

  private seedRandom(seed: number) {
    let m = 0x80000000 // 2**31
    let a = 1103515245
    let c = 12345
    let state = seed

    Math.random = () => {
      state = (a * state + c) % m
      return state / (m - 1)
    }
  }

  private fade(t: number): number {
    return t * t * t * (t * (t * 6 - 15) + 10)
  }

  private lerp(t: number, a: number, b: number): number {
    return a + t * (b - a)
  }

  private grad(hash: number, x: number, y: number): number {
    const h = hash & 15
    const u = h < 8 ? x : y
    const v = h < 4 ? y : h === 12 || h === 14 ? x : 0
    return ((h & 1) === 0 ? u : -u) + ((h & 2) === 0 ? v : -v)
  }

  /**
   * Generate 2D Perlin noise value at given coordinates
   * @param x X coordinate
   * @param y Y coordinate
   * @returns Noise value between -1 and 1
   */
  noise2D(x: number, y: number): number {
    const X = Math.floor(x) & 255
    const Y = Math.floor(y) & 255

    x -= Math.floor(x)
    y -= Math.floor(y)

    const u = this.fade(x)
    const v = this.fade(y)

    const A = this.p[X] + Y
    const AA = this.p[A]
    const AB = this.p[A + 1]
    const B = this.p[X + 1] + Y
    const BA = this.p[B]
    const BB = this.p[B + 1]

    return this.lerp(
      v,
      this.lerp(u, this.grad(this.p[AA], x, y), this.grad(this.p[BA], x - 1, y)),
      this.lerp(u, this.grad(this.p[AB], x, y - 1), this.grad(this.p[BB], x - 1, y - 1))
    )
  }

  /**
   * Generate fractal noise with multiple octaves
   * @param x X coordinate
   * @param y Y coordinate
   * @param octaves Number of octaves
   * @param persistence Amplitude multiplier for each octave
   * @param scale Scale factor for coordinates
   * @returns Noise value between -1 and 1
   */
  fractalNoise2D(
    x: number,
    y: number,
    octaves: number = 4,
    persistence: number = 0.5,
    scale: number = 1
  ): number {
    let value = 0
    let amplitude = 1
    let frequency = scale
    let maxValue = 0

    for (let i = 0; i < octaves; i++) {
      value += this.noise2D(x * frequency, y * frequency) * amplitude
      maxValue += amplitude
      amplitude *= persistence
      frequency *= 2
    }

    return value / maxValue
  }

  /**
   * Generate a seamless noise pattern for tiling
   * @param x X coordinate
   * @param y Y coordinate
   * @param width Tile width
   * @param height Tile height
   * @param octaves Number of octaves
   * @param persistence Amplitude multiplier
   * @param scale Scale factor
   * @returns Noise value between -1 and 1
   */
  seamlessNoise2D(
    x: number,
    y: number,
    width: number,
    height: number,
    octaves: number = 4,
    persistence: number = 0.5,
    scale: number = 1
  ): number {
    const s = x / width
    const t = y / height

    const nx = Math.cos(s * 2 * Math.PI) * width / (2 * Math.PI)
    const ny = Math.cos(t * 2 * Math.PI) * height / (2 * Math.PI)
    const nz = Math.sin(s * 2 * Math.PI) * width / (2 * Math.PI)
    const nw = Math.sin(t * 2 * Math.PI) * height / (2 * Math.PI)

    const a = this.fractalNoise2D(nx, ny, octaves, persistence, scale)
    const b = this.fractalNoise2D(nz, nw, octaves, persistence, scale)
    const c = this.fractalNoise2D(nx, nw, octaves, persistence, scale)
    const d = this.fractalNoise2D(nz, ny, octaves, persistence, scale)

    const i1 = this.lerp(s, a, b)
    const i2 = this.lerp(s, c, d)

    return this.lerp(t, i1, i2)
  }
}

/**
 * Create a noise-based mask for fog of war effects
 * @param width Canvas width
 * @param height Canvas height
 * @param scale Noise scale
 * @param octaves Number of noise octaves
 * @param persistence Noise persistence
 * @param seed Random seed
 * @returns ImageData for the mask
 */
export function createFogMask(
  width: number,
  height: number,
  scale: number = 0.01,
  octaves: number = 4,
  persistence: number = 0.5,
  seed?: number
): ImageData {
  const noise = new PerlinNoise(seed)
  const imageData = new ImageData(width, height)
  const data = imageData.data

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = (y * width + x) * 4

      // Generate seamless noise for infinite tiling
      const noiseValue = noise.seamlessNoise2D(x, y, width, height, octaves, persistence, scale)

      // Convert noise from [-1, 1] to [0, 1] and apply curve for better distribution
      let alpha = (noiseValue + 1) * 0.5
      alpha = Math.pow(alpha, 1.5) // Apply curve for more interesting distribution

      // Create gradient from edges to center for natural fog falloff
      const centerX = width * 0.5
      const centerY = height * 0.5
      const maxDistance = Math.sqrt(centerX * centerX + centerY * centerY)
      const distance = Math.sqrt((x - centerX) ** 2 + (y - centerY) ** 2)
      const edgeFactor = 1 - Math.min(distance / maxDistance, 1)

      // Combine noise with edge gradient
      alpha = alpha * 0.7 + edgeFactor * 0.3

      // Set RGBA values (white fog with varying alpha)
      data[index] = 255     // Red
      data[index + 1] = 255 // Green
      data[index + 2] = 255 // Blue
      data[index + 3] = Math.floor(alpha * 255 * 0.6) // Alpha (60% max opacity)
    }
  }

  return imageData
}

/**
 * Create edge masking for infinite map appearance
 * @param width Canvas width
 * @param height Canvas height
 * @param edgeSize Size of edge fade in pixels
 * @returns ImageData for edge mask
 */
export function createEdgeMask(
  width: number,
  height: number,
  edgeSize: number = 100
): ImageData {
  const imageData = new ImageData(width, height)
  const data = imageData.data

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = (y * width + x) * 4

      // Calculate distance from edges
      const distFromLeft = x
      const distFromRight = width - x
      const distFromTop = y
      const distFromBottom = height - y

      const minDistFromEdge = Math.min(distFromLeft, distFromRight, distFromTop, distFromBottom)

      // Create smooth fade at edges
      let alpha = 1
      if (minDistFromEdge < edgeSize) {
        alpha = minDistFromEdge / edgeSize
        alpha = Math.pow(alpha, 0.5) // Smooth curve
      }

      // Set RGBA values (black mask with varying alpha)
      data[index] = 0       // Red
      data[index + 1] = 0   // Green
      data[index + 2] = 0   // Blue
      data[index + 3] = Math.floor((1 - alpha) * 255) // Alpha
    }
  }

  return imageData
}

/**
 * Create edge masking with Perlin noise for organic map edge transparency
 * @param width Canvas width
 * @param height Canvas height
 * @param edgeSize Size of edge fade in pixels
 * @param scale Noise scale for organic variation
 * @param octaves Number of noise octaves
 * @param persistence Noise persistence
 * @param seed Random seed
 * @param centerX Optional center X position (defaults to canvas center)
 * @param centerY Optional center Y position (defaults to canvas center)
 * @returns ImageData for edge mask with Perlin noise
 */
export function createEdgePerlinMask(
  width: number,
  height: number,
  edgeSize: number = 100,
  scale: number = 0.005,
  octaves: number = 3,
  persistence: number = 0.4,
  seed?: number,
  centerX?: number,
  centerY?: number
): ImageData {
  const noise = new PerlinNoise(seed)
  const imageData = new ImageData(width, height)
  const data = imageData.data

  // Use provided center or default to canvas center
  const maskCenterX = centerX !== undefined ? centerX : width * 0.5
  const maskCenterY = centerY !== undefined ? centerY : height * 0.5
  const maxRadius = Math.min(width, height) * 0.4 // Use 40% of smaller dimension for circular falloff

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = (y * width + x) * 4

      // Calculate radial distance from center for circular falloff
      const distFromCenter = Math.sqrt((x - maskCenterX) ** 2 + (y - maskCenterY) ** 2)
      const normalizedDistance = Math.min(distFromCenter / maxRadius, 1)

      // Create smooth radial fade from center to edges with more gradual transition
      let edgeFactor = 1
      const fadeStart = 0.3 // Start fading at 30% of radius for more gradual effect
      if (normalizedDistance > fadeStart) {
        const fadeProgress = (normalizedDistance - fadeStart) / (1 - fadeStart)
        edgeFactor = 1 - Math.pow(fadeProgress, 0.5) // Smoother curve for more gradual transition
      }

      // Generate multiple layers of Perlin noise for complex organic variation
      const noiseValue1 = noise.fractalNoise2D(x, y, octaves, persistence, scale)
      const noiseValue2 = noise.fractalNoise2D(x * 0.5, y * 0.5, octaves - 1, persistence * 0.8, scale * 2)

      // Combine noise layers for more organic patterns
      const combinedNoise = (noiseValue1 * 0.7 + noiseValue2 * 0.3)

      // Convert noise from [-1, 1] to [0, 1] with enhanced variation
      let noiseAlpha = (combinedNoise + 1) * 0.5
      noiseAlpha = Math.pow(noiseAlpha, 0.9) // Softer distribution curve

      // Create organic edge transparency with high noise influence
      let alpha = 0
      if (normalizedDistance > fadeStart) {
        const baseTransparency = 1 - edgeFactor
        const noiseVariation = noiseAlpha * 0.8 // 80% noise influence for organic edges

        // Add some randomness to the fade start position based on noise
        const noisyFadeStart = fadeStart + (noiseAlpha - 0.5) * 0.2
        const adjustedFadeProgress = Math.max(0, (normalizedDistance - noisyFadeStart) / (1 - noisyFadeStart))

        alpha = Math.min(1, adjustedFadeProgress * 0.6 + noiseVariation * 0.4)
      }

      // Set RGBA values (white mask with varying alpha for destination-out)
      data[index] = 255     // Red
      data[index + 1] = 255 // Green
      data[index + 2] = 255 // Blue
      data[index + 3] = Math.floor(alpha * 255) // Alpha
    }
  }

  return imageData
}

/**
 * Create small circular highlight mask with Perlin noise for marker highlighting
 * @param width Canvas width
 * @param height Canvas height
 * @param centerX Center X position of the highlight
 * @param centerY Center Y position of the highlight
 * @param radius Radius of the highlight area
 * @param scale Noise scale for organic variation
 * @param octaves Number of noise octaves
 * @param persistence Noise persistence
 * @param seed Random seed
 * @returns ImageData for marker highlight mask
 */
export function createMarkerHighlightMask(
  width: number,
  height: number,
  centerX: number,
  centerY: number,
  radius: number = 30,
  scale: number = 0.02,
  octaves: number = 2,
  persistence: number = 0.5,
  seed?: number
): ImageData {
  const noise = new PerlinNoise(seed)
  const imageData = new ImageData(width, height)
  const data = imageData.data

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = (y * width + x) * 4

      // Calculate distance from highlight center
      const distFromCenter = Math.sqrt((x - centerX) ** 2 + (y - centerY) ** 2)
      const normalizedDistance = Math.min(distFromCenter / radius, 1)

      // Create circular highlight with soft edges
      let alpha = 0
      if (distFromCenter <= radius) {
        // Generate Perlin noise for organic edge variation
        const noiseValue = noise.fractalNoise2D(x, y, octaves, persistence, scale)
        const noiseAlpha = (noiseValue + 1) * 0.5 // Convert from [-1, 1] to [0, 1]

        // Create smooth circular fade with noise variation
        const baseFade = 1 - Math.pow(normalizedDistance, 0.8) // Smooth circular fade
        const noiseVariation = noiseAlpha * 0.3 // 30% noise influence for subtle organic edges

        // Combine base fade with noise for organic highlight
        alpha = Math.max(0, Math.min(1, baseFade * 0.7 + noiseVariation))

        // Apply additional softening at edges
        if (normalizedDistance > 0.7) {
          const edgeFade = (1 - normalizedDistance) / 0.3 // Fade in outer 30%
          alpha *= edgeFade
        }
      }

      // Set RGBA values (white highlight with varying alpha for destination-out)
      data[index] = 255     // Red
      data[index + 1] = 255 // Green
      data[index + 2] = 255 // Blue
      data[index + 3] = Math.floor((1 - alpha) * 255) // Inverted alpha for destination-out
    }
  }

  return imageData
}