import authService from '../../services/authService';
import {AppDispatch} from "../index";

export const loginSuccess = (user: { name: string; token: string }) => ({
    type: 'LOGIN_SUCCESS',
    payload: user,
});

export const login = (email: string, password: string) => {
    return async (dispatch: AppDispatch) => {
        try {
            const data = await authService.login(email, password);
            dispatch(loginSuccess({ name: "John Doy", token: data.access }));
            return { success: true };
        } catch (error) {
            return { success: false, message: error.message };
        }
    };
};

export const logout = () => ({
    type: 'LOGOUT',
});
