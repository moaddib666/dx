/**
 * Vuex Store Module for Tabletop Map Player
 * Manages player/NPC spawning, selection, movement, and action points
 */

const state = {
  // Current loaded map data (imported from editor)
  mapData: null,

  // Spawned players/NPCs on the map
  players: [],

  // Currently selected player
  selectedPlayerId: null,

  // Player state
  playerState: {
    currentLayer: 0,
    gridVisible: true,
    backgroundVisible: true
  },

  // Next player ID counter
  nextPlayerId: 1
};

const getters = {
  currentMap: (state) => state.mapData,

  players: (state) => state.players,

  selectedPlayer: (state) => {
    if (!state.selectedPlayerId) return null;
    return state.players.find(p => p.id === state.selectedPlayerId);
  },

  selectedPlayerId: (state) => state.selectedPlayerId,

  currentLayer: (state) => state.playerState.currentLayer,

  gridVisible: (state) => state.playerState.gridVisible,

  backgroundVisible: (state) => state.playerState.backgroundVisible,

  gridConfig: (state) => state.mapData?.grid || null,

  // Get player at specific position
  getPlayerAt: (state) => (x, y, layer) => {
    return state.players.find(p => p.x === x && p.y === y && p.layer === layer);
  }
};

const mutations = {
  SET_MAP_DATA(state, mapData) {
    state.mapData = mapData;
    // Reset players when loading new map
    state.players = [];
    state.selectedPlayerId = null;
    state.nextPlayerId = 1;
  },

  SPAWN_PLAYER(state, { x, y, layer, name, image, actionPoints }) {
    const newPlayer = {
      id: state.nextPlayerId++,
      x,
      y,
      layer,
      name: name || `Player ${state.nextPlayerId - 1}`,
      image: image || null,
      maxActionPoints: actionPoints || 10,
      currentActionPoints: actionPoints || 10
    };
    state.players.push(newPlayer);
  },

  REMOVE_PLAYER(state, playerId) {
    const index = state.players.findIndex(p => p.id === playerId);
    if (index !== -1) {
      state.players.splice(index, 1);
      if (state.selectedPlayerId === playerId) {
        state.selectedPlayerId = null;
      }
    }
  },

  SELECT_PLAYER(state, playerId) {
    state.selectedPlayerId = playerId;
  },

  MOVE_PLAYER(state, { playerId, x, y, layer, cost }) {
    const player = state.players.find(p => p.id === playerId);
    if (player) {
      player.x = x;
      player.y = y;
      player.layer = layer;
      player.currentActionPoints = Math.max(0, player.currentActionPoints - cost);
    }
  },

  REFILL_ACTION_POINTS(state, playerId) {
    const player = state.players.find(p => p.id === playerId);
    if (player) {
      player.currentActionPoints = player.maxActionPoints;
    }
  },

  SET_ACTION_POINTS(state, { playerId, actionPoints }) {
    const player = state.players.find(p => p.id === playerId);
    if (player) {
      player.currentActionPoints = Math.min(actionPoints, player.maxActionPoints);
    }
  },

  SET_CURRENT_LAYER(state, layer) {
    state.playerState.currentLayer = layer;
  },

  SET_GRID_VISIBLE(state, visible) {
    state.playerState.gridVisible = visible;
  },

  SET_BACKGROUND_VISIBLE(state, visible) {
    state.playerState.backgroundVisible = visible;
  },

  SET_BACKGROUND_IMAGE(state, imageData) {
    if (state.mapData) {
      state.mapData.backgroundImage = imageData;
    }
  }
};

const actions = {
  loadMap({ commit }, mapData) {
    commit('SET_MAP_DATA', mapData);
  },

  spawnPlayer({ commit }, payload) {
    commit('SPAWN_PLAYER', payload);
  },

  removePlayer({ commit }, playerId) {
    commit('REMOVE_PLAYER', playerId);
  },

  selectPlayer({ commit }, playerId) {
    commit('SELECT_PLAYER', playerId);
  },

  movePlayer({ commit }, payload) {
    commit('MOVE_PLAYER', payload);
  },

  refillActionPoints({ commit }, playerId) {
    commit('REFILL_ACTION_POINTS', playerId);
  },

  setActionPoints({ commit }, payload) {
    commit('SET_ACTION_POINTS', payload);
  },

  setCurrentLayer({ commit }, layer) {
    commit('SET_CURRENT_LAYER', layer);
  },

  toggleGridVisibility({ commit, state }) {
    commit('SET_GRID_VISIBLE', !state.playerState.gridVisible);
  },

  toggleBackgroundVisibility({ commit, state }) {
    commit('SET_BACKGROUND_VISIBLE', !state.playerState.backgroundVisible);
  },

  setBackgroundImage({ commit }, imageData) {
    commit('SET_BACKGROUND_IMAGE', imageData);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
