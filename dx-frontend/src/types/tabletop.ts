/**
 * Tabletop Map Editor Type Definitions
 * Based on docs/tabletop.md specification
 */

// Grid Configuration
export interface GridConfig {
  cellWidth: number;          // pixels
  cellHeight: number;         // pixels
  columns: number;            // horizontal cells
  rows: number;              // vertical cells
  xMorph: number;            // -1.0 to 1.0 for perspective
  yMorph: number;            // -1.0 to 1.0 for perspective
}

// Spawner Types
export type SpawnerType = 'player' | 'npc' | 'object' | 'effect';

export interface SpawnerProperties {
  name?: string;
  description?: string;
  count?: number;            // For NPC spawners - how many to spawn
  respawn?: boolean;         // Can respawn after defeat
  [key: string]: any;        // Additional custom properties
}

export interface Spawner {
  type: SpawnerType;
  properties: SpawnerProperties;
}

// Game Object Types
export type GameObjectType = 'character' | 'item' | 'chest';

export interface GameObjectProperties {
  name?: string;
  description?: string;
  [key: string]: any;        // Additional custom properties
}

export interface GameObject {
  type: GameObjectType;
  properties: GameObjectProperties;
}

// Cell Connections (movement)
export interface CellConnections {
  north: boolean;            // Can move north?
  south: boolean;
  east: boolean;
  west: boolean;
}

// Cell Data
export interface Cell {
  x: number;
  y: number;
  layer: number;
  available: boolean;        // Can spawn/move here?
  spawner: Spawner | null;
  gameObject: GameObject | null;
  connections: CellConnections;
}

// Layer Metadata (10 dimensions)
export interface LayerMetadata {
  id: number;                // 0-9
  name: string;              // e.g., "1st Dimension", "2nd Dimension"
  description: string;
  visualStyle: string;       // e.g., "Full color", "Grayscale with Flow highlights"
  energyCost: number;        // Energy cost to exist in this dimension
  active: boolean;           // Is this layer accessible in gameplay?
}

// Map Metadata
export interface MapMetadata {
  name: string;
  author: string;
  created: string;           // ISO date string
  modified: string;          // ISO date string
  version: string;
  description?: string;
  tags?: string[];
}

// Complete Map Data
export interface MapData {
  version: string;
  metadata: MapMetadata;
  grid: GridConfig;
  layers: LayerMetadata[];
  cells: Cell[];             // Flat array of all cells across all layers
  backgroundImage?: string;  // Base64 or URL
}

// Editor Tool Types
export type EditorTool =
  | 'select'                 // Select and inspect cells
  | 'availability'           // Toggle cell availability
  | 'wall'                   // Draw/remove walls (connections)
  | 'spawner-player'         // Place player spawners
  | 'spawner-npc'            // Place NPC spawners
  | 'spawner-object'         // Place object spawners
  | 'spawner-effect'         // Place effect spawners
  | 'game-object'            // Place game objects
  | 'erase';                 // Erase spawners/objects

// Editor State
export interface EditorState {
  currentLayer: number;      // 0-9
  selectedTool: EditorTool;
  selectedCell: { x: number; y: number; layer: number } | null;
  gridVisible: boolean;
  backgroundVisible: boolean;
  isDirty: boolean;          // Has unsaved changes
}

// Default layer configurations based on Dimension-X lore
export const DEFAULT_LAYERS: LayerMetadata[] = [
  {
    id: 0,
    name: '1st Dimension',
    description: 'Real world, normal life, full energy',
    visualStyle: 'Full color, normal',
    energyCost: 0,
    active: true
  },
  {
    id: 1,
    name: '2nd Dimension',
    description: 'Dark mirror world',
    visualStyle: 'Grayscale with Flow highlights',
    energyCost: 1,
    active: true
  },
  {
    id: 2,
    name: '3rd Dimension',
    description: 'Faded shadow realm',
    visualStyle: 'Heavy fog, gray',
    energyCost: 2,
    active: true
  },
  {
    id: 3,
    name: '4th Dimension',
    description: 'Dead zone with storms',
    visualStyle: 'Storm effects, blue-eyed shadows',
    energyCost: 3,
    active: true
  },
  {
    id: 4,
    name: '5th Dimension',
    description: 'Unknown/inaccessible',
    visualStyle: 'Not yet explored',
    energyCost: 5,
    active: false
  },
  {
    id: 5,
    name: '6th Dimension',
    description: 'Unknown/inaccessible',
    visualStyle: 'Not yet explored',
    energyCost: 5,
    active: false
  },
  {
    id: 6,
    name: '7th Dimension',
    description: 'Unknown/inaccessible',
    visualStyle: 'Not yet explored',
    energyCost: 5,
    active: false
  },
  {
    id: 7,
    name: '8th Dimension',
    description: 'Unknown/inaccessible',
    visualStyle: 'Not yet explored',
    energyCost: 5,
    active: false
  },
  {
    id: 8,
    name: '9th Dimension',
    description: 'Unknown/inaccessible',
    visualStyle: 'Not yet explored',
    energyCost: 5,
    active: false
  },
  {
    id: 9,
    name: '10th Dimension',
    description: 'Unknown/inaccessible',
    visualStyle: 'Not yet explored',
    energyCost: 5,
    active: false
  }
];

// Helper function to create empty cell
export function createEmptyCell(x: number, y: number, layer: number): Cell {
  return {
    x,
    y,
    layer,
    available: true,
    spawner: null,
    gameObject: null,
    connections: {
      north: true,
      south: true,
      east: true,
      west: true
    }
  };
}

// Helper function to create default grid config
export function createDefaultGridConfig(): GridConfig {
  return {
    cellWidth: 64,
    cellHeight: 64,
    columns: 30,
    rows: 30,
    xMorph: 0,
    yMorph: 0
  };
}

// Helper function to create new map
export function createNewMap(name: string, author: string): MapData {
  const now = new Date().toISOString();
  return {
    version: '1.0',
    metadata: {
      name,
      author,
      created: now,
      modified: now,
      version: '1.0',
      description: '',
      tags: []
    },
    grid: createDefaultGridConfig(),
    layers: [...DEFAULT_LAYERS],
    cells: [],
    backgroundImage: undefined
  };
}
