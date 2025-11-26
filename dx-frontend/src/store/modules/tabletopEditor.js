import {
  createNewMap,
  createEmptyCell,
  createDefaultGridConfig,
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
  isDirty: (state) => state.editorState.isDirty,

  // Get cells for current layer
  currentLayerCells: (state) => {
    if (!state.mapData) return [];
    return state.mapData.cells.filter(cell => cell.layer === state.editorState.currentLayer);
  },

  // Get specific cell
  getCell: (state) => (x, y, layer) => {
    if (!state.mapData) return null;
    return state.mapData.cells.find(
      cell => cell.x === x && cell.y === y && cell.layer === layer
    );
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
    state.mapData = mapData;
    state.editorState.isDirty = false;
  },

  SET_CURRENT_LAYER(state, layer) {
    state.editorState.currentLayer = layer;
    state.editorState.selectedCell = null; // Clear selection when changing layers
  },

  SET_SELECTED_TOOL(state, tool) {
    state.editorState.selectedTool = tool;
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
      state.mapData.cells[cellIndex] = {
        ...state.mapData.cells[cellIndex],
        ...updates
      };
    } else {
      // Create new cell if it doesn't exist
      const newCell = createEmptyCell(x, y, layer);
      state.mapData.cells.push({ ...newCell, ...updates });
    }

    state.editorState.isDirty = true;
  },

  TOGGLE_CELL_AVAILABILITY(state, { x, y, layer }) {
    if (!state.mapData) return;

    const cell = state.mapData.cells.find(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (cell) {
      cell.available = !cell.available;
    } else {
      const newCell = createEmptyCell(x, y, layer);
      newCell.available = false;
      state.mapData.cells.push(newCell);
    }

    state.editorState.isDirty = true;
  },

  TOGGLE_CELL_CONNECTION(state, { x, y, layer, direction }) {
    if (!state.mapData) return;

    let cell = state.mapData.cells.find(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (!cell) {
      cell = createEmptyCell(x, y, layer);
      state.mapData.cells.push(cell);
    }

    cell.connections[direction] = !cell.connections[direction];
    state.editorState.isDirty = true;
  },

  SET_CELL_SPAWNER(state, { x, y, layer, spawner }) {
    if (!state.mapData) return;

    let cell = state.mapData.cells.find(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (!cell) {
      cell = createEmptyCell(x, y, layer);
      state.mapData.cells.push(cell);
    }

    cell.spawner = spawner;
    state.editorState.isDirty = true;
  },

  SET_CELL_GAME_OBJECT(state, { x, y, layer, gameObject }) {
    if (!state.mapData) return;

    let cell = state.mapData.cells.find(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (!cell) {
      cell = createEmptyCell(x, y, layer);
      state.mapData.cells.push(cell);
    }

    cell.gameObject = gameObject;
    state.editorState.isDirty = true;
  },

  CLEAR_CELL_CONTENT(state, { x, y, layer }) {
    if (!state.mapData) return;

    const cell = state.mapData.cells.find(
      c => c.x === x && c.y === y && c.layer === layer
    );

    if (cell) {
      cell.spawner = null;
      cell.gameObject = null;
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
  }
};

const actions = {
  createNewMap({ commit }, { name, author }) {
    const newMap = createNewMap(name, author);
    commit('SET_MAP_DATA', newMap);
  },

  loadMap({ commit }, mapData) {
    commit('SET_MAP_DATA', mapData);
  },

  setCurrentLayer({ commit }, layer) {
    if (layer >= 0 && layer <= 9) {
      commit('SET_CURRENT_LAYER', layer);
    }
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
    commit('TOGGLE_CELL_CONNECTION', { x, y, layer, direction });
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
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
