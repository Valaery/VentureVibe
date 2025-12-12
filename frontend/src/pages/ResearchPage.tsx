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
            <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 shadow-sm">
                <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <h1 className="text-3xl font-bold bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
                            VentureVibe
                        </h1>
                        <span className="hidden sm:inline-block text-xs text-muted-foreground border-l pl-3 ml-1">
                            AI-Powered Validation
                        </span>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-muted-foreground hidden md:inline">Welcome, {user?.email}</span>
                        <Button variant="outline" size="sm" onClick={logout} className="hover:bg-destructive/10 hover:text-destructive hover:border-destructive">Logout</Button>
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
