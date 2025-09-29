/**
 * File-based metadata resolver implementation using localStorage
 * This implementation stores metadata in browser localStorage for persistence
 * Can be easily extended to use actual file system or API in the future
 */

import { MetadataResolver, PlaceMetadata, validateMetadata } from './MetadataResolver'

export class FileMetadataResolver implements MetadataResolver {
  private readonly storageKey = 'dx-place-metadata'
  private readonly version = '1.0.0'
  private readonly mapDataPath = '/worldmap/map-data-2025-09-29-fixed.json'
  private readonly markersPath = '/worldmap/markers/'

  /**
   * Get the storage key for a specific place
   * @param placeId - Unique identifier for the place
   * @returns Storage key string
   */
  private getPlaceKey(placeId: string): string {
    return `${this.storageKey}:${placeId}`
  }

  /**
   * Get the index storage key for listing all places
   * @returns Index storage key string
   */
  private getIndexKey(): string {
    return `${this.storageKey}:index`
  }

  /**
   * Load the metadata index (list of all place IDs)
   * @returns Array of place IDs
   */
  private loadIndex(): string[] {
    try {
      const indexData = localStorage.getItem(this.getIndexKey())
      if (!indexData) return []

      const parsed = JSON.parse(indexData)
      return Array.isArray(parsed) ? parsed : []
    } catch (error) {
      console.warn('Failed to load metadata index:', error)
      return []
    }
  }

  /**
   * Save the metadata index (list of all place IDs)
   * @param placeIds - Array of place IDs to save
   */
  private saveIndex(placeIds: string[]): void {
    try {
      localStorage.setItem(this.getIndexKey(), JSON.stringify(placeIds))
    } catch (error) {
      console.error('Failed to save metadata index:', error)
    }
  }

  /**
   * Add a place ID to the index if it doesn't exist
   * @param placeId - Place ID to add
   */
  private addToIndex(placeId: string): void {
    const index = this.loadIndex()
    if (!index.includes(placeId)) {
      index.push(placeId)
      this.saveIndex(index)
    }
  }

  /**
   * Remove a place ID from the index
   * @param placeId - Place ID to remove
   */
  private removeFromIndex(placeId: string): void {
    const index = this.loadIndex()
    const filteredIndex = index.filter(id => id !== placeId)
    this.saveIndex(filteredIndex)
  }

  /**
   * Load metadata from individual marker JSON file
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to place metadata or null if not found
   */
  private async loadFromMarkerFile(placeId: string): Promise<PlaceMetadata | null> {
    try {
      console.log(`🌐 Making HTTP request to load marker file: ${this.markersPath}${placeId}.json`)
      const response = await fetch(`${this.markersPath}${placeId}.json`)
      if (!response.ok) {
        console.log(`❌ Marker file not found: ${this.markersPath}${placeId}.json (${response.status})`)
        return null
      }

      console.log(`✅ Successfully loaded marker file: ${this.markersPath}${placeId}.json`)
      const data = await response.json()

      // Validate the loaded data
      if (!validateMetadata(data)) {
        console.warn(`Invalid metadata structure in marker file for ${placeId}`)
        return null
      }

      // Resolve image path if present
      if (data.image) {
        data.image = this.resolveImagePath(data.image)
      }

      return data
    } catch (error) {
      // File not found or other error - this is expected for many cases
      console.log(`❌ Error loading marker file for ${placeId}:`, error)
      return null
    }
  }

  /**
   * Load metadata from main map data file
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to place metadata or null if not found
   */
  private async loadFromMapData(placeId: string): Promise<PlaceMetadata | null> {
    try {
      console.log(`🌐 Making HTTP request to load map data: ${this.mapDataPath}`)
      const response = await fetch(this.mapDataPath)
      if (!response.ok) {
        console.log(`❌ Map data file not found: ${this.mapDataPath} (${response.status})`)
        return null
      }

      console.log(`✅ Successfully loaded map data: ${this.mapDataPath}`)
      const mapData = await response.json()

      // Find marker by ID
      const marker = mapData.markers?.find((m: any) => m.id === placeId)
      if (!marker) {
        console.log(`❌ Marker with ID '${placeId}' not found in map data`)
        return null
      }

      console.log(`✅ Found marker '${placeId}' in map data: ${marker.name}`)
      // Convert marker to PlaceMetadata format
      return this.convertMarkerToMetadata(marker)
    } catch (error) {
      console.warn(`❌ Failed to load from map data for ${placeId}:`, error)
      return null
    }
  }

  /**
   * Load metadata from main map data file by name
   * @param placeName - Unique name for the place
   * @returns Promise resolving to place metadata or null if not found
   */
  private async loadFromMapDataByName(placeName: string): Promise<PlaceMetadata | null> {
    try {
      const response = await fetch(this.mapDataPath)
      if (!response.ok) return null

      const mapData = await response.json()

      // Find marker by name (case-insensitive)
      const marker = mapData.markers?.find((m: any) =>
        m.name?.toLowerCase() === placeName.toLowerCase()
      )
      if (!marker) return null

      // Convert marker to PlaceMetadata format
      return this.convertMarkerToMetadata(marker)
    } catch (error) {
      console.warn(`Failed to load from map data by name for ${placeName}:`, error)
      return null
    }
  }

  /**
   * Resolve image path to proper URL
   * @param imagePath - Image path from marker data (could be relative or full URL)
   * @returns Resolved image URL
   */
  private resolveImagePath(imagePath: string): string {
    if (!imagePath) return ''

    // If it's already a full URL (starts with http:// or https://), return as is
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
      return imagePath
    }

    // If it's a data URL, return as is
    if (imagePath.startsWith('data:')) {
      return imagePath
    }

    // If it starts with a slash, it's already an absolute path from root
    if (imagePath.startsWith('/')) {
      return imagePath
    }

    // For relative paths like "worldmap/images/city_of_memories.png"
    // Convert to absolute path from public directory
    return `/${imagePath}`
  }

  /**
   * Convert map marker data to PlaceMetadata format
   * @param marker - Marker data from map file
   * @returns PlaceMetadata object
   */
  private convertMarkerToMetadata(marker: any): PlaceMetadata {
    const now = new Date().toISOString()
    return {
      id: marker.id || `marker_${marker.name?.toLowerCase().replace(/\s+/g, '_')}`,
      name: marker.name || 'Unknown Place',
      description: marker.description || '',
      tags: marker.type ? [marker.type] : [],
      created: now,
      modified: now,
      image: this.resolveImagePath(marker.image || '')
    }
  }

  /**
   * Load metadata for a specific place
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to place metadata or null if not found
   */
  async loadMetadata(placeId: string): Promise<PlaceMetadata | null> {
    try {
      console.log(`🔍 Loading metadata for place: ${placeId}`)

      // First, try to load from localStorage (existing functionality)
      console.log(`📦 Checking localStorage for: ${placeId}`)
      const data = localStorage.getItem(this.getPlaceKey(placeId))
      if (data) {
        console.log(`✅ Found data in localStorage for: ${placeId}`)
        const parsed = JSON.parse(data)

        // Validate the loaded data
        if (validateMetadata(parsed)) {
          console.log(`✅ Valid metadata loaded from localStorage for: ${placeId}`)
          return parsed
        } else {
          console.warn(`❌ Invalid metadata structure for place ${placeId} in localStorage`)
        }
      } else {
        console.log(`❌ No data found in localStorage for: ${placeId}`)
      }

      // If not found in localStorage, try to load from individual marker file
      console.log(`🔍 Trying to load from marker file for: ${placeId}`)
      const markerFileData = await this.loadFromMarkerFile(placeId)
      if (markerFileData) {
        console.log(`✅ Successfully loaded from marker file for: ${placeId}`)
        return markerFileData
      }

      // If not found in marker file, try to load from main map data
      console.log(`🔍 Trying to load from map data for: ${placeId}`)
      const mapData = await this.loadFromMapData(placeId)
      if (mapData) {
        console.log(`✅ Successfully loaded from map data for: ${placeId}`)
        return mapData
      }

      // Not found anywhere
      console.log(`❌ Metadata not found anywhere for: ${placeId}`)
      return null
    } catch (error) {
      console.error(`❌ Failed to load metadata for place ${placeId}:`, error)
      return null
    }
  }

  /**
   * Load metadata for a specific place by name
   * @param placeName - Unique name for the place
   * @returns Promise resolving to place metadata or null if not found
   */
  async loadMetadataByName(placeName: string): Promise<PlaceMetadata | null> {
    try {
      // Try to load from main map data by name
      const mapData = await this.loadFromMapDataByName(placeName)
      if (mapData) {
        return mapData
      }

      // Not found
      return null
    } catch (error) {
      console.error(`Failed to load metadata for place by name ${placeName}:`, error)
      return null
    }
  }

  /**
   * Save metadata for a specific place
   * @param metadata - Place metadata to save
   * @returns Promise resolving to success status
   */
  async saveMetadata(metadata: PlaceMetadata): Promise<boolean> {
    try {
      // Validate metadata before saving
      if (!validateMetadata(metadata)) {
        console.error('Invalid metadata structure, cannot save')
        return false
      }

      // Update the modified timestamp
      const updatedMetadata = {
        ...metadata,
        modified: new Date().toISOString()
      }

      // Save the metadata
      localStorage.setItem(
        this.getPlaceKey(metadata.id),
        JSON.stringify(updatedMetadata)
      )

      // Add to index
      this.addToIndex(metadata.id)

      return true
    } catch (error) {
      console.error(`Failed to save metadata for place ${metadata.id}:`, error)
      return false
    }
  }

  /**
   * Delete metadata for a specific place
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to success status
   */
  async deleteMetadata(placeId: string): Promise<boolean> {
    try {
      localStorage.removeItem(this.getPlaceKey(placeId))
      this.removeFromIndex(placeId)
      return true
    } catch (error) {
      console.error(`Failed to delete metadata for place ${placeId}:`, error)
      return false
    }
  }

  /**
   * List all available place metadata
   * @returns Promise resolving to array of place metadata
   */
  async listMetadata(): Promise<PlaceMetadata[]> {
    try {
      const index = this.loadIndex()
      const metadataList: PlaceMetadata[] = []

      for (const placeId of index) {
        const metadata = await this.loadMetadata(placeId)
        if (metadata) {
          metadataList.push(metadata)
        }
      }

      return metadataList
    } catch (error) {
      console.error('Failed to list metadata:', error)
      return []
    }
  }

  /**
   * Check if metadata exists for a specific place
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to existence status
   */
  async hasMetadata(placeId: string): Promise<boolean> {
    try {
      const data = localStorage.getItem(this.getPlaceKey(placeId))
      return data !== null
    } catch (error) {
      console.error(`Failed to check metadata existence for place ${placeId}:`, error)
      return false
    }
  }

  /**
   * Clear all metadata (useful for testing or reset)
   * @returns Promise resolving to success status
   */
  async clearAllMetadata(): Promise<boolean> {
    try {
      const index = this.loadIndex()

      // Remove all place metadata
      for (const placeId of index) {
        localStorage.removeItem(this.getPlaceKey(placeId))
      }

      // Clear the index
      localStorage.removeItem(this.getIndexKey())

      return true
    } catch (error) {
      console.error('Failed to clear all metadata:', error)
      return false
    }
  }

  /**
   * Get storage statistics
   * @returns Object with storage information
   */
  getStorageInfo(): { totalPlaces: number; storageUsed: number } {
    try {
      const index = this.loadIndex()
      let storageUsed = 0

      // Calculate approximate storage usage
      for (const placeId of index) {
        const data = localStorage.getItem(this.getPlaceKey(placeId))
        if (data) {
          storageUsed += data.length
        }
      }

      return {
        totalPlaces: index.length,
        storageUsed: storageUsed
      }
    } catch (error) {
      console.error('Failed to get storage info:', error)
      return { totalPlaces: 0, storageUsed: 0 }
    }
  }
}