interface AuthState {
    isAuthenticated: boolean;
    user: { name: string; token: string } | null;
    error: string | null;
}

const initialState: AuthState = {
    isAuthenticated: false,
    user: null,
    error: null,
};

const authReducer = (state = initialState, action: any): AuthState => {
    switch (action.type) {
        case 'LOGIN_SUCCESS':
            return { ...state, isAuthenticated: true, user: action.payload, error: null };
        case 'LOGIN_FAILURE':
            return { ...state, isAuthenticated: false, user: null, error: action.payload };
        case 'LOGOUT':
            return { ...state, isAuthenticated: false, user: null, error: null };
        default:
            return state;
    }
};

export default authReducer;
