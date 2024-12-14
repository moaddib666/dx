import { createStore } from 'vuex';
import Cookies from 'js-cookie';
import {jwtDecode} from 'jwt-decode'; // Adjust the import statement

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
      Cookies.set('dx_backend_token', token);
    },
    clearAuth(state) {
      state.user = null;
      state.token = null;
      Cookies.remove('dx_backend_token');
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
  },
  modules: {}
});
