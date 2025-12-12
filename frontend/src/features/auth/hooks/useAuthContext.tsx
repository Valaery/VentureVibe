import { useState, useContext, createContext, useEffect } from "react";
import { authService } from "../data/services/authService";

import { LoginInput, RegisterInput } from "../data/schemas/authSchemas";
import { useNavigate } from "react-router-dom";

interface User {
    id: string; // Placeholder ID
    email: string;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (data: LoginInput) => Promise<void>;
    register: (data: RegisterInput) => Promise<void>;
    logout: () => void;
    isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const navigate = useNavigate();

    // In a real app, useQuery to fetch user if token exists
    useEffect(() => {
        if (token && !user) {
            // Decoding token or fetching /me would go here
            // setUser({ id: "1", email: "restored@example.com" }); 
        }
    }, [token, user]);

    const login = async (data: LoginInput) => {
        const res = await authService.login(data);
        setToken(res.access_token);
        localStorage.setItem('token', res.access_token);
        setUser({ id: "new", email: data.email }); // Simplified
        navigate('/research');
    };

    const register = async (data: RegisterInput) => {
        await authService.register(data);
        await login({ email: data.email, password: data.password });
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <AuthContext.Provider value={{ user, token, login, register, logout, isAuthenticated: !!token }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuthContext = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuthContext must be used within an AuthProvider');
    }
    return context;
};
