import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea'; // Need to create this or use standard textarea
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';

interface ResearchFormProps {
    onSubmit: (content: string, audience: string) => Promise<void>;
    isLoading: boolean;
}

export const ResearchForm: React.FC<ResearchFormProps> = ({ onSubmit, isLoading }) => {
    const [content, setContent] = useState('');
    const [audience, setAudience] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(content, audience);
    };

    return (
        <Card className="w-full max-w-2xl mx-auto shadow-xl border-2 border-primary/20 bg-card/50 backdrop-blur">
            <CardHeader>
                <CardTitle className="text-2xl bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Validate Your Product Idea</CardTitle>
                <CardDescription>Tell us about your product concept and target audience to get instant AI-powered insights.</CardDescription>
            </CardHeader>
            <form onSubmit={handleSubmit}>
                <CardContent className="space-y-6">
                    <div className="space-y-2">
                        <Label htmlFor="content">Product Idea</Label>
                        <Textarea
                            id="content"
                            placeholder="Describe your product idea in detail (e.g., 'A subscription service for high-end coffee beans with AI-based taste matching')..."
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            required
                            className="min-h-[120px]"
                        />
                        <p className="text-xs text-muted-foreground text-right border-t pt-2 mt-2">
                            {content.length} characters
                        </p>
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="audience">Target Audience</Label>
                        <Input
                            id="audience"
                            placeholder="e.g., Remote workers, Coffee enthusiasts, SaaS founders..."
                            value={audience}
                            onChange={(e) => setAudience(e.target.value)}
                            required
                        />
                    </div>
                </CardContent>
                <CardFooter>
                    <Button
                        type="submit"
                        variant="premium"
                        className="w-full"
                        disabled={isLoading}
                        size="lg"
                    >
                        {isLoading ? (
                            <>
                                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                AI Agents Analyzing...
                            </>
                        ) : (
                            'Get Instant Validation'
                        )}
                    </Button>
                </CardFooter>
            </form>
        </Card>
    );
};
