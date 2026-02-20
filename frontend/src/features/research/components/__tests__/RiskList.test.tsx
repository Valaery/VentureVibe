// ABOUTME: Unit tests for RiskList component covering risk factor display and severity-based sorting
// ABOUTME: Tests severity badge colors (critical=red, high=orange, medium=yellow, low=green) and risk categorization

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { RiskList } from '../RiskList';
import { createMockRiskFactor } from '@/test/mockData/researchResultFactory';
import type { RiskSeverity } from '@/features/research/data/services/researchService';

describe('RiskList', () => {
  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const risks = [createMockRiskFactor()];
      render(<RiskList risks={risks} />);

      expect(screen.getByText(/Market adoption may be slower than expected/i)).toBeInTheDocument();
    });

    it('should render multiple risk factors', () => {
      const risks = [
        createMockRiskFactor({ description: 'Risk 1' }),
        createMockRiskFactor({ description: 'Risk 2' }),
        createMockRiskFactor({ description: 'Risk 3' }),
      ];
      render(<RiskList risks={risks} />);

      expect(screen.getByText('Risk 1')).toBeInTheDocument();
      expect(screen.getByText('Risk 2')).toBeInTheDocument();
      expect(screen.getByText('Risk 3')).toBeInTheDocument();
    });

    it('should display risk description', () => {
      const description = 'Technical debt may slow development';
      const risks = [createMockRiskFactor({ description })];
      render(<RiskList risks={risks} />);

      expect(screen.getByText(description)).toBeInTheDocument();
    });

    it('should display risk mitigation', () => {
      const mitigation = 'Implement code reviews and refactoring sprints';
      const risks = [createMockRiskFactor({ mitigation })];
      render(<RiskList risks={risks} />);

      expect(screen.getByText(mitigation)).toBeInTheDocument();
    });

    it('should display risk category', () => {
      const risks = [createMockRiskFactor({ category: 'technical' })];
      render(<RiskList risks={risks} />);

      expect(screen.getByText('technical')).toBeInTheDocument();
    });
  });

  describe('Severity Badge Colors', () => {
    it('should render critical severity with red styling', () => {
      const risks = [
        createMockRiskFactor({
          severity: 'critical',
          description: 'Critical risk',
        }),
      ];
      render(<RiskList risks={risks} />);

      const badge = screen.getByText('Critical');
      expect(badge).toHaveClass('bg-red-100', 'text-red-700', 'border-red-300');
    });

    it('should render high severity with orange styling', () => {
      const risks = [
        createMockRiskFactor({
          severity: 'high',
          description: 'High risk',
        }),
      ];
      render(<RiskList risks={risks} />);

      const badge = screen.getByText('High');
      expect(badge).toHaveClass('bg-orange-100', 'text-orange-700', 'border-orange-300');
    });

    it('should render medium severity with yellow styling', () => {
      const risks = [
        createMockRiskFactor({
          severity: 'medium',
          description: 'Medium risk',
        }),
      ];
      render(<RiskList risks={risks} />);

      const badge = screen.getByText('Medium');
      expect(badge).toHaveClass('bg-yellow-100', 'text-yellow-700', 'border-yellow-300');
    });

    it('should render low severity with green styling', () => {
      const risks = [
        createMockRiskFactor({
          severity: 'low',
          description: 'Low risk',
        }),
      ];
      render(<RiskList risks={risks} />);

      const badge = screen.getByText('Low');
      expect(badge).toHaveClass('bg-green-100', 'text-green-700', 'border-green-300');
    });
  });

  describe('Border Colors', () => {
    it('should render critical risk with red left border', () => {
      const risks = [createMockRiskFactor({ severity: 'critical', description: 'Test' })];
      const { container } = render(<RiskList risks={risks} />);

      const riskCard = container.querySelector('.border-l-red-600');
      expect(riskCard).toBeInTheDocument();
    });

    it('should render high risk with orange left border', () => {
      const risks = [createMockRiskFactor({ severity: 'high', description: 'Test' })];
      const { container } = render(<RiskList risks={risks} />);

      const riskCard = container.querySelector('.border-l-orange-500');
      expect(riskCard).toBeInTheDocument();
    });

    it('should render medium risk with yellow left border', () => {
      const risks = [createMockRiskFactor({ severity: 'medium', description: 'Test' })];
      const { container } = render(<RiskList risks={risks} />);

      const riskCard = container.querySelector('.border-l-yellow-500');
      expect(riskCard).toBeInTheDocument();
    });

    it('should render low risk with green left border', () => {
      const risks = [createMockRiskFactor({ severity: 'low', description: 'Test' })];
      const { container } = render(<RiskList risks={risks} />);

      const riskCard = container.querySelector('.border-l-green-500');
      expect(riskCard).toBeInTheDocument();
    });
  });

  describe('Severity Sorting', () => {
    it('should sort risks by severity (critical first)', () => {
      const risks = [
        createMockRiskFactor({ severity: 'low', description: 'Low risk' }),
        createMockRiskFactor({ severity: 'critical', description: 'Critical risk' }),
        createMockRiskFactor({ severity: 'medium', description: 'Medium risk' }),
        createMockRiskFactor({ severity: 'high', description: 'High risk' }),
      ];
      render(<RiskList risks={risks} />);

      const descriptions = screen.getAllByText(/risk$/i).map(el => el.textContent);
      expect(descriptions[0]).toBe('Critical risk');
      expect(descriptions[1]).toBe('High risk');
      expect(descriptions[2]).toBe('Medium risk');
      expect(descriptions[3]).toBe('Low risk');
    });

    it('should handle multiple risks of the same severity', () => {
      const risks = [
        createMockRiskFactor({ severity: 'high', description: 'High risk 1' }),
        createMockRiskFactor({ severity: 'high', description: 'High risk 2' }),
      ];
      render(<RiskList risks={risks} />);

      expect(screen.getByText('High risk 1')).toBeInTheDocument();
      expect(screen.getByText('High risk 2')).toBeInTheDocument();
    });
  });

  describe('Risk Categories', () => {
    const categories = ['market', 'technical', 'regulatory', 'competitive', 'financial', 'execution'] as const;

    categories.forEach(category => {
      it(`should display ${category} category`, () => {
        const risks = [createMockRiskFactor({ category })];
        render(<RiskList risks={risks} />);

        expect(screen.getByText(category)).toBeInTheDocument();
      });
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty risks array', () => {
      const { container } = render(<RiskList risks={[]} />);

      expect(container.firstChild?.childNodes).toHaveLength(0);
    });

    it('should handle very long risk description', () => {
      const longDescription = 'A'.repeat(500);
      const risks = [createMockRiskFactor({ description: longDescription })];
      render(<RiskList risks={risks} />);

      expect(screen.getByText(longDescription)).toBeInTheDocument();
    });

    it('should handle very long mitigation text', () => {
      const longMitigation = 'B'.repeat(500);
      const risks = [createMockRiskFactor({ mitigation: longMitigation })];
      render(<RiskList risks={risks} />);

      expect(screen.getByText(longMitigation)).toBeInTheDocument();
    });

    it('should handle single risk', () => {
      const risks = [createMockRiskFactor({ description: 'Single risk' })];
      render(<RiskList risks={risks} />);

      expect(screen.getByText('Single risk')).toBeInTheDocument();
    });

    it('should handle many risks', () => {
      const manyRisks = Array.from({ length: 20 }, (_, i) =>
        createMockRiskFactor({
          description: `Risk ${i + 1}`,
          severity: ['critical', 'high', 'medium', 'low'][i % 4] as RiskSeverity,
        })
      );
      render(<RiskList risks={manyRisks} />);

      // Check that first and last risk render
      expect(screen.getByText('Risk 1')).toBeInTheDocument();
      expect(screen.getByText('Risk 20')).toBeInTheDocument();
    });

    it('should not mutate original risks array', () => {
      const risks = [
        createMockRiskFactor({ severity: 'low', description: 'Low' }),
        createMockRiskFactor({ severity: 'critical', description: 'Critical' }),
      ];
      const originalOrder = [...risks];

      render(<RiskList risks={risks} />);

      // Original array should not be mutated
      expect(risks).toEqual(originalOrder);
    });
  });
});
