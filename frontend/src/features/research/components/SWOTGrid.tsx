import React from 'react';
import type { SWOTAnalysis } from '../data/services/researchService';

interface SWOTGridProps {
    swot: SWOTAnalysis;
}

const quadrants = [
    { key: 'strengths' as const, label: 'Strengths', bg: 'bg-green-50 dark:bg-green-900/20', border: 'border-green-200 dark:border-green-800', text: 'text-green-700 dark:text-green-300', dot: 'bg-green-500' },
    { key: 'weaknesses' as const, label: 'Weaknesses', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800', text: 'text-red-700 dark:text-red-300', dot: 'bg-red-500' },
    { key: 'opportunities' as const, label: 'Opportunities', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800', text: 'text-blue-700 dark:text-blue-300', dot: 'bg-blue-500' },
    { key: 'threats' as const, label: 'Threats', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800', text: 'text-amber-700 dark:text-amber-300', dot: 'bg-amber-500' },
];

export const SWOTGrid: React.FC<SWOTGridProps> = ({ swot }) => (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {quadrants.map(({ key, label, bg, border, text, dot }) => (
            <div key={key} className={`rounded-lg border p-4 ${bg} ${border}`}>
                <h4 className={`font-semibold text-sm mb-3 ${text}`}>{label}</h4>
                <ul className="space-y-2">
                    {swot[key].map((item, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                            <span className={`mt-1.5 w-1.5 h-1.5 rounded-full shrink-0 ${dot}`} />
                            <span>{item}</span>
                        </li>
                    ))}
                </ul>
            </div>
        ))}
    </div>
);
