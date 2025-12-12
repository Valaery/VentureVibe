import { useState, useContext, createContext, useEffect } from "react";
import { useLoginMutation } from "./mutations/useLoginMutation";
import { useRegisterMutation } from "./mutations/useRegisterMutation";

import type { LoginInput, RegisterInput, User } from "../data/schemas/authSchemas";
import { useNavigate } from "react-router-dom";

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (data: LoginInput) => Promise<void>;
    register: (data: RegisterInput) => Promise<void>;
    logout: () => void;
    isAuthenticated: boolean;
    isLoggingIn: boolean;
    isRegistering: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const navigate = useNavigate();

    const loginMutation = useLoginMutation();
    const registerMutation = useRegisterMutation();

    // In a real app, useQuery to fetch user if token exists
    useEffect(() => {
        if (token && !user) {
            // Decoding token or fetching /me would go here
            // For now, we'll just set a placeholder user
            // setUser({ id: "1", email: "restored@example.com" }); 
        }
    }, [token, user]);

    const login = async (data: LoginInput) => {
        const res = await loginMutation.mutateAsync(data);
        setToken(res.access_token);
        localStorage.setItem('token', res.access_token);
        setUser({ id: "new", email: data.email }); // Simplified
        navigate('/research');
    };

    const register = async (data: RegisterInput) => {
        await registerMutation.mutateAsync(data);
        await login({ email: data.email, password: data.password });
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                login,
                register,
                logout,
                isAuthenticated: !!token,
                isLoggingIn: loginMutation.isPending,
                isRegistering: registerMutation.isPending,
            }}
        >
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
