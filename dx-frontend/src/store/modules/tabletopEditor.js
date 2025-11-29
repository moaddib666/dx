import {
  createNewMap,
  createEmptyCell,
  createDefaultGridConfig,
  createEdge,
  getEdgeKey,
  migrateMapToV2,
  DIRECTION_DELTAS,
  DEFAULT_LAYERS
} from '@/types/tabletop';

const state = {
  mapData: null,
  editorState: {
    currentLayer: 0,
    selectedTool: 'select',
    selectedCell: null,
    gridVisible: true,
    backgroundVisible: true,
    // Editor mode controls which tool set and behaviors are active
    // 'availability' | 'object' | 'path' | 'config'
    editorMode: 'availability',
    // Legend / visibility toggles for overlays
    availabilityVisible: true,
    pathsVisible: true,
    objectsVisible: true,
    isDirty: false
  }
};

const getters = {
  currentMap: (state) => state.mapData,
  currentLayer: (state) => state.editorState.currentLayer,
  selectedTool: (state) => state.editorState.selectedTool,
  selectedCell: (state) => state.editorState.selectedCell,
  gridVisible: (state) => state.editorState.gridVisible,
  backgroundVisible: (state) => state.editorState.backgroundVisible,
  editorMode: (state) => state.editorState.editorMode,
  availabilityVisible: (state) => state.editorState.availabilityVisible,
  pathsVisible: (state) => state.editorState.pathsVisible,
  objectsVisible: (state) => state.editorState.objectsVisible,
  isDirty: (state) => state.editorState.isDirty,

  // Get cells for current layer
  currentLayerCells: (state) => {
    if (!state.mapData || !state.mapData.cells) return [];
    return state.mapData.cells.filter(cell => cell.layer === state.editorState.currentLayer);
  },

  // Get specific cell
  getCell: (state) => (x, y, layer) => {
    if (!state.mapData || !state.mapData.cells) return null;
    return state.mapData.cells.find(
      cell => cell.x === x && cell.y === y && cell.layer === layer
    );
  },

  // Get specific edge
  getEdge: (state) => (fromX, fromY, toX, toY, layer) => {
    if (!state.mapData || !state.mapData.edges) return null;
    return state.mapData.edges.find(
      edge => edge.id.fromX === fromX &&
              edge.id.fromY === fromY &&
              edge.id.toX === toX &&
              edge.id.toY === toY &&
              edge.id.layer === layer
    );
  },

  // Get all edges from a specific cell
  getEdgesFromCell: (state) => (x, y, layer) => {
    if (!state.mapData || !state.mapData.edges) return [];
    return state.mapData.edges.filter(
      edge => edge.id.fromX === x && edge.id.fromY === y && edge.id.layer === layer
    );
  },

  // Get all edges for current layer
  currentLayerEdges: (state) => {
    if (!state.mapData || !state.mapData.edges) return [];
    return state.mapData.edges.filter(edge => edge.id.layer === state.editorState.currentLayer);
  },

  // Get layer metadata
  getCurrentLayerMetadata: (state) => {
    if (!state.mapData) return null;
    return state.mapData.layers.find(layer => layer.id === state.editorState.currentLayer);
  },

  // Get grid config
  gridConfig: (state) => state.mapData?.grid || null
};

const mutations = {
  SET_MAP_DATA(state, mapData) {
    console.log('[Store] SET_MAP_DATA mutation called');
    console.log('[Store] Incoming mapData:', mapData ? {
      version: mapData.version,
      hasMetadata: !!mapData.metadata,
      metadataName: mapData.metadata?.name,
      metadataCreated: mapData.metadata?.created,
      hasGrid: !!mapData.grid,
      gridConfig: mapData.grid,
      hasLayers: !!mapData.layers,
      layersCount: mapData.layers?.length,
      hasCells: !!mapData.cells,
      cellsCount: mapData.cells?.length,
      hasEdges: !!mapData.edges,
      edgesCount: mapData.edges?.length,
      hasBackgroundImage: !!mapData.backgroundImage
    } : 'null');

    // Deep clone the mapData to ensure we have a fresh copy
    // This prevents mutations from affecting the original imported data
    if (mapData) {
      // Apply migration if needed (v1.0 -> v2.0)
      let migratedData = mapData;
      if (mapData.version !== '2.0' || !mapData.edges) {
        console.log('[Store] Applying migration to v2.0 format');
        migratedData = migrateMapToV2(mapData);
      }

      console.log('[Store] Deep cloning map data for reactivity');
      state.mapData = {
        version: migratedData.version,
        metadata: { ...migratedData.metadata },
        grid: { ...migratedData.grid },
        layers: migratedData.layers.map(layer => ({ ...layer })),
        cells: migratedData.cells ? migratedData.cells.map(cell => ({
          ...cell,
          spawner: cell.spawner ? { ...cell.spawner, properties: { ...cell.spawner.properties } } : null,
          gameObject: cell.gameObject ? { ...cell.gameObject, properties: { ...cell.gameObject.properties } } : null
        })) : [],
        edges: migratedData.edges ? migratedData.edges.map(edge => ({
          ...edge,
          id: { ...edge.id }
        })) : [],
        backgroundImage: migratedData.backgroundImage
      };
    } else {
      state.mapData = null;
    }

    state.editorState.isDirty = false;
    // Reset visibility settings to ensure grid and background are visible after import
    state.editorState.gridVisible = true;
    state.editorState.backgroundVisible = true;

    console.log('[Store] ✅ Map data set in state');
    console.log('[Store] Editor state:', {
      currentLayer: state.editorState.currentLayer,
      gridVisible: state.editorState.gridVisible,
      backgroundVisible: state.editorState.backgroundVisible,
      isDirty: state.editorState.isDirty
    });
  },

  SET_CURRENT_LAYER(state, layer) {
    state.editorState.currentLayer = layer;
    state.editorState.selectedCell = null; // Clear selection when changing layers
  },

  SET_SELECTED_TOOL(state, tool) {
    state.editorState.selectedTool = tool;
  },

  SET_EDITOR_MODE(state, mode) {
    state.editorState.editorMode = mode;
  },

  SET_SELECTED_CELL(state, cell) {
    state.editorState.selectedCell = cell;
  },

  SET_GRID_VISIBLE(state, visible) {
    state.editorState.gridVisible = visible;
  },

  SET_BACKGROUND_VISIBLE(state, visible) {
    state.editorState.backgroundVisible = visible;
  },

  SET_AVAILABILITY_VISIBLE(state, visible) {
    state.editorState.availabilityVisible = visible;
  },

  SET_PATHS_VISIBLE(state, visible) {
    state.editorState.pathsVisible = visible;
  },

  SET_OBJECTS_VISIBLE(state, visible) {
    state.editorState.objectsVisible = visible;
  },

  SET_DIRTY(state, dirty) {
    state.editorState.isDirty = dirty;
  },

  UPDATE_GRID_CONFIG(state, config) {
    if (state.mapData) {
      state.mapData.grid = { ...state.mapData.grid, ...config };
      state.editorState.isDirty = true;
    }
  },

  UPDATE_CELL(state, { x, y, layer, updates }) {
    if (!state.mapData) return;

    const cellIndex = state.mapData.cells.findIndex(
      cell => cell.x === x && cell.y === y && cell.layer === layer
    );

    if (cellIndex !== -1) {
      // Create a new cell with updates
      const updatedCell = {
        ...state.mapData.cells[cellIndex],
        ...updates
      };
      state.mapData.cells = [
        ...state.mapData.cells.slice(0, cellIndex),
        updatedCell,
        ...state.mapData.cells.slice(cellIndex + 1)
      ];
    } else {
      // Create new cell if it doesn't exist
      const newCell = createEmptyCell(x, y, layer);
      state.mapData.cells = [...state.mapData.cells, { ...newCell, ...updates }];
    }

    state.editorState.isDirty = true;
  },

  TOGGLE_CELL_AVAILABILITY(state, { x, y, layer }) {
    if (!state.mapData) return;

    const cellIndex = state.mapData.cells.findIndex(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (cellIndex !== -1) {
      // Toggle passable and terrain
      const currentCell = state.mapData.cells[cellIndex];
      const newPassable = !currentCell.passable;
      const newTerrain = newPassable ? 'grass' : 'rock';

      const updatedCell = {
        ...currentCell,
        passable: newPassable,
        terrain: newTerrain
      };

      state.mapData.cells = [
        ...state.mapData.cells.slice(0, cellIndex),
        updatedCell,
        ...state.mapData.cells.slice(cellIndex + 1)
      ];
    } else {
      // Create new cell with passable set to false (rock terrain)
      const newCell = createEmptyCell(x, y, layer, 'rock');
      newCell.passable = false;
      state.mapData.cells = [...state.mapData.cells, newCell];
    }

    state.editorState.isDirty = true;
  },

  TOGGLE_EDGE(state, { x, y, layer, direction }) {
    if (!state.mapData || !state.mapData.edges) return;

    const delta = DIRECTION_DELTAS[direction];
    if (!delta) return;

    const toX = x + delta.dx;
    const toY = y + delta.dy;

    // Check if neighbor is within grid bounds
    const gridConfig = state.mapData.grid;
    if (!gridConfig) return;

    const { columns, rows } = gridConfig;
    if (toX < 0 || toY < 0 || toX >= columns || toY >= rows) {
      // Neighbor is out of bounds, cannot toggle edge
      return;
    }

    // Check if both cells are passable
    const fromCell = state.mapData.cells.find(
      c => c.x === x && c.y === y && c.layer === layer
    );
    const fromPassable = !fromCell || fromCell.passable !== false;

    const toCell = state.mapData.cells.find(
      c => c.x === toX && c.y === toY && c.layer === layer
    );
    const toPassable = !toCell || toCell.passable !== false;

    if (!fromPassable || !toPassable) {
      // Cannot toggle edge if either cell is impassable
      return;
    }

    // Find the edge
    const edgeIndex = state.mapData.edges.findIndex(
      e => e.id.fromX === x &&
           e.id.fromY === y &&
           e.id.toX === toX &&
           e.id.toY === toY &&
           e.id.layer === layer
    );

    if (edgeIndex !== -1) {
      // Edge exists, toggle its blocked status
      const edge = state.mapData.edges[edgeIndex];
      const updatedEdge = {
        ...edge,
        id: { ...edge.id },
        blocked: !edge.blocked
      };

      state.mapData.edges = [
        ...state.mapData.edges.slice(0, edgeIndex),
        updatedEdge,
        ...state.mapData.edges.slice(edgeIndex + 1)
      ];
    } else {
      // Edge doesn't exist, create it as blocked
      const newEdge = createEdge(x, y, toX, toY, layer, direction, true);
      state.mapData.edges = [...state.mapData.edges, newEdge];
    }

    state.editorState.isDirty = true;
  },

  SET_CELL_SPAWNER(state, { x, y, layer, spawner }) {
    if (!state.mapData) return;

    const cellIndex = state.mapData.cells.findIndex(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (cellIndex !== -1) {
      // Create a new cell with updated spawner
      const updatedCell = {
        ...state.mapData.cells[cellIndex],
        spawner: spawner ? { ...spawner, properties: { ...spawner.properties } } : null
      };
      state.mapData.cells = [
        ...state.mapData.cells.slice(0, cellIndex),
        updatedCell,
        ...state.mapData.cells.slice(cellIndex + 1)
      ];
    } else {
      // Create new cell with spawner
      const newCell = createEmptyCell(x, y, layer);
      newCell.spawner = spawner ? { ...spawner, properties: { ...spawner.properties } } : null;
      state.mapData.cells = [...state.mapData.cells, newCell];
    }

    state.editorState.isDirty = true;
  },

  SET_CELL_GAME_OBJECT(state, { x, y, layer, gameObject }) {
    if (!state.mapData) return;

    const cellIndex = state.mapData.cells.findIndex(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (cellIndex !== -1) {
      // Create a new cell with updated gameObject
      const updatedCell = {
        ...state.mapData.cells[cellIndex],
        gameObject: gameObject ? { ...gameObject, properties: { ...gameObject.properties } } : null
      };
      state.mapData.cells = [
        ...state.mapData.cells.slice(0, cellIndex),
        updatedCell,
        ...state.mapData.cells.slice(cellIndex + 1)
      ];
    } else {
      // Create new cell with gameObject
      const newCell = createEmptyCell(x, y, layer);
      newCell.gameObject = gameObject ? { ...gameObject, properties: { ...gameObject.properties } } : null;
      state.mapData.cells = [...state.mapData.cells, newCell];
    }

    state.editorState.isDirty = true;
  },

  CLEAR_CELL_CONTENT(state, { x, y, layer }) {
    if (!state.mapData) return;

    const cellIndex = state.mapData.cells.findIndex(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (cellIndex !== -1) {
      // Create a new cell with cleared content
      const updatedCell = {
        ...state.mapData.cells[cellIndex],
        spawner: null,
        gameObject: null
      };
      state.mapData.cells = [
        ...state.mapData.cells.slice(0, cellIndex),
        updatedCell,
        ...state.mapData.cells.slice(cellIndex + 1)
      ];
      state.editorState.isDirty = true;
    }
  },

  SET_BACKGROUND_IMAGE(state, imageData) {
    if (state.mapData) {
      state.mapData.backgroundImage = imageData;
      state.editorState.isDirty = true;
    }
  },

  UPDATE_MAP_METADATA(state, metadata) {
    if (state.mapData) {
      state.mapData.metadata = { ...state.mapData.metadata, ...metadata };
      state.mapData.metadata.modified = new Date().toISOString();
      state.editorState.isDirty = true;
    }
  },

  AUTO_GENERATE_EDGES(state) {
    if (!state.mapData || !state.mapData.grid || !state.mapData.layers) return;

    console.log('[Auto-map] Starting automatic edge generation...');

    const { columns, rows } = state.mapData.grid;
    const activeLayers = state.mapData.layers.filter(l => l.active).map(l => l.id);

    // Build cell lookup for quick passability checks
    const cellLookup = new Map();
    if (state.mapData.cells) {
      state.mapData.cells.forEach(cell => {
        cellLookup.set(`${cell.x},${cell.y},${cell.layer}`, cell);
      });
    }

    // Helper to check if a cell is passable
    const isCellPassable = (x, y, layer) => {
      // Out of bounds = not passable
      if (x < 0 || y < 0 || x >= columns || y >= rows) return false;

      const key = `${x},${y},${layer}`;
      const cell = cellLookup.get(key);

      // If cell doesn't exist, it's passable by default (implicit grass)
      // If cell exists, check passable property (default to true if not explicitly false)
      return !cell || cell.passable !== false;
    };

    const newEdges = [];
    let edgeCount = 0;

    // Generate edges for each active layer
    activeLayers.forEach(layer => {
      for (let y = 0; y < rows; y++) {
        for (let x = 0; x < columns; x++) {
          // Skip if this cell is not passable
          if (!isCellPassable(x, y, layer)) continue;

          // Create edges for all 8 directions
          Object.entries(DIRECTION_DELTAS).forEach(([direction, delta]) => {
            const toX = x + delta.dx;
            const toY = y + delta.dy;

            // Check if target is within bounds and passable
            if (isCellPassable(toX, toY, layer)) {
              newEdges.push(createEdge(x, y, toX, toY, layer, direction, false));
              edgeCount++;
            }
          });
        }
      }
    });

    // Replace edges array with newly generated edges
    state.mapData.edges = newEdges;
    state.editorState.isDirty = true;

    console.log(`[Auto-map] ✅ Generated ${edgeCount} edges for ${activeLayers.length} active layer(s)`);
    console.log(`[Auto-map] Grid: ${columns}x${rows}, Total edges: ${newEdges.length}`);
  }
};

const actions = {
  createNewMap({ commit }, { name, author }) {
    const newMap = createNewMap(name, author);
    commit('SET_MAP_DATA', newMap);
  },

  loadMap({ commit }, mapData) {
    console.log('[Store Action] loadMap called with mapData:', mapData ? {
      name: mapData.metadata?.name,
      version: mapData.version,
      gridColumns: mapData.grid?.columns,
      gridRows: mapData.grid?.rows,
      layersCount: mapData.layers?.length,
      cellsCount: mapData.cells?.length
    } : 'null');
    commit('SET_MAP_DATA', mapData);
    console.log('[Store Action] ✅ loadMap completed, SET_MAP_DATA mutation committed');
  },

  setCurrentLayer({ commit }, layer) {
    if (layer >= 0 && layer <= 9) {
      commit('SET_CURRENT_LAYER', layer);
    }
  },

  setEditorMode({ commit }, mode) {
    if (!['availability', 'object', 'path', 'config'].includes(mode)) return;

    // Change mode and reset tool to a safe default (select) so that
    // tools from a previous mode don't leak into the new mode.
    commit('SET_EDITOR_MODE', mode);
    commit('SET_SELECTED_TOOL', 'select');
  },

  selectTool({ commit }, tool) {
    commit('SET_SELECTED_TOOL', tool);
  },

  selectCell({ commit }, cell) {
    commit('SET_SELECTED_CELL', cell);
  },

  toggleGridVisibility({ commit, state }) {
    commit('SET_GRID_VISIBLE', !state.editorState.gridVisible);
  },

  toggleBackgroundVisibility({ commit, state }) {
    commit('SET_BACKGROUND_VISIBLE', !state.editorState.backgroundVisible);
  },

  toggleAvailabilityVisibility({ commit, state }) {
    commit('SET_AVAILABILITY_VISIBLE', !state.editorState.availabilityVisible);
  },

  togglePathsVisibility({ commit, state }) {
    commit('SET_PATHS_VISIBLE', !state.editorState.pathsVisible);
  },

  toggleObjectsVisibility({ commit, state }) {
    commit('SET_OBJECTS_VISIBLE', !state.editorState.objectsVisible);
  },

  updateGridConfig({ commit }, config) {
    commit('UPDATE_GRID_CONFIG', config);
  },

  updateCell({ commit }, payload) {
    commit('UPDATE_CELL', payload);
  },

  toggleCellAvailability({ commit }, { x, y, layer }) {
    commit('TOGGLE_CELL_AVAILABILITY', { x, y, layer });
  },

  toggleCellConnection({ commit }, { x, y, layer, direction }) {
    commit('TOGGLE_EDGE', { x, y, layer, direction });
  },

  placeCellSpawner({ commit }, { x, y, layer, spawner }) {
    commit('SET_CELL_SPAWNER', { x, y, layer, spawner });
  },

  placeCellGameObject({ commit }, { x, y, layer, gameObject }) {
    commit('SET_CELL_GAME_OBJECT', { x, y, layer, gameObject });
  },

  clearCellContent({ commit }, { x, y, layer }) {
    commit('CLEAR_CELL_CONTENT', { x, y, layer });
  },

  setBackgroundImage({ commit }, imageData) {
    commit('SET_BACKGROUND_IMAGE', imageData);
  },

  updateMapMetadata({ commit }, metadata) {
    commit('UPDATE_MAP_METADATA', metadata);
  },

  autoGenerateEdges({ commit }) {
    commit('AUTO_GENERATE_EDGES');
  },

  saveMap({ state, commit }) {
    // Mark as clean after save
    commit('SET_DIRTY', false);
    return state.mapData;
  },

  resetEditor({ commit }) {
    commit('SET_MAP_DATA', null);
    commit('SET_CURRENT_LAYER', 0);
    commit('SET_SELECTED_TOOL', 'select');
    commit('SET_SELECTED_CELL', null);
    commit('SET_EDITOR_MODE', 'availability');
    commit('SET_GRID_VISIBLE', true);
    commit('SET_BACKGROUND_VISIBLE', true);
    commit('SET_AVAILABILITY_VISIBLE', true);
    commit('SET_PATHS_VISIBLE', true);
    commit('SET_OBJECTS_VISIBLE', true);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
