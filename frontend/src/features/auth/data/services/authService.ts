import { api } from "@/core/data/api";
import { LoginInput, RegisterInput } from "../schemas/authSchemas";

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export const authService = {
    login: async (data: LoginInput): Promise<AuthResponse> => {
        const formData = new FormData();
        formData.append('username', data.email);
        formData.append('password', data.password);

        const response = await api.post<AuthResponse>('/auth/token', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        return response.data;
    },

    register: async (data: RegisterInput): Promise<any> => {
        const response = await api.post('/auth/register', {
            email: data.email,
            password: data.password,
            full_name: data.full_name
        });
        return response.data;
    }
};
