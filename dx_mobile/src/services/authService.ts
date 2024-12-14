import {AuthGameApi} from "../api";

const login = async (email: string, password: string) => {
    try {
        const response = await AuthGameApi.authJwtTokenCreate( { email, password });
        return response.data;
    } catch (error) {
        throw new Error('Failed to login');
    }
};

const logout = async () => {
    try {
        // const response = await AuthGameApi.authJwtTokenCreate();
        // return response.data;
        return {}
    } catch (error) {
        throw new Error('Failed to logout');
    }
};

export default { login, logout };
