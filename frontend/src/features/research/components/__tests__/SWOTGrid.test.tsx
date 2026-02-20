// ABOUTME: Unit tests for SWOTGrid component covering 2x2 grid layout and SWOT analysis data
// ABOUTME: Tests rendering of strengths, weaknesses, opportunities, threats with correct colors and layout

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SWOTGrid } from '../SWOTGrid';
import { createMockSWOTAnalysis } from '@/test/mockData/researchResultFactory';

describe('SWOTGrid', () => {
  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const swot = createMockSWOTAnalysis();
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText('Strengths')).toBeInTheDocument();
      expect(screen.getByText('Weaknesses')).toBeInTheDocument();
      expect(screen.getByText('Opportunities')).toBeInTheDocument();
      expect(screen.getByText('Threats')).toBeInTheDocument();
    });

    it('should render all four quadrants', () => {
      const swot = createMockSWOTAnalysis();
      const { container } = render(<SWOTGrid swot={swot} />);

      // Should have 4 quadrant divs
      const quadrants = container.querySelectorAll('.rounded-lg.border.p-4');
      expect(quadrants).toHaveLength(4);
    });
  });

  describe('Strengths Quadrant', () => {
    it('should render all strength items', () => {
      const strengths = ['Strength 1', 'Strength 2', 'Strength 3'];
      const swot = createMockSWOTAnalysis({ strengths });
      render(<SWOTGrid swot={swot} />);

      strengths.forEach(strength => {
        expect(screen.getByText(strength)).toBeInTheDocument();
      });
    });

    it('should handle empty strengths array', () => {
      const swot = createMockSWOTAnalysis({ strengths: [] });
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText('Strengths')).toBeInTheDocument();
    });

    it('should render strengths with correct styling', () => {
      const swot = createMockSWOTAnalysis({ strengths: ['Test Strength'] });
      const { container } = render(<SWOTGrid swot={swot} />);

      const strengthsSection = screen.getByText('Strengths').closest('div');
      expect(strengthsSection).toHaveClass('bg-green-50');
      expect(strengthsSection).toHaveClass('border-green-200');
    });
  });

  describe('Weaknesses Quadrant', () => {
    it('should render all weakness items', () => {
      const weaknesses = ['Weakness 1', 'Weakness 2'];
      const swot = createMockSWOTAnalysis({ weaknesses });
      render(<SWOTGrid swot={swot} />);

      weaknesses.forEach(weakness => {
        expect(screen.getByText(weakness)).toBeInTheDocument();
      });
    });

    it('should handle empty weaknesses array', () => {
      const swot = createMockSWOTAnalysis({ weaknesses: [] });
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText('Weaknesses')).toBeInTheDocument();
    });

    it('should render weaknesses with correct styling', () => {
      const swot = createMockSWOTAnalysis({ weaknesses: ['Test Weakness'] });
      const { container } = render(<SWOTGrid swot={swot} />);

      const weaknessesSection = screen.getByText('Weaknesses').closest('div');
      expect(weaknessesSection).toHaveClass('bg-red-50');
      expect(weaknessesSection).toHaveClass('border-red-200');
    });
  });

  describe('Opportunities Quadrant', () => {
    it('should render all opportunity items', () => {
      const opportunities = ['Opportunity 1', 'Opportunity 2', 'Opportunity 3'];
      const swot = createMockSWOTAnalysis({ opportunities });
      render(<SWOTGrid swot={swot} />);

      opportunities.forEach(opportunity => {
        expect(screen.getByText(opportunity)).toBeInTheDocument();
      });
    });

    it('should handle empty opportunities array', () => {
      const swot = createMockSWOTAnalysis({ opportunities: [] });
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText('Opportunities')).toBeInTheDocument();
    });

    it('should render opportunities with correct styling', () => {
      const swot = createMockSWOTAnalysis({ opportunities: ['Test Opportunity'] });
      const { container } = render(<SWOTGrid swot={swot} />);

      const opportunitiesSection = screen.getByText('Opportunities').closest('div');
      expect(opportunitiesSection).toHaveClass('bg-blue-50');
      expect(opportunitiesSection).toHaveClass('border-blue-200');
    });
  });

  describe('Threats Quadrant', () => {
    it('should render all threat items', () => {
      const threats = ['Threat 1', 'Threat 2'];
      const swot = createMockSWOTAnalysis({ threats });
      render(<SWOTGrid swot={swot} />);

      threats.forEach(threat => {
        expect(screen.getByText(threat)).toBeInTheDocument();
      });
    });

    it('should handle empty threats array', () => {
      const swot = createMockSWOTAnalysis({ threats: [] });
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText('Threats')).toBeInTheDocument();
    });

    it('should render threats with correct styling', () => {
      const swot = createMockSWOTAnalysis({ threats: ['Test Threat'] });
      const { container } = render(<SWOTGrid swot={swot} />);

      const threatsSection = screen.getByText('Threats').closest('div');
      expect(threatsSection).toHaveClass('bg-amber-50');
      expect(threatsSection).toHaveClass('border-amber-200');
    });
  });

  describe('Edge Cases', () => {
    it('should handle all empty arrays', () => {
      const swot = createMockSWOTAnalysis({
        strengths: [],
        weaknesses: [],
        opportunities: [],
        threats: [],
      });
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText('Strengths')).toBeInTheDocument();
      expect(screen.getByText('Weaknesses')).toBeInTheDocument();
      expect(screen.getByText('Opportunities')).toBeInTheDocument();
      expect(screen.getByText('Threats')).toBeInTheDocument();
    });

    it('should handle very long item text', () => {
      const longText = 'A'.repeat(200);
      const swot = createMockSWOTAnalysis({
        strengths: [longText],
      });
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText(longText)).toBeInTheDocument();
    });

    it('should handle many items in each quadrant', () => {
      const manyItems = Array.from({ length: 20 }, (_, i) => `Item ${i + 1}`);
      const swot = createMockSWOTAnalysis({
        strengths: manyItems,
        weaknesses: manyItems,
        opportunities: manyItems,
        threats: manyItems,
      });
      render(<SWOTGrid swot={swot} />);

      // Check that first and last items render (appears in all 4 quadrants)
      expect(screen.getAllByText('Item 1')).toHaveLength(4);
      expect(screen.getAllByText('Item 20')).toHaveLength(4);
    });

    it('should handle single item in each quadrant', () => {
      const swot = createMockSWOTAnalysis({
        strengths: ['Only strength'],
        weaknesses: ['Only weakness'],
        opportunities: ['Only opportunity'],
        threats: ['Only threat'],
      });
      render(<SWOTGrid swot={swot} />);

      expect(screen.getByText('Only strength')).toBeInTheDocument();
      expect(screen.getByText('Only weakness')).toBeInTheDocument();
      expect(screen.getByText('Only opportunity')).toBeInTheDocument();
      expect(screen.getByText('Only threat')).toBeInTheDocument();
    });
  });
});
