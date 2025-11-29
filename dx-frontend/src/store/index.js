import { createStore } from 'vuex';
import Cookies from 'js-cookie';
import {jwtDecode} from 'jwt-decode'; // Adjust the import statement
import tabletopEditor from './modules/tabletopEditor';
import tabletopPlayer from './modules/tabletopPlayer';

export default createStore({
  state: {
    user: null,
    token: Cookies.get('dx_backend_token') || null,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
      // Set secure flag based on whether the connection is HTTPS
      const isSecure = window.location.protocol === 'https:';
      Cookies.set('dx_backend_token', token, { secure: isSecure });
    },
    clearAuth(state) {
      state.user = null;
      state.token = null;
      // Use the same secure setting when removing cookies
      const isSecure = window.location.protocol === 'https:';
      Cookies.remove('dx_backend_token', { secure: isSecure });
    },
  },
  actions: {
    login({ commit }, { token }) {
      commit('setToken', token);
    },
    logout({ commit }) {
      commit('clearAuth');
    },
  },
  getters: {
    isAuthenticated: state => {
      if (state.token) {
        try {
          const decodedToken = jwtDecode(state.token); // Use jwt_decode
          const currentTime = Date.now() / 1000;
          return decodedToken.exp > currentTime;
        } catch (error) {
          return false;
        }
      }
      return false;
    },
    getAuthToken: state => state.token,
  },
  modules: {
    tabletopEditor,
    tabletopPlayer
  }
});
