/**
 * Abstract metadata resolver interface for place metadata operations
 * This interface allows for different backend implementations (file, API, etc.)
 */

export interface PlaceMetadata {
  id: string
  name: string
  image?: string
  description: string
  tags: string[]
  created: string
  modified: string
}

export interface MetadataResolver {
  /**
   * Load metadata for a specific place
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to place metadata or null if not found
   */
  loadMetadata(placeId: string): Promise<PlaceMetadata | null>

  /**
   * Save metadata for a specific place
   * @param metadata - Place metadata to save
   * @returns Promise resolving to success status
   */
  saveMetadata(metadata: PlaceMetadata): Promise<boolean>

  /**
   * Delete metadata for a specific place
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to success status
   */
  deleteMetadata(placeId: string): Promise<boolean>

  /**
   * List all available place metadata
   * @returns Promise resolving to array of place metadata
   */
  listMetadata(): Promise<PlaceMetadata[]>

  /**
   * Check if metadata exists for a specific place
   * @param placeId - Unique identifier for the place
   * @returns Promise resolving to existence status
   */
  hasMetadata(placeId: string): Promise<boolean>
}

/**
 * Create a default place metadata object
 * @param placeId - Unique identifier for the place
 * @param name - Display name for the place
 * @returns Default place metadata
 */
export function createDefaultMetadata(placeId: string, name: string): PlaceMetadata {
  const now = new Date().toISOString()
  return {
    id: placeId,
    name: name,
    description: '',
    tags: [],
    created: now,
    modified: now
  }
}

/**
 * Validate place metadata structure
 * @param metadata - Metadata object to validate
 * @returns True if valid, false otherwise
 */
export function validateMetadata(metadata: any): metadata is PlaceMetadata {
  return (
    typeof metadata === 'object' &&
    metadata !== null &&
    typeof metadata.id === 'string' &&
    typeof metadata.name === 'string' &&
    typeof metadata.description === 'string' &&
    Array.isArray(metadata.tags) &&
    metadata.tags.every((tag: any) => typeof tag === 'string') &&
    typeof metadata.created === 'string' &&
    typeof metadata.modified === 'string' &&
    (metadata.image === undefined || typeof metadata.image === 'string')
  )
}