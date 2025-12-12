import { VentureVibeLogo } from '@/components/brand/VentureVibeLogo';
import React, { useState } from 'react';
import { ResearchForm } from '@/features/research/components/ResearchForm';
import { ResearchResultDisplay } from '@/features/research/components/ResearchResultDisplay';
import { useAuthContext } from '@/features/auth/hooks/useAuthContext';
import { Button } from '@/components/ui/button';
import { useResearchMutation } from '@/features/research/hooks/mutations/useResearchMutation';

const ResearchPage: React.FC = () => {
    const { logout, user } = useAuthContext();
    const [result, setResult] = useState<any>(null);
    const mutation = useResearchMutation();

    const handleResearchSubmit = async (content: string, audience: string) => {
        mutation.mutate({ content, target_audience: audience }, {
            onSuccess: (data: any) => {
                setResult(data);
            },
            onError: (error: any) => {
                console.error("Research failed", error);
            }
        });
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/50 dark:from-slate-950 dark:via-blue-950/30 dark:to-indigo-950/50 pb-10">
            <header className="sticky top-0 z-50 border-b border-white/20 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl supports-[backdrop-filter]:bg-white/60 dark:supports-[backdrop-filter]:bg-slate-900/60 shadow-lg shadow-primary/5 transition-all duration-300">
                <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <VentureVibeLogo size="md" />
                        <div className="flex flex-col">
                            <h1 className="text-2xl font-bold font-display bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
                                VentureVibe
                            </h1>
                            <span className="hidden sm:inline-block text-xs text-muted-foreground">
                                AI-Powered Validation
                            </span>
                        </div>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="hidden md:flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white font-semibold text-sm shadow-md">
                                {user?.email?.[0].toUpperCase()}
                            </div>
                            <span className="text-sm text-muted-foreground">{user?.email}</span>
                        </div>
                        <Button variant="outline" size="sm" onClick={logout} className="hover:bg-destructive/10 hover:text-destructive hover:border-destructive transition-all duration-200">Logout</Button>
                    </div>
                </div>
            </header>

            <main className="container mx-auto px-4 py-8 space-y-8">
                {!result && (
                    <div className="text-center space-y-4 mb-8 mt-8">
                        <h2 className="text-4xl md:text-5xl font-bold tracking-tight bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
                            Validate Ideas at the Speed of Thought
                        </h2>
                        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                            Get instant AI-powered market research, competitive analysis, and strategic insights for your next big idea.
                        </p>
                    </div>
                )}

                <ResearchForm onSubmit={handleResearchSubmit} isLoading={mutation.isPending} />

                {result && <ResearchResultDisplay result={result} />}
            </main>
        </div>
    );
};

export default ResearchPage;
