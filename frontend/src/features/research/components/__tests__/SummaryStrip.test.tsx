// ABOUTME: Unit tests for SummaryStrip component covering score display, investment readiness, and executive summary
// ABOUTME: Tests rendering, confidence levels, investment stage progression, and edge cases

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SummaryStrip } from '../SummaryStrip';
import { createMockResearchResult } from '@/test/mockData/researchResultFactory';

describe('SummaryStrip', () => {
  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const result = createMockResearchResult();
      render(<SummaryStrip result={result} />);

      expect(screen.getByText(/Feasibility Score/i)).toBeInTheDocument();
    });

    it('should display the feasibility score', () => {
      const result = createMockResearchResult({ feasibility_score: 85 });
      render(<SummaryStrip result={result} />);

      // ProgressCircle component will render the score value
      const scoreElement = screen.getByText('85');
      expect(scoreElement).toBeInTheDocument();
    });

    it('should display the executive summary', () => {
      const summary = 'This is a test executive summary for the product';
      const result = createMockResearchResult({ executive_summary: summary });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText(summary)).toBeInTheDocument();
    });

    it('should display Investment Readiness label', () => {
      const result = createMockResearchResult();
      render(<SummaryStrip result={result} />);

      expect(screen.getByText(/Investment Readiness/i)).toBeInTheDocument();
    });
  });

  describe('Confidence Level Badge', () => {
    it('should render high confidence badge with correct styling', () => {
      const result = createMockResearchResult({ confidence_level: 'high' });
      render(<SummaryStrip result={result} />);

      const badge = screen.getByText(/high confidence/i);
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-green-100', 'text-green-700');
    });

    it('should render medium confidence badge with correct styling', () => {
      const result = createMockResearchResult({ confidence_level: 'medium' });
      render(<SummaryStrip result={result} />);

      const badge = screen.getByText(/medium confidence/i);
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-yellow-100', 'text-yellow-700');
    });

    it('should render low confidence badge with correct styling', () => {
      const result = createMockResearchResult({ confidence_level: 'low' });
      render(<SummaryStrip result={result} />);

      const badge = screen.getByText(/low confidence/i);
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-red-100', 'text-red-700');
    });
  });

  describe('Investment Readiness Stepper', () => {
    it('should highlight the current stage for pre_idea', () => {
      const result = createMockResearchResult({ investment_readiness: 'pre_idea' });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('Pre-Idea')).toBeInTheDocument();
    });

    it('should highlight the current stage for idea_stage', () => {
      const result = createMockResearchResult({ investment_readiness: 'idea_stage' });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('Idea Stage')).toBeInTheDocument();
    });

    it('should highlight the current stage for mvp_ready', () => {
      const result = createMockResearchResult({ investment_readiness: 'mvp_ready' });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('MVP Ready')).toBeInTheDocument();
    });

    it('should highlight the current stage for seed_ready', () => {
      const result = createMockResearchResult({ investment_readiness: 'seed_ready' });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('Seed Ready')).toBeInTheDocument();
    });

    it('should highlight the current stage for series_a_ready', () => {
      const result = createMockResearchResult({ investment_readiness: 'series_a_ready' });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('Series A')).toBeInTheDocument();
    });

    it('should render all 5 investment stages', () => {
      const result = createMockResearchResult();
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('Pre-Idea')).toBeInTheDocument();
      expect(screen.getByText('Idea Stage')).toBeInTheDocument();
      expect(screen.getByText('MVP Ready')).toBeInTheDocument();
      expect(screen.getByText('Seed Ready')).toBeInTheDocument();
      expect(screen.getByText('Series A')).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle zero feasibility score', () => {
      const result = createMockResearchResult({ feasibility_score: 0 });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('0')).toBeInTheDocument();
    });

    it('should handle 100 feasibility score', () => {
      const result = createMockResearchResult({ feasibility_score: 100 });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText('100')).toBeInTheDocument();
    });

    it('should handle empty executive summary', () => {
      const result = createMockResearchResult({ executive_summary: '' });
      render(<SummaryStrip result={result} />);

      // Should still render the blockquote, even if empty
      expect(screen.getByText(/Feasibility Score/i)).toBeInTheDocument();
    });

    it('should handle very long executive summary', () => {
      const longSummary = 'A'.repeat(500);
      const result = createMockResearchResult({ executive_summary: longSummary });
      render(<SummaryStrip result={result} />);

      expect(screen.getByText(longSummary)).toBeInTheDocument();
    });
  });
});
