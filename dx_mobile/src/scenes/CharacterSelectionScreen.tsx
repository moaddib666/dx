import React from 'react';
import { View, Text, Button } from 'react-native';
import { useSelector } from 'react-redux';

const CharacterSelectionScreen = ({ navigation }: { navigation: any }) => {
    const user = useSelector((state: any) => state.auth.user);

    return (
        <View>
            <Text>Welcome, {user.name}</Text>
            <Button title="Create Character" onPress={() => navigation.navigate('CharacterCreation')} />
            <Button title="Select Character" onPress={() => navigation.navigate('Fight')} />
        </View>
    );
};

export default CharacterSelectionScreen;
