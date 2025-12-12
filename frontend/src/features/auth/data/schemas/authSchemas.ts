import { z } from "zod";

export const loginSchema = z.object({
    email: z.string().email({ message: "Invalid email address" }),
    password: z.string().min(6, { message: "Password must be at least 6 characters" }),
});

export const registerSchema = loginSchema.extend({
    full_name: z.string().optional(),
});

export const userSchema = z.object({
    id: z.string(),
    email: z.string().email(),
    full_name: z.string().optional(),
});

export const authResponseSchema = z.object({
    access_token: z.string(),
    token_type: z.string().default("bearer"),
});

export type LoginInput = z.infer<typeof loginSchema>;
export type RegisterInput = z.infer<typeof registerSchema>;
export type User = z.infer<typeof userSchema>;
export type AuthResponse = z.infer<typeof authResponseSchema>;
