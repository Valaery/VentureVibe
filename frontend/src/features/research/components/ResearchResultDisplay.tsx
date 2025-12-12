import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { TrendingUp, Users, Lightbulb, Target } from 'lucide-react';

interface ResearchResultProps {
    result: {
        market_analysis: string;
        feasibility_score: number;
        competitors: string[];
        strategic_advice: string;
    };
}

export const ResearchResultDisplay: React.FC<ResearchResultProps> = ({ result }) => {
    const getFeasibilityColor = (score: number) => {
        if (score >= 80) return 'bg-green-500';
        if (score >= 60) return 'bg-blue-500';
        if (score >= 40) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    const getFeasibilityLabel = (score: number) => {
        if (score >= 80) return 'Highly Feasible';
        if (score >= 60) return 'Feasible';
        if (score >= 40) return 'Moderate';
        return 'Challenging';
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-700">
            {/* Feasibility Score Card */}
            <Card className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-950/30 dark:via-indigo-950/30 dark:to-purple-950/30 border-2 border-primary/20 shadow-lg">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-primary">
                        <Target className="h-5 w-5" />
                        Feasibility Assessment
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <div className="relative">
                                <div className="text-6xl font-bold bg-gradient-to-br from-blue-600 to-purple-600 bg-clip-text text-transparent">
                                    {result.feasibility_score}
                                </div>
                                <span className="text-2xl text-muted-foreground ml-1">/100</span>
                            </div>
                        </div>
                        <Badge
                            className={`${getFeasibilityColor(result.feasibility_score)} text-white px-4 py-2 text-sm`}
                        >
                            {getFeasibilityLabel(result.feasibility_score)}
                        </Badge>
                    </div>
                </CardContent>
            </Card>

            {/* Accordion for Research Details */}
            <Card className="shadow-lg">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <TrendingUp className="h-5 w-5" />
                        Research Insights
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <Accordion type="multiple" defaultValue={['market', 'competitors', 'strategy']} className="w-full">
                        <AccordionItem value="market">
                            <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                                <div className="flex items-center gap-2">
                                    <TrendingUp className="h-4 w-4" />
                                    Market Analysis
                                </div>
                            </AccordionTrigger>
                            <AccordionContent>
                                <ScrollArea className="h-auto max-h-[300px] pr-4">
                                    <p className="whitespace-pre-wrap text-muted-foreground leading-relaxed">
                                        {result.market_analysis}
                                    </p>
                                </ScrollArea>
                            </AccordionContent>
                        </AccordionItem>

                        <AccordionItem value="competitors">
                            <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                                <div className="flex items-center gap-2">
                                    <Users className="h-4 w-4" />
                                    Competitors ({result.competitors.length})
                                </div>
                            </AccordionTrigger>
                            <AccordionContent>
                                <div className="space-y-2">
                                    {result.competitors.map((comp, i) => (
                                        <div
                                            key={i}
                                            className="flex items-start gap-2 p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
                                        >
                                            <Badge variant="outline" className="mt-0.5">{i + 1}</Badge>
                                            <span className="text-sm">{comp}</span>
                                        </div>
                                    ))}
                                </div>
                            </AccordionContent>
                        </AccordionItem>

                        <AccordionItem value="strategy">
                            <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                                <div className="flex items-center gap-2">
                                    <Lightbulb className="h-4 w-4" />
                                    Strategic Advice
                                </div>
                            </AccordionTrigger>
                            <AccordionContent>
                                <ScrollArea className="h-auto max-h-[300px] pr-4">
                                    <div className="p-4 rounded-lg bg-green-50/50 dark:bg-green-950/20 border border-green-200 dark:border-green-900">
                                        <p className="whitespace-pre-wrap leading-relaxed text-foreground">
                                            {result.strategic_advice}
                                        </p>
                                    </div>
                                </ScrollArea>
                            </AccordionContent>
                        </AccordionItem>
                    </Accordion>
                </CardContent>
            </Card>
        </div>
    );
};
