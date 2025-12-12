import React from 'react';

interface ProgressCircleProps {
    value: number;
    size?: number;
    strokeWidth?: number;
    className?: string;
}

export const ProgressCircle: React.FC<ProgressCircleProps> = ({
    value,
    size = 120,
    strokeWidth = 8,
    className = ''
}) => {
    const radius = (size - strokeWidth) / 2;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (value / 100) * circumference;

    const getColor = (score: number) => {
        if (score >= 80) return 'hsl(142.1, 76.2%, 36.3%)'; // green
        if (score >= 50) return 'hsl(47.9, 95.8%, 53.1%)'; // yellow
        return 'hsl(0, 84.2%, 60.2%)'; // red
    };

    return (
        <div className={`relative ${className}`}>
            <svg width={size} height={size} className="transform -rotate-90">
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="hsl(var(--muted))"
                    strokeWidth={strokeWidth}
                    fill="none"
                />
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke={getColor(value)}
                    strokeWidth={strokeWidth}
                    fill="none"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold font-display">{value}</span>
                <span className="text-xs text-muted-foreground">/ 100</span>
            </div>
        </div>
    );
};
