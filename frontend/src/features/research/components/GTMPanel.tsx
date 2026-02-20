import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import type { GTMStrategy } from '../data/services/researchService';

interface GTMPanelProps {
    gtm: GTMStrategy;
}

export const GTMPanel: React.FC<GTMPanelProps> = ({ gtm }) => (
    <div className="space-y-4">
        <Card className="border-primary/20 bg-primary/5">
            <CardContent className="pt-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-primary mb-1">Ideal Customer Profile (ICP)</p>
                <p className="text-sm">{gtm.target_icp}</p>
            </CardContent>
        </Card>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div className="bg-card border rounded-lg p-3 text-center">
                <p className="text-lg font-bold text-primary">{gtm.time_to_first_revenue_months}mo</p>
                <p className="text-xs text-muted-foreground">Time to Revenue</p>
            </div>
            {gtm.estimated_cac_usd != null && (
                <div className="bg-card border rounded-lg p-3 text-center">
                    <p className="text-lg font-bold text-primary">${gtm.estimated_cac_usd}</p>
                    <p className="text-xs text-muted-foreground">Est. CAC</p>
                </div>
            )}
            <div className="bg-card border rounded-lg p-3 text-center">
                <p className="text-sm font-semibold text-primary">{gtm.pricing_model}</p>
                <p className="text-xs text-muted-foreground">Pricing Model</p>
            </div>
        </div>

        <Separator />

        <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">Acquisition Channels</p>
            <div className="flex flex-wrap gap-2">
                <Badge className="bg-primary text-primary-foreground">{gtm.primary_channel}</Badge>
                {gtm.secondary_channels.map((ch, i) => (
                    <Badge key={i} variant="outline">{ch}</Badge>
                ))}
            </div>
        </div>
    </div>
);
