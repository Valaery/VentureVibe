import React, { useState } from 'react';
import { useAuthContext } from '../hooks/useAuthContext';
import { VentureVibeLogo } from '@/components/brand/VentureVibeLogo';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Link } from 'react-router-dom';

export const RegisterForm: React.FC = () => {
    const { register } = useAuthContext();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            // Correct interface usage: object with fields
            await register({ email, password, full_name: fullName });
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Registration failed');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-blue-950 dark:to-indigo-950 animate-in fade-in duration-500">
            <Card className="w-[420px] shadow-2xl border-2 border-primary/20 backdrop-blur-sm bg-white/90 dark:bg-slate-950/90">
                <CardHeader className="space-y-3">
                    <div className="flex flex-col items-center justify-center mb-4 gap-2">
                        <VentureVibeLogo size="lg" animated />
                        <div className="text-4xl font-bold bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent font-display">
                            VentureVibe
                        </div>
                    </div>
                    <CardTitle className="text-center text-2xl">Start Your Free Trial</CardTitle>
                    <CardDescription className="text-center">
                        Join thousands validating ideas at the speed of thought
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent>
                        <div className="grid w-full items-center gap-4">
                            <div className="flex flex-col space-y-1.5">
                                <Label htmlFor="fullName">Full Name</Label>
                                <Input id="fullName" placeholder="John Doe" value={fullName} onChange={(e) => setFullName(e.target.value)} />
                            </div>
                            <div className="flex flex-col space-y-1.5">
                                <Label htmlFor="email">Email</Label>
                                <Input id="email" type="email" placeholder="name@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
                            </div>
                            <div className="flex flex-col space-y-1.5">
                                <Label htmlFor="password">Password</Label>
                                <Input id="password" type="password" placeholder="Min. 8 characters" value={password} onChange={(e) => setPassword(e.target.value)} required />
                            </div>
                        </div>
                        {error && <p className="text-destructive text-sm mt-2">{error}</p>}
                    </CardContent>
                    <CardFooter className="flex flex-col gap-3">
                        <Button className="w-full bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90" type="submit">Create Account</Button>
                        <p className="text-sm text-muted-foreground text-center">
                            Already have an account? <Link to="/login" className="text-primary font-semibold hover:underline">Sign In</Link>
                        </p>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
};
