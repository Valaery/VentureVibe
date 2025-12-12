import React, { useState } from 'react';
import { ResearchForm } from '@/features/research/components/ResearchForm';
import { ResearchResultDisplay } from '@/features/research/components/ResearchResultDisplay';
import { AppShell } from '@/components/layout/AppShell';
import { useResearchMutation } from '@/features/research/hooks/mutations/useResearchMutation';

const ResearchPage: React.FC = () => {
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
        <AppShell>
            <div className="space-y-8">
                {!result && (
                    <div className="text-center space-y-2 mb-8">
                        <h2 className="text-3xl font-bold tracking-tight">Evaluate your next big idea</h2>
                        <p className="text-muted-foreground">AI-powered market research and strategy at your fingertips.</p>
                    </div>
                )}

                <ResearchForm onSubmit={handleResearchSubmit} isLoading={mutation.isPending} />

                {result && <ResearchResultDisplay result={result} />}
            </div>
        </AppShell>
    );
};

export default ResearchPage;
