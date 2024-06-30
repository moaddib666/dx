import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from '../components/scenes/LoginScreen';
// import CharacterCreationScreen from '../components/scenes/CharacterCreationScreen';
import CharacterSelectionScreen from '../components/scenes/CharacterSelectionScreen';
import FightScreen from '../components/scenes/FightScreen';
// import FightResultScreen from '../components/scenes/FightResultScreen';

const Stack = createStackNavigator();

function Navigation() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Login">
                <Stack.Screen name="Login" component={LoginScreen} />
                {/*<Stack.Screen name="CharacterCreation" component={CharacterCreationScreen} />*/}
                <Stack.Screen name="CharacterSelection" component={CharacterSelectionScreen} />
                <Stack.Screen name="Fight" component={FightScreen} />
                {/*<Stack.Screen name="FightResult" component={FightResultScreen} />*/}
            </Stack.Navigator>
        </NavigationContainer>
    );
}

export default Navigation;
