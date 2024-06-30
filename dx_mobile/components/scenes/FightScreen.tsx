import React from 'react';
import { View, Text, Button } from 'react-native';

const FightScreen = ({ navigation }: { navigation: any }) => {
    return (
        <View>
            <Text>Fight Screen</Text>
            <Button title="End Turn" onPress={() => navigation.navigate('FightResult')} />
        </View>
    );
};

export default FightScreen;