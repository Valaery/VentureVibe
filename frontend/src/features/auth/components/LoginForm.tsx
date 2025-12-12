import React, { useState } from 'react';
import { useAuthContext } from '../hooks/useAuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Link } from 'react-router-dom';

export const LoginForm: React.FC = () => {
    const { login } = useAuthContext();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await login({ email, password });
        } catch (err) {
            setError('Invalid email or password');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-blue-950 dark:to-indigo-950">
            <Card className="w-[420px] shadow-2xl border-2 border-primary/20">
                <CardHeader className="space-y-3">
                    <div className="flex items-center justify-center mb-2">
                        <div className="text-4xl font-bold bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
                            VentureVibe
                        </div>
                    </div>
                    <CardTitle className="text-center text-2xl">Welcome Back</CardTitle>
                    <CardDescription className="text-center">
                        Sign in to validate your next big idea
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent>
                        <div className="grid w-full items-center gap-4">
                            <div className="flex flex-col space-y-1.5">
                                <Label htmlFor="email">Email</Label>
                                <Input id="email" type="email" placeholder="name@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
                            </div>
                            <div className="flex flex-col space-y-1.5">
                                <Label htmlFor="password">Password</Label>
                                <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                            </div>
                        </div>
                        {error && <p className="text-destructive text-sm mt-2">{error}</p>}
                    </CardContent>
                    <CardFooter className="flex flex-col gap-3">
                        <Button className="w-full bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90" type="submit">Sign In</Button>
                        <p className="text-sm text-muted-foreground text-center">
                            Don't have an account? <Link to="/register" className="text-primary font-semibold hover:underline">Start Free Trial</Link>
                        </p>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
};
