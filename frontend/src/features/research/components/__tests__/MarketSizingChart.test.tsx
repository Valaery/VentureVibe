// ABOUTME: Unit tests for MarketSizingChart component covering Recharts visualization and market sizing data
// ABOUTME: Tests chart rendering, data display, methodology, and growth rate calculations

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MarketSizingChart } from '../MarketSizingChart';
import { createMockMarketSizing } from '@/test/mockData/researchResultFactory';

// Mock recharts to avoid SVG rendering issues in tests
vi.mock('recharts', () => ({
  BarChart: ({ children }: any) => <div data-testid="bar-chart">{children}</div>,
  Bar: ({ children }: any) => <div data-testid="bar">{children}</div>,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  CartesianGrid: () => <div data-testid="grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  Cell: () => <div data-testid="cell" />,
  ResponsiveContainer: ({ children }: any) => <div data-testid="responsive-container">{children}</div>,
}));

describe('MarketSizingChart', () => {
  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const marketSizing = createMockMarketSizing();
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByTestId('responsive-container')).toBeInTheDocument();
      expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    });

    it('should render chart components', () => {
      const marketSizing = createMockMarketSizing();
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByTestId('x-axis')).toBeInTheDocument();
      expect(screen.getByTestId('y-axis')).toBeInTheDocument();
      expect(screen.getByTestId('grid')).toBeInTheDocument();
    });
  });

  describe('Data Display', () => {
    it('should display TAM value correctly', () => {
      const marketSizing = createMockMarketSizing({ tam_usd_billion: 100 });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText('$100B')).toBeInTheDocument();
      expect(screen.getByText('TAM')).toBeInTheDocument();
    });

    it('should display SAM value correctly', () => {
      const marketSizing = createMockMarketSizing({ sam_usd_billion: 25 });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText('$25B')).toBeInTheDocument();
      expect(screen.getByText('SAM')).toBeInTheDocument();
    });

    it('should display SOM value correctly in millions', () => {
      const marketSizing = createMockMarketSizing({ som_usd_million: 750 });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText('$750M')).toBeInTheDocument();
      expect(screen.getByText('SOM')).toBeInTheDocument();
    });

    it('should display all three market size metrics', () => {
      const marketSizing = createMockMarketSizing({
        tam_usd_billion: 50,
        sam_usd_billion: 10,
        som_usd_million: 500,
      });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText('$50B')).toBeInTheDocument();
      expect(screen.getByText('$10B')).toBeInTheDocument();
      expect(screen.getByText('$500M')).toBeInTheDocument();
    });
  });

  describe('Growth Rate Display', () => {
    it('should display growth rate when provided', () => {
      const marketSizing = createMockMarketSizing({ growth_rate_pct: 20 });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText(/20% CAGR/i)).toBeInTheDocument();
      expect(screen.getByText(/Market growing at/i)).toBeInTheDocument();
    });

    it('should not display growth rate when null', () => {
      const marketSizing = createMockMarketSizing({ growth_rate_pct: null });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.queryByText(/CAGR/i)).not.toBeInTheDocument();
    });

    it('should handle zero growth rate', () => {
      const marketSizing = createMockMarketSizing({ growth_rate_pct: 0 });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText(/0% CAGR/i)).toBeInTheDocument();
    });
  });

  describe('Methodology Display', () => {
    it('should display top-down methodology', () => {
      const marketSizing = createMockMarketSizing({
        sizing_methodology: 'top_down',
        tam_source_basis: 'Industry reports',
      });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText(/top-down/i)).toBeInTheDocument();
      expect(screen.getByText(/Industry reports/i)).toBeInTheDocument();
    });

    it('should display bottom-up methodology', () => {
      const marketSizing = createMockMarketSizing({
        sizing_methodology: 'bottom_up',
        tam_source_basis: 'Customer analysis',
      });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText(/bottom-up/i)).toBeInTheDocument();
      expect(screen.getByText(/Customer analysis/i)).toBeInTheDocument();
    });

    it('should display hybrid methodology', () => {
      const marketSizing = createMockMarketSizing({
        sizing_methodology: 'hybrid',
        tam_source_basis: 'Combined approach',
      });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText(/hybrid/i)).toBeInTheDocument();
      expect(screen.getByText(/Combined approach/i)).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle zero values', () => {
      const marketSizing = createMockMarketSizing({
        tam_usd_billion: 0,
        sam_usd_billion: 0,
        som_usd_million: 0,
      });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getAllByText('$0B')).toHaveLength(2); // TAM and SAM
      expect(screen.getByText('$0M')).toBeInTheDocument();
    });

    it('should handle very large TAM values', () => {
      const marketSizing = createMockMarketSizing({ tam_usd_billion: 1000 });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText('$1000B')).toBeInTheDocument();
    });

    it('should handle decimal values', () => {
      const marketSizing = createMockMarketSizing({
        tam_usd_billion: 25.5,
        sam_usd_billion: 5.2,
        som_usd_million: 125.8,
      });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText('$25.5B')).toBeInTheDocument();
      expect(screen.getByText('$5.2B')).toBeInTheDocument();
      expect(screen.getByText('$125.8M')).toBeInTheDocument();
    });

    it('should handle negative growth rate', () => {
      const marketSizing = createMockMarketSizing({ growth_rate_pct: -5 });
      render(<MarketSizingChart marketSizing={marketSizing} />);

      expect(screen.getByText(/-5% CAGR/i)).toBeInTheDocument();
    });
  });
});
