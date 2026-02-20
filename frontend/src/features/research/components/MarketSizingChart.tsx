import React from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid,
    Tooltip, Cell, ResponsiveContainer,
} from 'recharts';
import type { MarketSizing } from '../data/services/researchService';

const COLORS: Record<string, string> = {
    TAM: '#6366f1',
    SAM: '#22c55e',
    SOM: '#f59e0b',
};

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload?.length) {
        const isSOM = label === 'SOM';
        return (
            <div className="bg-white border border-border rounded-lg p-3 shadow-md text-sm">
                <p className="font-semibold mb-1">{label}</p>
                <p className="text-muted-foreground">
                    {isSOM
                        ? `$${(payload[0].value * 1000).toFixed(0)}M`
                        : `$${payload[0].value}B`}
                </p>
            </div>
        );
    }
    return null;
};

interface MarketSizingChartProps {
    marketSizing: MarketSizing;
}

export const MarketSizingChart: React.FC<MarketSizingChartProps> = ({ marketSizing }) => {
    const data = [
        { name: 'TAM', value: marketSizing.tam_usd_billion },
        { name: 'SAM', value: marketSizing.sam_usd_billion },
        { name: 'SOM', value: marketSizing.som_usd_million / 1000 },
    ];

    return (
        <div className="space-y-4">
            <ResponsiveContainer width="100%" height={180}>
                <BarChart layout="vertical" data={data} margin={{ top: 0, right: 60, left: 8, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <YAxis type="category" dataKey="name" width={40} tick={{ fontSize: 13, fontWeight: 600 }} />
                    <XAxis type="number" tickFormatter={(v) => `$${v}B`} tick={{ fontSize: 11 }} domain={[0, 'dataMax + 5']} />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                        {data.map((entry) => (
                            <Cell key={entry.name} fill={COLORS[entry.name]} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            <div className="grid grid-cols-3 gap-3 text-sm">
                <div className="text-center p-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/20">
                    <p className="font-bold text-indigo-700 dark:text-indigo-300">${marketSizing.tam_usd_billion}B</p>
                    <p className="text-xs text-muted-foreground">TAM</p>
                </div>
                <div className="text-center p-2 rounded-lg bg-green-50 dark:bg-green-900/20">
                    <p className="font-bold text-green-700 dark:text-green-300">${marketSizing.sam_usd_billion}B</p>
                    <p className="text-xs text-muted-foreground">SAM</p>
                </div>
                <div className="text-center p-2 rounded-lg bg-amber-50 dark:bg-amber-900/20">
                    <p className="font-bold text-amber-700 dark:text-amber-300">${marketSizing.som_usd_million}M</p>
                    <p className="text-xs text-muted-foreground">SOM</p>
                </div>
            </div>

            {marketSizing.growth_rate_pct != null && (
                <p className="text-sm text-muted-foreground">
                    Market growing at <span className="font-semibold text-green-600">{marketSizing.growth_rate_pct}% CAGR</span>
                </p>
            )}

            <p className="text-xs text-muted-foreground italic">
                Methodology: {marketSizing.sizing_methodology.replace('_', '-')} | {marketSizing.tam_source_basis}
            </p>
        </div>
    );
};
