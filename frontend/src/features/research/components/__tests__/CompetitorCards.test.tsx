// ABOUTME: Unit tests for CompetitorCards component covering competitor display, moat callout, and differentiation
// ABOUTME: Tests rendering of direct/indirect competitors, funding info, and competitive positioning

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CompetitorCards } from '../CompetitorCards';
import {
  createMockCompetitiveAnalysis,
  createMockCompetitor,
} from '@/test/mockData/researchResultFactory';

describe('CompetitorCards', () => {
  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis();
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(/Your Competitive Moat/i)).toBeInTheDocument();
    });

    it('should display differentiation score', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        differentiation_score: 8,
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText('8/10')).toBeInTheDocument();
      expect(screen.getByText(/Differentiation Score/i)).toBeInTheDocument();
    });

    it('should display competitive moat', () => {
      const moat = 'Strong network effects and proprietary technology';
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        competitive_moat: moat,
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(moat)).toBeInTheDocument();
    });
  });

  describe('Direct Competitors', () => {
    it('should render direct competitors section', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [
          createMockCompetitor({ name: 'Direct Comp 1' }),
          createMockCompetitor({ name: 'Direct Comp 2' }),
        ],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(/Direct Competitors \(2\)/i)).toBeInTheDocument();
      expect(screen.getByText('Direct Comp 1')).toBeInTheDocument();
      expect(screen.getByText('Direct Comp 2')).toBeInTheDocument();
    });

    it('should display competitor positioning', () => {
      const positioning = 'Enterprise-focused AI platform';
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [
          createMockCompetitor({ positioning }),
        ],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(positioning)).toBeInTheDocument();
    });

    it('should display competitor business model', () => {
      const businessModel = 'Freemium with enterprise upsell';
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [
          createMockCompetitor({ business_model: businessModel }),
        ],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(businessModel)).toBeInTheDocument();
    });

    it('should display competitor primary weakness', () => {
      const weakness = 'Slow innovation cycle';
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [
          createMockCompetitor({ primary_weakness: weakness }),
        ],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(weakness)).toBeInTheDocument();
    });

    it('should display competitor funding when available', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [
          createMockCompetitor({ estimated_funding_usd_million: 150 }),
        ],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText('$150M raised')).toBeInTheDocument();
    });

    it('should not display funding when null', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [
          createMockCompetitor({ estimated_funding_usd_million: null }),
        ],
        indirect_competitors: [],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.queryByText(/raised/i)).not.toBeInTheDocument();
    });

    it('should display Direct badge for direct competitors', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [createMockCompetitor()],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText('Direct')).toBeInTheDocument();
    });
  });

  describe('Indirect Competitors', () => {
    it('should render indirect competitors section', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        indirect_competitors: [
          createMockCompetitor({ name: 'Indirect Comp 1' }),
          createMockCompetitor({ name: 'Indirect Comp 2' }),
        ],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(/Indirect Competitors \(2\)/i)).toBeInTheDocument();
      expect(screen.getByText('Indirect Comp 1')).toBeInTheDocument();
      expect(screen.getByText('Indirect Comp 2')).toBeInTheDocument();
    });

    it('should display Indirect badge for indirect competitors', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        indirect_competitors: [createMockCompetitor()],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText('Indirect')).toBeInTheDocument();
    });

    it('should not render indirect section when empty', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        indirect_competitors: [],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.queryByText(/Indirect Competitors/i)).not.toBeInTheDocument();
    });
  });

  describe('Differentiation Score Visual', () => {
    it('should render 10 bars for differentiation score', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        differentiation_score: 5,
      });
      const { container } = render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      // Find all the score bars
      const scoreBars = container.querySelectorAll('.w-2.h-4.rounded-sm');
      expect(scoreBars).toHaveLength(10);
    });

    it('should handle minimum score of 0', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        differentiation_score: 0,
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText('0/10')).toBeInTheDocument();
    });

    it('should handle maximum score of 10', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        differentiation_score: 10,
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText('10/10')).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty direct competitors', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: [],
        indirect_competitors: [],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.queryByText(/Direct Competitors/i)).not.toBeInTheDocument();
    });

    it('should handle empty indirect competitors', () => {
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        indirect_competitors: [],
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.queryByText(/Indirect Competitors/i)).not.toBeInTheDocument();
    });

    it('should handle many competitors', () => {
      const manyCompetitors = Array.from({ length: 10 }, (_, i) =>
        createMockCompetitor({ name: `Competitor ${i + 1}` })
      );
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        direct_competitors: manyCompetitors,
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(/Direct Competitors \(10\)/i)).toBeInTheDocument();
    });

    it('should handle very long moat description', () => {
      const longMoat = 'A'.repeat(500);
      const competitiveAnalysis = createMockCompetitiveAnalysis({
        competitive_moat: longMoat,
      });
      render(<CompetitorCards competitiveAnalysis={competitiveAnalysis} />);

      expect(screen.getByText(longMoat)).toBeInTheDocument();
    });
  });
});
