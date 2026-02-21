import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ProgressCircle } from '@/components/ui/progress-circle';
import type { ResearchResult, InvestmentReadiness, ConfidenceLevel } from '../data/services/researchService';

const INVESTMENT_STAGES: InvestmentReadiness[] = [
    'pre_idea', 'idea_stage', 'mvp_ready', 'seed_ready', 'series_a_ready'
];

const STAGE_LABELS: Record<InvestmentReadiness, string> = {
    pre_idea: 'Pre-Idea',
    idea_stage: 'Idea Stage',
    mvp_ready: 'MVP Ready',
    seed_ready: 'Seed Ready',
    series_a_ready: 'Series A',
};

const CONFIDENCE_COLORS: Record<ConfidenceLevel, string> = {
    low: 'bg-red-100 text-red-700 border-red-200',
    medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    high: 'bg-green-100 text-green-700 border-green-200',
};

interface SummaryStripProps {
    result: ResearchResult;
}

export const SummaryStrip: React.FC<SummaryStripProps> = ({ result }) => {
    const currentStageIndex = INVESTMENT_STAGES.indexOf(result.investment_readiness);

    return (
        <Card className="border-primary/20 bg-gradient-to-r from-primary/5 to-secondary/5">
            <CardContent className="pt-6">
                <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                    <div className="flex items-center gap-4 shrink-0">
                        <ProgressCircle value={result.feasibility_score} />
                        <div>
                            <p className="text-sm text-muted-foreground">Feasibility Score</p>
                            <Badge variant="outline" className={CONFIDENCE_COLORS[result.confidence_level]}>
                                {result.confidence_level} confidence
                            </Badge>
                        </div>
                    </div>

                    <div className="h-px md:h-12 md:w-px bg-border w-full md:w-auto" />

                    <div className="flex-1 min-w-0">
                        <p className="text-xs text-muted-foreground mb-2 font-medium uppercase tracking-wide">
                            Investment Readiness
                        </p>
                        <div className="flex items-center gap-1">
                            {INVESTMENT_STAGES.map((stage, i) => (
                                <React.Fragment key={stage}>
                                    <div className="flex flex-col items-center">
                                        <div className={`w-3 h-3 rounded-full border-2 transition-colors ${
                                            i < currentStageIndex
                                                ? 'bg-primary border-primary'
                                                : i === currentStageIndex
                                                ? 'bg-primary border-primary ring-2 ring-primary/30'
                                                : 'bg-muted border-border'
                                        }`} />
                                        <span className={`text-xs mt-1 hidden sm:block ${
                                            i === currentStageIndex
                                                ? 'font-semibold text-primary'
                                                : 'text-muted-foreground'
                                        }`}>
                                            {STAGE_LABELS[stage]}
                                        </span>
                                    </div>
                                    {i < INVESTMENT_STAGES.length - 1 && (
                                        <div className={`flex-1 h-0.5 mb-4 ${
                                            i < currentStageIndex ? 'bg-primary' : 'bg-border'
                                        }`} />
                                    )}
                                </React.Fragment>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="mt-4 pt-4 border-t border-border/50">
                    <blockquote className="border-l-4 border-primary pl-4 italic text-muted-foreground text-justify">
                        {result.executive_summary}
                    </blockquote>
                </div>
            </CardContent>
        </Card>
    );
};
