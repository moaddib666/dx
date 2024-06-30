import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../../store/actions/authActions';
import { AppDispatch, RootState } from '../../store';

const LoginScreen = ({ navigation }: { navigation: any }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const dispatch = useDispatch<AppDispatch>();

    const handleLogin = async () => {
        const result = await dispatch(login(email, password));
        if (!result.success) {
            setError(result.message);
        } else {
            navigation.navigate('CharacterSelection');
        }
    };

    return (
        <View style={styles.loginContainer}>
            <View style={styles.loginForm}>
                <TextInput
                    style={styles.input}
                    placeholder="E-mail"
                    placeholderTextColor="#ccc"
                    value={email}
                    onChangeText={setEmail}
                    keyboardType="email-address"
                />
                <TextInput
                    style={styles.input}
                    placeholder="Password"
                    placeholderTextColor="#ccc"
                    value={password}
                    onChangeText={setPassword}
                    secureTextEntry
                />
                {error && <Text style={styles.errorText}>{error}</Text>}
                <Button title="Login" onPress={handleLogin} />
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    loginContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
    },
    loginForm: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 20,
        borderRadius: 10,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    input: {
        width: '100%',
        marginBottom: 15,
        padding: 10,
        borderRadius: 5,
        borderColor: '#ccc',
        borderWidth: 1,
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        color: '#fff',
    },
    errorText: {
        color: 'red',
        marginBottom: 15,
    },
});

export default LoginScreen;
