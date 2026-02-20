// ABOUTME: Unit tests for GTMPanel component covering go-to-market strategy display
// ABOUTME: Tests ICP card, metric tiles (CAC, time to revenue, pricing), and channel badges

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GTMPanel } from '../GTMPanel';
import { createMockGTMStrategy } from '@/test/mockData/researchResultFactory';

describe('GTMPanel', () => {
  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const gtm = createMockGTMStrategy();
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText(/Ideal Customer Profile/i)).toBeInTheDocument();
    });

    it('should display ICP (Ideal Customer Profile)', () => {
      const icp = 'B2B SaaS companies with 100-500 employees in North America';
      const gtm = createMockGTMStrategy({ target_icp: icp });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText(icp)).toBeInTheDocument();
    });
  });

  describe('Metric Tiles', () => {
    it('should display time to first revenue in months', () => {
      const gtm = createMockGTMStrategy({ time_to_first_revenue_months: 12 });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('12mo')).toBeInTheDocument();
      expect(screen.getByText(/Time to Revenue/i)).toBeInTheDocument();
    });

    it('should display estimated CAC when provided', () => {
      const gtm = createMockGTMStrategy({ estimated_cac_usd: 350 });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('$350')).toBeInTheDocument();
      expect(screen.getByText(/Est. CAC/i)).toBeInTheDocument();
    });

    it('should not display CAC when null', () => {
      const gtm = createMockGTMStrategy({ estimated_cac_usd: null });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.queryByText(/Est. CAC/i)).not.toBeInTheDocument();
    });

    it('should display pricing model', () => {
      const pricingModel = 'Usage-based with minimum commitment';
      const gtm = createMockGTMStrategy({ pricing_model: pricingModel });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText(pricingModel)).toBeInTheDocument();
      expect(screen.getByText(/Pricing Model/i)).toBeInTheDocument();
    });

    it('should handle zero CAC', () => {
      const gtm = createMockGTMStrategy({ estimated_cac_usd: 0 });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('$0')).toBeInTheDocument();
    });

    it('should handle large CAC values', () => {
      const gtm = createMockGTMStrategy({ estimated_cac_usd: 5000 });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('$5000')).toBeInTheDocument();
    });

    it('should handle zero time to revenue', () => {
      const gtm = createMockGTMStrategy({ time_to_first_revenue_months: 0 });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('0mo')).toBeInTheDocument();
    });
  });

  describe('Acquisition Channels', () => {
    it('should display primary channel with primary styling', () => {
      const gtm = createMockGTMStrategy({ primary_channel: 'Direct Sales' });
      render(<GTMPanel gtm={gtm} />);

      const primaryChannel = screen.getByText('Direct Sales');
      expect(primaryChannel).toBeInTheDocument();
      expect(primaryChannel).toHaveClass('bg-primary', 'text-primary-foreground');
    });

    it('should display secondary channels with outline styling', () => {
      const secondaryChannels = ['SEO', 'Referral Program', 'Community Building'];
      const gtm = createMockGTMStrategy({ secondary_channels: secondaryChannels });
      render(<GTMPanel gtm={gtm} />);

      secondaryChannels.forEach(channel => {
        const badge = screen.getByText(channel);
        expect(badge).toBeInTheDocument();
      });
    });

    it('should display Acquisition Channels label', () => {
      const gtm = createMockGTMStrategy();
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText(/Acquisition Channels/i)).toBeInTheDocument();
    });

    it('should handle empty secondary channels', () => {
      const gtm = createMockGTMStrategy({ secondary_channels: [] });
      render(<GTMPanel gtm={gtm} />);

      // Should still show primary channel
      expect(screen.getByText(/Content Marketing/i)).toBeInTheDocument();
    });

    it('should handle multiple secondary channels', () => {
      const secondaryChannels = ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4'];
      const gtm = createMockGTMStrategy({ secondary_channels: secondaryChannels });
      render(<GTMPanel gtm={gtm} />);

      secondaryChannels.forEach(channel => {
        expect(screen.getByText(channel)).toBeInTheDocument();
      });
    });

    it('should handle single secondary channel', () => {
      const gtm = createMockGTMStrategy({ secondary_channels: ['Partnerships'] });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('Partnerships')).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle very long ICP description', () => {
      const longICP = 'A'.repeat(500);
      const gtm = createMockGTMStrategy({ target_icp: longICP });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText(longICP)).toBeInTheDocument();
    });

    it('should handle very long pricing model description', () => {
      const longPricing = 'B'.repeat(200);
      const gtm = createMockGTMStrategy({ pricing_model: longPricing });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText(longPricing)).toBeInTheDocument();
    });

    it('should handle very long channel names', () => {
      const longChannel = 'C'.repeat(100);
      const gtm = createMockGTMStrategy({ primary_channel: longChannel });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText(longChannel)).toBeInTheDocument();
    });

    it('should handle large time to revenue values', () => {
      const gtm = createMockGTMStrategy({ time_to_first_revenue_months: 36 });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('36mo')).toBeInTheDocument();
    });

    it('should render all sections together', () => {
      const gtm = createMockGTMStrategy({
        target_icp: 'Test ICP',
        time_to_first_revenue_months: 6,
        estimated_cac_usd: 200,
        pricing_model: 'Test Pricing',
        primary_channel: 'Test Primary',
        secondary_channels: ['Test Secondary 1', 'Test Secondary 2'],
      });
      render(<GTMPanel gtm={gtm} />);

      expect(screen.getByText('Test ICP')).toBeInTheDocument();
      expect(screen.getByText('6mo')).toBeInTheDocument();
      expect(screen.getByText('$200')).toBeInTheDocument();
      expect(screen.getByText('Test Pricing')).toBeInTheDocument();
      expect(screen.getByText('Test Primary')).toBeInTheDocument();
      expect(screen.getByText('Test Secondary 1')).toBeInTheDocument();
      expect(screen.getByText('Test Secondary 2')).toBeInTheDocument();
    });
  });
});
