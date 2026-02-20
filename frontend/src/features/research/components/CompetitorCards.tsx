import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import type { CompetitiveAnalysis, Competitor } from '../data/services/researchService';

interface CompetitorCardProps {
    competitor: Competitor;
    type: 'direct' | 'indirect';
}

const CompetitorCard: React.FC<CompetitorCardProps> = ({ competitor, type }) => (
    <Card className={`border-l-4 ${type === 'direct' ? 'border-l-red-400' : 'border-l-amber-400'}`}>
        <CardHeader className="pb-2">
            <div className="flex items-start justify-between gap-2">
                <CardTitle className="text-base">{competitor.name}</CardTitle>
                <Badge variant="outline" className="shrink-0 text-xs">
                    {type === 'direct' ? 'Direct' : 'Indirect'}
                </Badge>
            </div>
            {competitor.estimated_funding_usd_million != null && (
                <p className="text-xs text-muted-foreground">${competitor.estimated_funding_usd_million}M raised</p>
            )}
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
            <div>
                <span className="font-medium text-xs uppercase tracking-wide text-muted-foreground">Positioning</span>
                <p className="mt-0.5">{competitor.positioning}</p>
            </div>
            <div>
                <span className="font-medium text-xs uppercase tracking-wide text-muted-foreground">Business Model</span>
                <p className="mt-0.5">{competitor.business_model}</p>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 rounded-md p-2">
                <span className="font-medium text-xs uppercase tracking-wide text-green-700 dark:text-green-300">Key Weakness</span>
                <p className="mt-0.5 text-green-800 dark:text-green-200">{competitor.primary_weakness}</p>
            </div>
        </CardContent>
    </Card>
);

interface CompetitorCardsProps {
    competitiveAnalysis: CompetitiveAnalysis;
}

export const CompetitorCards: React.FC<CompetitorCardsProps> = ({ competitiveAnalysis }) => {
    const { direct_competitors, indirect_competitors, competitive_moat, differentiation_score } = competitiveAnalysis;

    return (
        <div className="space-y-4">
            <div className="flex items-center gap-3">
                <span className="text-sm font-medium">Differentiation Score</span>
                <div className="flex gap-0.5">
                    {Array.from({ length: 10 }).map((_, i) => (
                        <div key={i} className={`w-2 h-4 rounded-sm ${i < differentiation_score ? 'bg-primary' : 'bg-muted'}`} />
                    ))}
                </div>
                <span className="text-sm font-bold text-primary">{differentiation_score}/10</span>
            </div>

            <div className="bg-primary/5 border border-primary/20 rounded-lg p-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-primary mb-1">Your Competitive Moat</p>
                <p className="text-sm">{competitive_moat}</p>
            </div>

            {direct_competitors.length > 0 && (
                <div>
                    <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-red-400" />
                        Direct Competitors ({direct_competitors.length})
                    </h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {direct_competitors.map((c, i) => (
                            <CompetitorCard key={i} competitor={c} type="direct" />
                        ))}
                    </div>
                </div>
            )}

            {indirect_competitors.length > 0 && (
                <>
                    <Separator />
                    <div>
                        <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-amber-400" />
                            Indirect Competitors ({indirect_competitors.length})
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            {indirect_competitors.map((c, i) => (
                                <CompetitorCard key={i} competitor={c} type="indirect" />
                            ))}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};
