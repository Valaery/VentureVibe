import React from 'react';

interface LogoProps {
    size?: 'sm' | 'md' | 'lg';
    animated?: boolean;
    className?: string;
}

export const VentureVibeLogo: React.FC<LogoProps> = ({
    size = 'md',
    animated = false,
    className = ''
}) => {
    const sizeClasses = {
        sm: 'w-8 h-8',
        md: 'w-12 h-12',
        lg: 'w-16 h-16'
    };

    return (
        <div className={`${sizeClasses[size]} ${className}`}>
            <svg viewBox="0 0 100 100" className={animated ? 'animate-pulse' : ''}>
                <defs>
                    <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="hsl(217.2, 91.2%, 59.8%)" />
                        <stop offset="50%" stopColor="hsl(243.4, 75.4%, 58.6%)" />
                        <stop offset="100%" stopColor="hsl(258.3, 89.5%, 66.3%)" />
                    </linearGradient>
                </defs>
                {/* Lightbulb base morphing into rocket */}
                <path
                    d="M50,10 L60,40 L70,70 L60,90 L40,90 L30,70 L40,40 Z"
                    fill="url(#logoGradient)"
                    className="transition-all duration-300"
                />
                {/* Add more sophisticated SVG path for lightbulb-to-rocket concept */}
            </svg>
        </div>
    );
};
