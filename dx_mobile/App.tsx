import { StyleSheet, Text, View } from 'react-native';
import {Provider} from "react-redux";
import store from "./src/store";
import React, {Component} from "react";
import Navigation from "./src/navigation/Navigation";
import {DefaultSessionStorage} from "./src/storage";
import {loginSuccess} from "./src/store/actions/authActions";
import connectBus from "./src/services/eventsService";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});



export default class App extends Component {
    state = {
        token: null,
        isLoaded: false,
    };

    async componentDidMount() {
        const savedToken = await DefaultSessionStorage.GetSession();
        if (savedToken) {
            store.dispatch(loginSuccess({ name: 'SavedUser', token: savedToken }));
            await connectBus(); // Connect WebSocket
            this.setState({ token: savedToken, isLoaded: true });
        } else {
            this.setState({ isLoaded: true });
        }
    }

    handleLoginSuccess = async (userToken: string) => {
        await DefaultSessionStorage.NewSession(userToken);
        await connectBus(); // Connect WebSocket
        this.setState({ token: userToken });
    };

    render() {
        const { token, isLoaded } = this.state;

        if (!isLoaded) {
            return null; // or a loading spinner
        }

        return (
            <Provider store={store}>
                <Navigation  />
            </Provider>
        );
    }
}
