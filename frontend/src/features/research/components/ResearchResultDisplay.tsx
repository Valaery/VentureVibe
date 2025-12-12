import React from 'react';

import ReactMarkdown from 'react-markdown';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ProgressCircle } from '@/components/ui/progress-circle';
import { Badge } from '@/components/ui/badge';

interface ResearchResultProps {
    result: {
        market_analysis: string;
        feasibility_score: number;
        competitors: string[];
        strategic_advice: string;
    };
}

export const ResearchResultDisplay: React.FC<ResearchResultProps> = ({ result }) => {
    return (
        <div className="space-y-6 animate-in fade-in duration-700">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-blue-100 dark:border-blue-900">
                    <CardHeader>
                        <CardTitle className="text-blue-700 dark:text-blue-300">Feasibility Score</CardTitle>
                    </CardHeader>
                    <CardContent className="flex items-center justify-center py-8">
                        <ProgressCircle value={result.feasibility_score} />
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Competitors</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex flex-wrap gap-2">
                            {result.competitors.map((comp, i) => (
                                <Badge key={i} variant="secondary" className="px-3 py-1 text-sm shadow-sm">
                                    {comp}
                                </Badge>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Market Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="prose prose-sm max-w-none dark:prose-invert">
                        <ReactMarkdown
                            components={{
                                h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mb-4" {...props} />,
                                h2: ({ node, ...props }) => <h2 className="text-xl font-semibold mb-3" {...props} />,
                                h3: ({ node, ...props }) => <h3 className="text-lg font-semibold mb-2" {...props} />,
                                p: ({ node, ...props }) => <p className="mb-4 leading-relaxed text-muted-foreground" {...props} />,
                                ul: ({ node, ...props }) => <ul className="list-disc pl-6 mb-4 space-y-2" {...props} />,
                                ol: ({ node, ...props }) => <ol className="list-decimal pl-6 mb-4 space-y-2" {...props} />,
                                li: ({ node, ...props }) => <li className="text-muted-foreground" {...props} />,
                                strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
                                em: ({ node, ...props }) => <em className="italic" {...props} />,
                                code: ({ node, ...props }) => <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono" {...props} />,
                            }}
                        >
                            {result.market_analysis}
                        </ReactMarkdown>
                    </div>
                </CardContent>
            </Card>

            <Card className="border-green-100 dark:border-green-900 bg-green-50/50 dark:bg-green-900/10">
                <CardHeader>
                    <CardTitle className="text-green-700 dark:text-green-300">Strategic Advice</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="prose prose-sm max-w-none dark:prose-invert">
                        <ReactMarkdown
                            components={{
                                h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mb-4 text-green-800 dark:text-green-200" {...props} />,
                                h2: ({ node, ...props }) => <h2 className="text-xl font-semibold mb-3 text-green-700 dark:text-green-300" {...props} />,
                                h3: ({ node, ...props }) => <h3 className="text-lg font-semibold mb-2 text-green-600 dark:text-green-400" {...props} />,
                                p: ({ node, ...props }) => <p className="mb-4 leading-relaxed text-gray-700 dark:text-gray-300" {...props} />,
                                ul: ({ node, ...props }) => <ul className="list-disc pl-6 mb-4 space-y-2" {...props} />,
                                ol: ({ node, ...props }) => <ol className="list-decimal pl-6 mb-4 space-y-2" {...props} />,
                                li: ({ node, ...props }) => <li className="text-gray-700 dark:text-gray-300" {...props} />,
                                strong: ({ node, ...props }) => <strong className="font-semibold text-green-800 dark:text-green-200" {...props} />,
                                em: ({ node, ...props }) => <em className="italic text-gray-600 dark:text-gray-400" {...props} />,
                                code: ({ node, ...props }) => <code className="bg-green-100 dark:bg-green-900/30 px-1.5 py-0.5 rounded text-sm font-mono" {...props} />,
                            }}
                        >
                            {result.strategic_advice}
                        </ReactMarkdown>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
