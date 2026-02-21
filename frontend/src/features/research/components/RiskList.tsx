import React from 'react';
import { Badge } from '@/components/ui/badge';
import type { RiskFactor, RiskSeverity } from '../data/services/researchService';

const SEVERITY_CONFIG: Record<RiskSeverity, { border: string; badge: string; label: string }> = {
    critical: { border: 'border-l-red-600', badge: 'bg-red-100 text-red-700 border-red-300', label: 'Critical' },
    high: { border: 'border-l-orange-500', badge: 'bg-orange-100 text-orange-700 border-orange-300', label: 'High' },
    medium: { border: 'border-l-yellow-500', badge: 'bg-yellow-100 text-yellow-700 border-yellow-300', label: 'Medium' },
    low: { border: 'border-l-green-500', badge: 'bg-green-100 text-green-700 border-green-300', label: 'Low' },
};

const SEVERITY_ORDER: Record<RiskSeverity, number> = { critical: 0, high: 1, medium: 2, low: 3 };

interface RiskListProps {
    risks: RiskFactor[];
}

export const RiskList: React.FC<RiskListProps> = ({ risks }) => {
    const sorted = [...risks].sort((a, b) => SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity]);

    return (
        <div className="space-y-3">
            {sorted.map((risk, i) => {
                const { border, badge, label } = SEVERITY_CONFIG[risk.severity];
                return (
                    <div key={i} className={`border border-l-4 ${border} pl-4 py-3 rounded-r-lg bg-card`}>
                        <div className="flex items-start justify-between gap-3 mb-1">
                            <p className="text-sm font-medium text-justify">{risk.description}</p>
                            <div className="flex items-center gap-1.5 shrink-0">
                                <Badge variant="outline" className={`text-xs ${badge}`}>{label}</Badge>
                                <Badge variant="secondary" className="text-xs capitalize">{risk.category}</Badge>
                            </div>
                        </div>
                        <p className="text-xs text-muted-foreground text-justify">
                            <span className="font-medium">Mitigation:</span> {risk.mitigation}
                        </p>
                    </div>
                );
            })}
        </div>
    );
};
