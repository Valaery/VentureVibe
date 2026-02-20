import React from 'react';
import type { AgentThought } from '../data/services/researchService';

const AGENT_COLORS: Record<string, string> = {
    'Product Strategist': 'bg-violet-500',
    'Research Analyst': 'bg-blue-500',
    'Market Sizing Analyst': 'bg-green-500',
    'Competitive Intelligence Analyst': 'bg-red-500',
    'SWOT & Risk Analyst': 'bg-amber-500',
    'GTM Strategist': 'bg-indigo-500',
};

function getColor(agentName: string): string {
    return AGENT_COLORS[agentName] ?? 'bg-gray-500';
}

interface AgentTimelineProps {
    thoughts: AgentThought[];
}

export const AgentTimeline: React.FC<AgentTimelineProps> = ({ thoughts }) => {
    if (!thoughts?.length) {
        return <p className="text-sm text-muted-foreground">No agent activity recorded.</p>;
    }

    return (
        <div className="space-y-3">
            {thoughts.map((thought, i) => (
                <div
                    key={i}
                    className="flex gap-3 animate-in fade-in slide-in-from-left-4 duration-500"
                    style={{ animationDelay: `${i * 150}ms`, animationFillMode: 'both' }}
                >
                    <div className="flex flex-col items-center">
                        <div className={`w-2.5 h-2.5 rounded-full mt-1.5 shrink-0 ${getColor(thought.agent_name)}`} />
                        {i < thoughts.length - 1 && <div className="w-0.5 bg-border flex-1 mt-1" />}
                    </div>
                    <div className="pb-3 min-w-0">
                        <p className="text-xs font-semibold text-muted-foreground">{thought.agent_name}</p>
                        <p className="text-sm mt-0.5">{thought.thought}</p>
                    </div>
                </div>
            ))}
        </div>
    );
};
