import AsyncStorage from '@react-native-async-storage/async-storage';

class Storage {

    public static prefix = 'game_';

    async setItem(key: string, value: string) {
        await AsyncStorage.setItem(`${Storage.prefix}:${key}`, value);
    }

    async getItem(key: string) {
        return await AsyncStorage.getItem(`${Storage.prefix}:${key}`);
    }

    async removeItem(key: string) {
        await AsyncStorage.removeItem(`${Storage.prefix}:${key}`);
    }
}

export class SessionStorage extends Storage {

    public static prefix = 'session_';

    async NewSession(token: string) {
        await this.setItem('token', token);
    }

    async GetSession() {
        return await this.getItem('token');
    }
}
