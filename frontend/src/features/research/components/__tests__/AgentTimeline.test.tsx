// ABOUTME: Unit tests for AgentTimeline component covering agent thought display and staggered animations
// ABOUTME: Tests rendering of agent activity log, empty state, and timeline visualization

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { AgentTimeline } from '../AgentTimeline';
import { createMockAgentThought } from '@/test/mockData/researchResultFactory';

describe('AgentTimeline', () => {
  describe('Rendering', () => {
    it('should render without crashing with valid props', () => {
      const thoughts = [createMockAgentThought()];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText('Product Strategist')).toBeInTheDocument();
    });

    it('should render multiple agent thoughts', () => {
      const thoughts = [
        createMockAgentThought({ agent_name: 'Agent 1', thought: 'Thought 1' }),
        createMockAgentThought({ agent_name: 'Agent 2', thought: 'Thought 2' }),
        createMockAgentThought({ agent_name: 'Agent 3', thought: 'Thought 3' }),
      ];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText('Agent 1')).toBeInTheDocument();
      expect(screen.getByText('Agent 2')).toBeInTheDocument();
      expect(screen.getByText('Agent 3')).toBeInTheDocument();
      expect(screen.getByText('Thought 1')).toBeInTheDocument();
      expect(screen.getByText('Thought 2')).toBeInTheDocument();
      expect(screen.getByText('Thought 3')).toBeInTheDocument();
    });

    it('should display agent names', () => {
      const agentName = 'Market Sizing Analyst';
      const thoughts = [createMockAgentThought({ agent_name: agentName })];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText(agentName)).toBeInTheDocument();
    });

    it('should display agent thoughts', () => {
      const thought = 'Analyzing market opportunity and competitive landscape';
      const thoughts = [createMockAgentThought({ thought })];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText(thought)).toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('should render empty state message when thoughts array is empty', () => {
      render(<AgentTimeline thoughts={[]} />);

      expect(screen.getByText(/No agent activity recorded/i)).toBeInTheDocument();
    });

    it('should render empty state message when thoughts is null', () => {
      render(<AgentTimeline thoughts={null as any} />);

      expect(screen.getByText(/No agent activity recorded/i)).toBeInTheDocument();
    });

    it('should render empty state message when thoughts is undefined', () => {
      render(<AgentTimeline thoughts={undefined as any} />);

      expect(screen.getByText(/No agent activity recorded/i)).toBeInTheDocument();
    });
  });

  describe('Agent Name Colors', () => {
    const agentColors = [
      { name: 'Product Strategist', colorClass: 'bg-violet-500' },
      { name: 'Research Analyst', colorClass: 'bg-blue-500' },
      { name: 'Market Sizing Analyst', colorClass: 'bg-green-500' },
      { name: 'Competitive Intelligence Analyst', colorClass: 'bg-red-500' },
      { name: 'SWOT & Risk Analyst', colorClass: 'bg-amber-500' },
      { name: 'GTM Strategist', colorClass: 'bg-indigo-500' },
    ];

    agentColors.forEach(({ name, colorClass }) => {
      it(`should render ${name} with correct color`, () => {
        const thoughts = [createMockAgentThought({ agent_name: name })];
        const { container } = render(<AgentTimeline thoughts={thoughts} />);

        const colorDot = container.querySelector(`.${colorClass}`);
        expect(colorDot).toBeInTheDocument();
      });
    });

    it('should use default gray color for unknown agent', () => {
      const thoughts = [createMockAgentThought({ agent_name: 'Unknown Agent' })];
      const { container } = render(<AgentTimeline thoughts={thoughts} />);

      const colorDot = container.querySelector('.bg-gray-500');
      expect(colorDot).toBeInTheDocument();
    });
  });

  describe('Timeline Structure', () => {
    it('should render timeline dots for each thought', () => {
      const thoughts = [
        createMockAgentThought(),
        createMockAgentThought(),
        createMockAgentThought(),
      ];
      const { container } = render(<AgentTimeline thoughts={thoughts} />);

      const dots = container.querySelectorAll('.w-2\\.5.h-2\\.5.rounded-full');
      expect(dots).toHaveLength(3);
    });

    it('should render connecting lines between thoughts', () => {
      const thoughts = [
        createMockAgentThought({ thought: 'First' }),
        createMockAgentThought({ thought: 'Second' }),
        createMockAgentThought({ thought: 'Third' }),
      ];
      const { container } = render(<AgentTimeline thoughts={thoughts} />);

      // Connecting lines should be 1 less than total thoughts (no line after last thought)
      const lines = container.querySelectorAll('.w-0\\.5.bg-border.flex-1');
      expect(lines).toHaveLength(2);
    });

    it('should not render connecting line after last thought', () => {
      const thoughts = [createMockAgentThought()];
      const { container } = render(<AgentTimeline thoughts={thoughts} />);

      const lines = container.querySelectorAll('.w-0\\.5.bg-border.flex-1');
      expect(lines).toHaveLength(0); // Single thought should have no connecting line
    });
  });

  describe('Animation', () => {
    it('should apply animation classes to thought entries', () => {
      const thoughts = [createMockAgentThought()];
      const { container } = render(<AgentTimeline thoughts={thoughts} />);

      const animatedDiv = container.querySelector('.animate-in.fade-in.slide-in-from-left-4');
      expect(animatedDiv).toBeInTheDocument();
    });

    it('should apply staggered animation delays', () => {
      const thoughts = [
        createMockAgentThought({ thought: 'First' }),
        createMockAgentThought({ thought: 'Second' }),
      ];
      const { container } = render(<AgentTimeline thoughts={thoughts} />);

      const animatedDivs = container.querySelectorAll('.animate-in');
      expect(animatedDivs).toHaveLength(2);

      // Check that style attribute contains animation delay
      const firstDiv = animatedDivs[0] as HTMLElement;
      const secondDiv = animatedDivs[1] as HTMLElement;

      expect(firstDiv.style.animationDelay).toBe('0ms');
      expect(secondDiv.style.animationDelay).toBe('150ms');
    });
  });

  describe('Edge Cases', () => {
    it('should handle very long agent names', () => {
      const longName = 'A'.repeat(100);
      const thoughts = [createMockAgentThought({ agent_name: longName })];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText(longName)).toBeInTheDocument();
    });

    it('should handle very long thought text', () => {
      const longThought = 'B'.repeat(500);
      const thoughts = [createMockAgentThought({ thought: longThought })];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText(longThought)).toBeInTheDocument();
    });

    it('should handle single thought', () => {
      const thoughts = [createMockAgentThought({ thought: 'Single thought' })];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText('Single thought')).toBeInTheDocument();
    });

    it('should handle many thoughts', () => {
      const manyThoughts = Array.from({ length: 20 }, (_, i) =>
        createMockAgentThought({
          agent_name: `Agent ${i + 1}`,
          thought: `Thought ${i + 1}`,
        })
      );
      render(<AgentTimeline thoughts={manyThoughts} />);

      expect(screen.getByText('Agent 1')).toBeInTheDocument();
      expect(screen.getByText('Agent 20')).toBeInTheDocument();
      expect(screen.getByText('Thought 1')).toBeInTheDocument();
      expect(screen.getByText('Thought 20')).toBeInTheDocument();
    });

    it('should handle empty thought text', () => {
      const thoughts = [createMockAgentThought({ thought: '' })];
      render(<AgentTimeline thoughts={thoughts} />);

      expect(screen.getByText('Product Strategist')).toBeInTheDocument();
    });

    it('should handle duplicate agent names', () => {
      const thoughts = [
        createMockAgentThought({ agent_name: 'Agent', thought: 'First' }),
        createMockAgentThought({ agent_name: 'Agent', thought: 'Second' }),
      ];
      render(<AgentTimeline thoughts={thoughts} />);

      const agentNames = screen.getAllByText('Agent');
      expect(agentNames).toHaveLength(2);
    });
  });
});
