import { StyleSheet, Text, View } from 'react-native';
import {Provider} from "react-redux";
import store from "./store";
import React from "react";
import Navigation from "./navigation/Navigation";

export default function App() {
  return (
      <Provider store={store}>
        <Navigation />
      </Provider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
