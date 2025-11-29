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

// Terrain Types (Heroes of Might and Magic style)
export type TerrainType =
  | 'grass'        // Normal terrain, standard movement cost
  | 'road'         // Fast movement, reduced cost
  | 'dirt'         // Normal terrain
  | 'sand'         // Slightly slower
  | 'swamp'        // Slow movement, high cost
  | 'water'        // Impassable for most units
  | 'lava'         // Impassable, damages units
  | 'snow'         // Slow movement
  | 'rock'         // Impassable
  | 'forest'       // Slow movement, provides cover
  | 'mountain'     // Impassable or very high cost
  | 'void';        // Completely impassable

// Terrain properties with movement costs
export interface TerrainProperties {
  type: TerrainType;
  movementCost: number;      // Cost to enter this cell (1 = normal, 2 = slow, Infinity = impassable)
  description?: string;
  visualStyle?: string;      // CSS class or color for rendering
}

// Default terrain configurations
export const TERRAIN_CONFIGS: Record<TerrainType, TerrainProperties> = {
  grass: { type: 'grass', movementCost: 1, description: 'Normal grassland', visualStyle: '#90EE90' },
  road: { type: 'road', movementCost: 0.75, description: 'Paved road', visualStyle: '#8B7355' },
  dirt: { type: 'dirt', movementCost: 1, description: 'Dirt path', visualStyle: '#D2691E' },
  sand: { type: 'sand', movementCost: 1.25, description: 'Sandy terrain', visualStyle: '#F4A460' },
  swamp: { type: 'swamp', movementCost: 2, description: 'Swampy ground', visualStyle: '#556B2F' },
  water: { type: 'water', movementCost: Infinity, description: 'Deep water', visualStyle: '#4682B4' },
  lava: { type: 'lava', movementCost: Infinity, description: 'Molten lava', visualStyle: '#FF4500' },
  snow: { type: 'snow', movementCost: 1.5, description: 'Snow covered', visualStyle: '#FFFAFA' },
  rock: { type: 'rock', movementCost: Infinity, description: 'Solid rock', visualStyle: '#696969' },
  forest: { type: 'forest', movementCost: 1.5, description: 'Dense forest', visualStyle: '#228B22' },
  mountain: { type: 'mountain', movementCost: Infinity, description: 'Mountain peak', visualStyle: '#A9A9A9' },
  void: { type: 'void', movementCost: Infinity, description: 'Empty void', visualStyle: '#000000' }
};

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

// Movement directions (including diagonals for edge map)
export type MovementDirection =
  | 'north'
  | 'south'
  | 'east'
  | 'west'
  | 'northEast'
  | 'northWest'
  | 'southEast'
  | 'southWest';

// Edge identifier - uniquely identifies an edge between two cells
export interface EdgeId {
  fromX: number;
  fromY: number;
  toX: number;
  toY: number;
  layer: number;
}

// Edge properties - represents a connection between two cells
export interface Edge {
  id: EdgeId;
  direction: MovementDirection;
  blocked: boolean;          // Is this edge blocked (wall, cliff, etc.)?
  cost?: number;            // Optional additional cost for this edge (e.g., door, difficult passage)
  description?: string;     // Optional description (e.g., "Locked door", "Narrow passage")
}

// Cell Data - represents a single cell in the grid
export interface Cell {
  x: number;
  y: number;
  layer: number;

  // Terrain and movement
  terrain: TerrainType;      // Type of terrain in this cell
  passable: boolean;         // Can units enter this cell? (false = impassable obstacle)

  // Occupancy
  occupied: boolean;         // Is a unit currently on this cell?
  occupantId?: string;       // ID of the unit occupying this cell

  // Content
  spawner: Spawner | null;
  gameObject: GameObject | null;

  // Visual and metadata
  visualOverride?: string;   // Optional custom visual style
  notes?: string;           // Designer notes for this cell
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
  edges: Edge[];             // All edges (connections) between cells - required for proper pathfinding
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

// Helper function to create empty cell with default terrain
export function createEmptyCell(x: number, y: number, layer: number, terrain: TerrainType = 'grass'): Cell {
  return {
    x,
    y,
    layer,
    terrain,
    passable: true,
    occupied: false,
    spawner: null,
    gameObject: null
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
    version: '2.0',  // Bumped version for new data structure
    metadata: {
      name,
      author,
      created: now,
      modified: now,
      version: '2.0',
      description: '',
      tags: []
    },
    grid: createDefaultGridConfig(),
    layers: [...DEFAULT_LAYERS],
    cells: [],
    edges: [],
    backgroundImage: undefined
  };
}

// Direction deltas for calculating neighbor positions
export const DIRECTION_DELTAS: Record<MovementDirection, { dx: number; dy: number }> = {
  north: { dx: 0, dy: -1 },
  south: { dx: 0, dy: 1 },
  east: { dx: 1, dy: 0 },
  west: { dx: -1, dy: 0 },
  northEast: { dx: 1, dy: -1 },
  northWest: { dx: -1, dy: -1 },
  southEast: { dx: 1, dy: 1 },
  southWest: { dx: -1, dy: 1 }
};

// Opposite directions for bidirectional edge validation
export const OPPOSITE_DIRECTION: Record<MovementDirection, MovementDirection> = {
  north: 'south',
  south: 'north',
  east: 'west',
  west: 'east',
  northEast: 'southWest',
  southWest: 'northEast',
  northWest: 'southEast',
  southEast: 'northWest'
};

// Helper function to create an edge key for lookups
export function getEdgeKey(fromX: number, fromY: number, toX: number, toY: number, layer: number): string {
  return `${fromX},${fromY}->${toX},${toY}@${layer}`;
}

// Helper function to create an edge
export function createEdge(
  fromX: number,
  fromY: number,
  toX: number,
  toY: number,
  layer: number,
  direction: MovementDirection,
  blocked: boolean = false
): Edge {
  return {
    id: { fromX, fromY, toX, toY, layer },
    direction,
    blocked
  };
}

// Helper function to build all possible edges for a grid
// This creates edges between all adjacent cells (cardinal and diagonal)
export function buildAllEdgesForGrid(columns: number, rows: number, layers: number[]): Edge[] {
  const edges: Edge[] = [];

  layers.forEach(layer => {
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < columns; x++) {
        // Create edges for all 8 directions
        Object.entries(DIRECTION_DELTAS).forEach(([direction, delta]) => {
          const toX = x + delta.dx;
          const toY = y + delta.dy;

          // Check if target is within bounds
          if (toX >= 0 && toY >= 0 && toX < columns && toY < rows) {
            edges.push(createEdge(x, y, toX, toY, layer, direction as MovementDirection, false));
          }
        });
      }
    }
  });

  return edges;
}

// Legacy types for migration from v1.0 to v2.0
interface LegacyCellConnections {
  north: boolean;
  south: boolean;
  east: boolean;
  west: boolean;
  northEast?: boolean;
  northWest?: boolean;
  southEast?: boolean;
  southWest?: boolean;
}

interface LegacyCell {
  x: number;
  y: number;
  layer: number;
  available: boolean;
  spawner: Spawner | null;
  gameObject: GameObject | null;
  connections: LegacyCellConnections;
}

interface LegacyMapData {
  version: string;
  metadata: MapMetadata;
  grid: GridConfig;
  layers: LayerMetadata[];
  cells: LegacyCell[];
  backgroundImage?: string;
}

// Migration utility: Convert v1.0 map to v2.0 format
export function migrateMapToV2(oldMap: any): MapData {
  console.log('[Migration] Converting map from v1.0 to v2.0 format');

  // Check if already v2.0
  if (oldMap.version === '2.0' && oldMap.edges && Array.isArray(oldMap.edges)) {
    console.log('[Migration] Map is already v2.0, no migration needed');
    return oldMap as MapData;
  }

  const legacyMap = oldMap as LegacyMapData;
  const { columns, rows } = legacyMap.grid;
  const activeLayers = legacyMap.layers.filter(l => l.active).map(l => l.id);

  // Convert cells from v1.0 to v2.0
  const newCells: Cell[] = legacyMap.cells.map(oldCell => {
    // Determine terrain based on availability
    // If cell was marked as unavailable, treat it as rock (impassable)
    const terrain: TerrainType = oldCell.available ? 'grass' : 'rock';
    const passable = oldCell.available;

    return {
      x: oldCell.x,
      y: oldCell.y,
      layer: oldCell.layer,
      terrain,
      passable,
      occupied: false,
      spawner: oldCell.spawner,
      gameObject: oldCell.gameObject
    };
  });

  // Build edges from old connections
  const edges: Edge[] = [];
  const cellLookup = new Map<string, LegacyCell>();

  legacyMap.cells.forEach(cell => {
    cellLookup.set(`${cell.x},${cell.y},${cell.layer}`, cell);
  });

  // For each cell, create edges based on its connections
  legacyMap.cells.forEach(cell => {
    if (!cell.available) return; // Skip unavailable cells

    const connections = cell.connections;

    // Process all 8 directions
    Object.entries(DIRECTION_DELTAS).forEach(([direction, delta]) => {
      const dir = direction as MovementDirection;
      const toX = cell.x + delta.dx;
      const toY = cell.y + delta.dy;

      // Check bounds
      if (toX < 0 || toY < 0 || toX >= columns || toY >= rows) return;

      // Check if neighbor exists and is available
      const neighborKey = `${toX},${toY},${cell.layer}`;
      const neighbor = cellLookup.get(neighborKey);
      const neighborAvailable = !neighbor || neighbor.available !== false;

      if (!neighborAvailable) return;

      // Determine if edge is blocked based on old connections
      let blocked = false;

      if (connections) {
        const connectionValue = connections[dir as keyof LegacyCellConnections];

        // For cardinal directions: false means blocked
        if (['north', 'south', 'east', 'west'].includes(dir)) {
          blocked = connectionValue === false;
        } else {
          // For diagonals: false means blocked, undefined means open
          blocked = connectionValue === false;
        }
      }

      edges.push(createEdge(cell.x, cell.y, toX, toY, cell.layer, dir, blocked));
    });
  });

  // For cells that don't exist in the old map, create default edges
  // This ensures all passable cells have edges
  activeLayers.forEach(layer => {
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < columns; x++) {
        const key = `${x},${y},${layer}`;
        if (!cellLookup.has(key)) {
          // This cell doesn't exist in old data, create default edges
          Object.entries(DIRECTION_DELTAS).forEach(([direction, delta]) => {
            const dir = direction as MovementDirection;
            const toX = x + delta.dx;
            const toY = y + delta.dy;

            if (toX >= 0 && toY >= 0 && toX < columns && toY < rows) {
              const neighborKey = `${toX},${toY},${layer}`;
              const neighbor = cellLookup.get(neighborKey);
              const neighborAvailable = !neighbor || neighbor.available !== false;

              if (neighborAvailable) {
                edges.push(createEdge(x, y, toX, toY, layer, dir, false));
              }
            }
          });
        }
      }
    }
  });

  console.log(`[Migration] Converted ${legacyMap.cells.length} cells and created ${edges.length} edges`);

  return {
    version: '2.0',
    metadata: {
      ...legacyMap.metadata,
      version: '2.0',
      modified: new Date().toISOString()
    },
    grid: legacyMap.grid,
    layers: legacyMap.layers,
    cells: newCells,
    edges,
    backgroundImage: legacyMap.backgroundImage
  };
}
