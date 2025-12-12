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
        <Card className="w-full max-w-2xl mx-auto shadow-lg border-2 border-primary/10">
            <CardHeader>
                <CardTitle className="text-2xl text-primary">New Product Research</CardTitle>
                <CardDescription>Tell us about your product idea and target audience.</CardDescription>
            </CardHeader>
            <form onSubmit={handleSubmit}>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="content">Product Idea</Label>
                        <Textarea
                            id="content"
                            placeholder="Describe your product idea..."
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            required
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="audience">Target Audience</Label>
                        <Input
                            id="audience"
                            placeholder="e.g., Remote workers, Coffee lovers..."
                            value={audience}
                            onChange={(e) => setAudience(e.target.value)}
                            required
                        />
                    </div>
                </CardContent>
                <CardFooter>
                    <Button type="submit" className="w-full" disabled={isLoading}>
                        {isLoading ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Analyzing with Agents...
                            </>
                        ) : (
                            'Start Research'
                        )}
                    </Button>
                </CardFooter>
            </form>
        </Card>
    );
};
