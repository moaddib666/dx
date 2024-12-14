// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './reducers/authReducer';
import characterReducer from './reducers/characterReducer';
import fightReducer from './reducers/fightReducer';
import authService from '../services/authService';  // This will be our custom argument

const store = configureStore({
    reducer: {
        auth: authReducer,
        character: characterReducer,
        fight: fightReducer,
    },
    middleware: getDefaultMiddleware =>
        getDefaultMiddleware({
            thunk: {
                extraArgument: authService,
            },
        }),
});

export default store;

// Optional: Export RootState and AppDispatch types for usage in components
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
