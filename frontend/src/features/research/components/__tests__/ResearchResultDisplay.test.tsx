// ABOUTME: Unit tests for ResearchResultDisplay component covering tab layout and export functionality
// ABOUTME: Tests 6-tab navigation, component integration, export buttons, and interactive checklist

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ResearchResultDisplay } from '../ResearchResultDisplay';
import { createMockResearchResult } from '@/test/mockData/researchResultFactory';

// Mock recharts
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

// Mock URL and Blob APIs
global.URL.createObjectURL = vi.fn(() => 'mock-url');
global.URL.revokeObjectURL = vi.fn();

const MockBlob = vi.fn(function(this: any, content: any, options: any) {
  this.content = content;
  this.options = options;
}) as any;

global.Blob = MockBlob;

describe('ResearchResultDisplay', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText(/Feasibility Score/i)).toBeInTheDocument();
    });

    it('should render SummaryStrip component', () => {
      const result = createMockResearchResult({
        executive_summary: 'Test summary for display',
      });
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText('Test summary for display')).toBeInTheDocument();
    });

    it('should render export buttons', () => {
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText('Export JSON')).toBeInTheDocument();
      expect(screen.getByText('Export Markdown')).toBeInTheDocument();
    });
  });

  describe('Tab Navigation', () => {
    it('should render all 6 tabs', () => {
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText('Overview')).toBeInTheDocument();
      expect(screen.getByText('Market')).toBeInTheDocument();
      expect(screen.getByText('Competition')).toBeInTheDocument();
      expect(screen.getByText('SWOT & Risk')).toBeInTheDocument();
      expect(screen.getByText('GTM')).toBeInTheDocument();
      expect(screen.getByText('AI Log')).toBeInTheDocument();
    });

    it('should display Overview tab by default', () => {
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByRole('tab', { name: /overview/i })).toHaveAttribute('data-state', 'active');
    });

    it('should switch to Market tab when clicked', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const marketTab = screen.getByRole('tab', { name: /market/i });
      await user.click(marketTab);

      expect(marketTab).toHaveAttribute('data-state', 'active');
    });

    it('should switch to Competition tab when clicked', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const competitionTab = screen.getByRole('tab', { name: /competition/i });
      await user.click(competitionTab);

      expect(competitionTab).toHaveAttribute('data-state', 'active');
    });

    it('should switch to SWOT & Risk tab when clicked', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const swotTab = screen.getByRole('tab', { name: /swot & risk/i });
      await user.click(swotTab);

      expect(swotTab).toHaveAttribute('data-state', 'active');
    });

    it('should switch to GTM tab when clicked', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const gtmTab = screen.getByRole('tab', { name: /gtm/i });
      await user.click(gtmTab);

      expect(gtmTab).toHaveAttribute('data-state', 'active');
    });

    it('should switch to AI Log tab when clicked', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const aiLogTab = screen.getByRole('tab', { name: /ai log/i });
      await user.click(aiLogTab);

      expect(aiLogTab).toHaveAttribute('data-state', 'active');
    });
  });

  describe('Overview Tab', () => {
    it('should display market analysis in Overview tab', () => {
      const result = createMockResearchResult({
        market_analysis: '## Test Market Analysis Content',
      });
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText(/Test Market Analysis Content/i)).toBeInTheDocument();
    });

    it('should display strategic advice in Overview tab', () => {
      const result = createMockResearchResult({
        strategic_advice: '## Test Strategic Advice Content',
      });
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText(/Test Strategic Advice Content/i)).toBeInTheDocument();
    });

    it('should display Key Assumptions accordion', () => {
      const result = createMockResearchResult({
        key_assumptions: ['Assumption 1', 'Assumption 2'],
      });
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText(/Key Assumptions \(2\)/i)).toBeInTheDocument();
    });

    it('should display Recommended Next Steps', () => {
      const result = createMockResearchResult({
        recommended_next_steps: ['Step 1', 'Step 2', 'Step 3'],
      });
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText('Step 1')).toBeInTheDocument();
      expect(screen.getByText('Step 2')).toBeInTheDocument();
      expect(screen.getByText('Step 3')).toBeInTheDocument();
    });

    it('should toggle next step checkbox on click', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult({
        recommended_next_steps: ['Test step'],
      });
      render(<ResearchResultDisplay result={result} />);

      const step = screen.getByText('Test step');
      await user.click(step);

      // After clicking, should have strikethrough class
      expect(step).toHaveClass('line-through');
    });
  });

  describe('Market Tab', () => {
    it('should display MarketSizingChart in Market tab', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const marketTab = screen.getByRole('tab', { name: /market/i });
      await user.click(marketTab);

      expect(screen.getByTestId('responsive-container')).toBeInTheDocument();
      expect(screen.getByText(/Market Sizing/i)).toBeInTheDocument();
    });
  });

  describe('Competition Tab', () => {
    it('should display CompetitorCards in Competition tab', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const competitionTab = screen.getByRole('tab', { name: /competition/i });
      await user.click(competitionTab);

      expect(screen.getByText(/Competitive Landscape/i)).toBeInTheDocument();
      expect(screen.getByText(/Your Competitive Moat/i)).toBeInTheDocument();
    });
  });

  describe('SWOT & Risk Tab', () => {
    it('should display SWOTGrid in SWOT & Risk tab', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const swotTab = screen.getByRole('tab', { name: /swot & risk/i });
      await user.click(swotTab);

      expect(screen.getByText('Strengths')).toBeInTheDocument();
      expect(screen.getByText('Weaknesses')).toBeInTheDocument();
      expect(screen.getByText('Opportunities')).toBeInTheDocument();
      expect(screen.getByText('Threats')).toBeInTheDocument();
    });

    it('should display RiskList in SWOT & Risk tab', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const swotTab = screen.getByRole('tab', { name: /swot & risk/i });
      await user.click(swotTab);

      expect(screen.getByText(/Risk Factors/i)).toBeInTheDocument();
    });
  });

  describe('GTM Tab', () => {
    it('should display GTMPanel in GTM tab', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const gtmTab = screen.getByRole('tab', { name: /gtm/i });
      await user.click(gtmTab);

      expect(screen.getByText(/Go-to-Market Strategy/i)).toBeInTheDocument();
      expect(screen.getByText(/Ideal Customer Profile/i)).toBeInTheDocument();
    });
  });

  describe('AI Log Tab', () => {
    it('should display AgentTimeline in AI Log tab', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult();
      render(<ResearchResultDisplay result={result} />);

      const aiLogTab = screen.getByRole('tab', { name: /ai log/i });
      await user.click(aiLogTab);

      expect(screen.getByText(/Agent Activity Log/i)).toBeInTheDocument();
    });
  });

  describe('Export Functionality', () => {
    it('should export JSON when Export JSON button is clicked', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult({ id: 'test-id-123' });

      // Mock document.createElement for anchor only
      const mockAnchor = {
        href: '',
        download: '',
        click: vi.fn(),
      };
      const originalCreateElement = document.createElement.bind(document);
      vi.spyOn(document, 'createElement').mockImplementation((tag: string) => {
        if (tag === 'a') return mockAnchor as any;
        return originalCreateElement(tag);
      });

      render(<ResearchResultDisplay result={result} />);

      const exportButton = screen.getByText('Export JSON');
      await user.click(exportButton);

      expect(global.Blob).toHaveBeenCalledWith(
        [expect.stringContaining('test-id-123')],
        { type: 'application/json' }
      );
      expect(mockAnchor.download).toBe('research-test-id-123.json');
      expect(mockAnchor.click).toHaveBeenCalled();
    });

    it('should export Markdown when Export Markdown button is clicked', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult({ id: 'test-id-456' });

      // Mock document.createElement for anchor only
      const mockAnchor = {
        href: '',
        download: '',
        click: vi.fn(),
      };
      const originalCreateElement = document.createElement.bind(document);
      vi.spyOn(document, 'createElement').mockImplementation((tag: string) => {
        if (tag === 'a') return mockAnchor as any;
        return originalCreateElement(tag);
      });

      render(<ResearchResultDisplay result={result} />);

      const exportButton = screen.getByText('Export Markdown');
      await user.click(exportButton);

      expect(global.Blob).toHaveBeenCalledWith(
        [expect.stringContaining('VentureVibe Research Report')],
        { type: 'text/markdown' }
      );
      expect(mockAnchor.download).toBe('research-test-id-456.md');
      expect(mockAnchor.click).toHaveBeenCalled();
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty agent thoughts', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult({ agent_thoughts: [] });
      render(<ResearchResultDisplay result={result} />);

      const aiLogTab = screen.getByRole('tab', { name: /ai log/i });
      await user.click(aiLogTab);

      expect(screen.getByText(/No agent activity recorded/i)).toBeInTheDocument();
    });

    it('should handle empty key assumptions', () => {
      const result = createMockResearchResult({ key_assumptions: [] });
      render(<ResearchResultDisplay result={result} />);

      expect(screen.getByText(/Key Assumptions \(0\)/i)).toBeInTheDocument();
    });

    it('should handle empty recommended next steps', () => {
      const result = createMockResearchResult({ recommended_next_steps: [] });
      render(<ResearchResultDisplay result={result} />);

      // Should still render the section title
      expect(screen.getByText(/Recommended Next Steps/i)).toBeInTheDocument();
    });

    it('should handle very long markdown content', () => {
      const longContent = '#'.repeat(10000);
      const result = createMockResearchResult({ market_analysis: longContent });
      render(<ResearchResultDisplay result={result} />);

      // Component should render without crashing
      expect(screen.getByText(/Market Analysis/i)).toBeInTheDocument();
    });

    it('should handle multiple checkbox toggles', async () => {
      const user = userEvent.setup();
      const result = createMockResearchResult({
        recommended_next_steps: ['Step 1', 'Step 2', 'Step 3'],
      });
      render(<ResearchResultDisplay result={result} />);

      const step1 = screen.getByText('Step 1');
      const step2 = screen.getByText('Step 2');

      // Toggle step 1
      await user.click(step1);
      expect(step1).toHaveClass('line-through');

      // Toggle step 2
      await user.click(step2);
      expect(step2).toHaveClass('line-through');

      // Untoggle step 1
      await user.click(step1);
      expect(step1).not.toHaveClass('line-through');
      expect(step2).toHaveClass('line-through');
    });
  });
});
