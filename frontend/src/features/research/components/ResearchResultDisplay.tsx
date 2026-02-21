import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { SummaryStrip } from './SummaryStrip';
import { MarketSizingChart } from './MarketSizingChart';
import { CompetitorCards } from './CompetitorCards';
import { SWOTGrid } from './SWOTGrid';
import { RiskList } from './RiskList';
import { GTMPanel } from './GTMPanel';
import { AgentTimeline } from './AgentTimeline';
import type { ResearchResult } from '../data/services/researchService';

interface ResearchResultProps {
    result: ResearchResult;
}

function downloadJSON(result: ResearchResult) {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research-${result.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function downloadMarkdown(result: ResearchResult) {
    const lines = [
        `# VentureVibe Research Report`,
        ``,
        `## Executive Summary`,
        ``,
        result.executive_summary,
        ``,
        `**Feasibility Score:** ${result.feasibility_score}/100 | **Confidence:** ${result.confidence_level} | **Investment Readiness:** ${result.investment_readiness}`,
        ``,
        `---`,
        ``,
        `## Market Analysis`,
        ``,
        result.market_analysis,
        ``,
        `### Market Sizing`,
        `- TAM: $${result.market_sizing.tam_usd_billion}B`,
        `- SAM: $${result.market_sizing.sam_usd_billion}B`,
        `- SOM: $${result.market_sizing.som_usd_million}M`,
        ...(result.market_sizing.growth_rate_pct != null
            ? [`- Growth Rate: ${result.market_sizing.growth_rate_pct}% CAGR`]
            : []),
        ``,
        `---`,
        ``,
        `## Competitive Analysis`,
        ``,
        `**Competitive Moat:** ${result.competitive_analysis.competitive_moat}`,
        `**Differentiation Score:** ${result.competitive_analysis.differentiation_score}/10`,
        ``,
        `### Direct Competitors`,
        ...result.competitive_analysis.direct_competitors.map(c => `- **${c.name}**: ${c.positioning}`),
        ``,
        `### Indirect Competitors`,
        ...result.competitive_analysis.indirect_competitors.map(c => `- **${c.name}**: ${c.positioning}`),
        ``,
        `---`,
        ``,
        `## SWOT Analysis`,
        ``,
        `**Strengths**`,
        ...result.swot_analysis.strengths.map(s => `- ${s}`),
        ``,
        `**Weaknesses**`,
        ...result.swot_analysis.weaknesses.map(s => `- ${s}`),
        ``,
        `**Opportunities**`,
        ...result.swot_analysis.opportunities.map(s => `- ${s}`),
        ``,
        `**Threats**`,
        ...result.swot_analysis.threats.map(s => `- ${s}`),
        ``,
        `---`,
        ``,
        `## Risk Factors`,
        ``,
        ...result.risk_factors.map(r => `- **[${r.severity.toUpperCase()}] ${r.category}:** ${r.description}\n  *Mitigation:* ${r.mitigation}`),
        ``,
        `---`,
        ``,
        `## Go-to-Market Strategy`,
        ``,
        `- **Primary Channel:** ${result.gtm_strategy.primary_channel}`,
        `- **Secondary Channels:** ${result.gtm_strategy.secondary_channels.join(', ')}`,
        `- **Pricing:** ${result.gtm_strategy.pricing_model}`,
        `- **ICP:** ${result.gtm_strategy.target_icp}`,
        `- **Time to Revenue:** ${result.gtm_strategy.time_to_first_revenue_months} months`,
        ``,
        `---`,
        ``,
        `## Strategic Advice`,
        ``,
        result.strategic_advice,
        ``,
        `## Key Assumptions`,
        ``,
        ...result.key_assumptions.map(a => `- ${a}`),
        ``,
        `## Recommended Next Steps`,
        ``,
        ...result.recommended_next_steps.map((s, i) => `${i + 1}. ${s}`),
    ].join('\n');

    const blob = new Blob([lines], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research-${result.id}.md`;
    a.click();
    URL.revokeObjectURL(url);
}

const markdownComponents = {
    h1: ({ node, ...props }: any) => <h1 className="text-2xl font-bold mb-4" {...props} />,
    h2: ({ node, ...props }: any) => <h2 className="text-xl font-semibold mb-3" {...props} />,
    h3: ({ node, ...props }: any) => <h3 className="text-lg font-semibold mb-2" {...props} />,
    p: ({ node, ...props }: any) => <p className="mb-4 leading-relaxed text-muted-foreground text-justify" {...props} />,
    ul: ({ node, ...props }: any) => <ul className="list-disc pl-6 mb-4 space-y-2" {...props} />,
    ol: ({ node, ...props }: any) => <ol className="list-decimal pl-6 mb-4 space-y-2" {...props} />,
    li: ({ node, ...props }: any) => <li className="text-muted-foreground" {...props} />,
    strong: ({ node, ...props }: any) => <strong className="font-semibold" {...props} />,
};

export const ResearchResultDisplay: React.FC<ResearchResultProps> = ({ result }) => {
    const [checkedSteps, setCheckedSteps] = React.useState<Set<number>>(new Set());

    const toggleStep = (i: number) => {
        setCheckedSteps(prev => {
            const next = new Set(prev);
            next.has(i) ? next.delete(i) : next.add(i);
            return next;
        });
    };

    return (
        <div className="space-y-4 animate-in fade-in duration-700">
            <SummaryStrip result={result} />

            <div className="flex justify-end gap-2">
                <Button variant="outline" size="sm" onClick={() => downloadJSON(result)}>
                    Export JSON
                </Button>
                <Button variant="outline" size="sm" onClick={() => downloadMarkdown(result)}>
                    Export Markdown
                </Button>
            </div>

            <Tabs defaultValue="overview" className="w-full">
                <TabsList className="flex-wrap h-auto gap-1">
                    <TabsTrigger value="overview">Overview</TabsTrigger>
                    <TabsTrigger value="market">Market</TabsTrigger>
                    <TabsTrigger value="competition">Competition</TabsTrigger>
                    <TabsTrigger value="swot-risk">SWOT & Risk</TabsTrigger>
                    <TabsTrigger value="gtm">GTM</TabsTrigger>
                    <TabsTrigger value="ai-log">AI Log</TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-4 mt-4">
                    <Card>
                        <CardHeader><CardTitle>Market Analysis</CardTitle></CardHeader>
                        <CardContent>
                            <div className="prose prose-sm max-w-none dark:prose-invert">
                                <ReactMarkdown components={markdownComponents}>{result.market_analysis}</ReactMarkdown>
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="border-green-100 dark:border-green-900 bg-green-50/50 dark:bg-green-900/10">
                        <CardHeader>
                            <CardTitle className="text-green-700 dark:text-green-300">Strategic Advice</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="prose prose-sm max-w-none dark:prose-invert">
                                <ReactMarkdown components={markdownComponents}>{result.strategic_advice}</ReactMarkdown>
                            </div>
                        </CardContent>
                    </Card>

                    <Accordion type="single" collapsible>
                        <AccordionItem value="assumptions">
                            <AccordionTrigger className="text-sm font-semibold">
                                Key Assumptions ({result.key_assumptions.length})
                            </AccordionTrigger>
                            <AccordionContent>
                                <ul className="space-y-2 pt-1">
                                    {result.key_assumptions.map((a, i) => (
                                        <li key={i} className="flex items-start gap-2 text-sm">
                                            <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
                                            {a}
                                        </li>
                                    ))}
                                </ul>
                            </AccordionContent>
                        </AccordionItem>
                    </Accordion>

                    <Card>
                        <CardHeader><CardTitle className="text-sm">Recommended Next Steps</CardTitle></CardHeader>
                        <CardContent>
                            <ol className="space-y-2">
                                {result.recommended_next_steps.map((step, i) => (
                                    <li
                                        key={i}
                                        className="flex items-start gap-3 text-sm cursor-pointer select-none"
                                        onClick={() => toggleStep(i)}
                                    >
                                        <div className={`mt-0.5 w-4 h-4 rounded-full border-2 flex items-center justify-center shrink-0 transition-colors ${
                                            checkedSteps.has(i) ? 'bg-primary border-primary' : 'border-border'
                                        }`}>
                                            {checkedSteps.has(i) && (
                                                <svg className="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                                </svg>
                                            )}
                                        </div>
                                        <span className={checkedSteps.has(i) ? 'line-through text-muted-foreground' : ''}>{step}</span>
                                    </li>
                                ))}
                            </ol>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="market" className="mt-4">
                    <Card>
                        <CardHeader><CardTitle>Market Sizing (TAM / SAM / SOM)</CardTitle></CardHeader>
                        <CardContent><MarketSizingChart marketSizing={result.market_sizing} /></CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="competition" className="mt-4">
                    <Card>
                        <CardHeader><CardTitle>Competitive Landscape</CardTitle></CardHeader>
                        <CardContent><CompetitorCards competitiveAnalysis={result.competitive_analysis} /></CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="swot-risk" className="space-y-4 mt-4">
                    <Card>
                        <CardHeader><CardTitle>SWOT Analysis</CardTitle></CardHeader>
                        <CardContent><SWOTGrid swot={result.swot_analysis} /></CardContent>
                    </Card>
                    <Card>
                        <CardHeader><CardTitle>Risk Factors</CardTitle></CardHeader>
                        <CardContent><RiskList risks={result.risk_factors} /></CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="gtm" className="mt-4">
                    <Card>
                        <CardHeader><CardTitle>Go-to-Market Strategy</CardTitle></CardHeader>
                        <CardContent><GTMPanel gtm={result.gtm_strategy} /></CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="ai-log" className="mt-4">
                    <Card>
                        <CardHeader><CardTitle>Agent Activity Log</CardTitle></CardHeader>
                        <CardContent><AgentTimeline thoughts={result.agent_thoughts} /></CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};
