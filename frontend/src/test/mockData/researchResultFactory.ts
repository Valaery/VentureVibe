// ABOUTME: Mock data factories for ResearchResult and related types for testing
// ABOUTME: Provides builder functions to create test fixtures with customizable values

import type {
  ResearchResult,
  MarketSizing,
  Competitor,
  CompetitiveAnalysis,
  SWOTAnalysis,
  RiskFactor,
  GTMStrategy,
  AgentThought,
  InvestmentReadiness,
  ConfidenceLevel,
  RiskSeverity,
  RiskCategory,
} from '@/features/research/data/services/researchService';

export const createMockMarketSizing = (overrides?: Partial<MarketSizing>): MarketSizing => ({
  tam_usd_billion: 50,
  sam_usd_billion: 10,
  som_usd_million: 500,
  sizing_methodology: 'top_down',
  tam_source_basis: 'Industry reports and market analysis',
  growth_rate_pct: 15,
  ...overrides,
});

export const createMockCompetitor = (overrides?: Partial<Competitor>): Competitor => ({
  name: 'Competitor Inc',
  positioning: 'Enterprise SaaS platform',
  primary_weakness: 'Poor user experience',
  estimated_funding_usd_million: 100,
  business_model: 'Subscription-based',
  ...overrides,
});

export const createMockCompetitiveAnalysis = (
  overrides?: Partial<CompetitiveAnalysis>
): CompetitiveAnalysis => ({
  direct_competitors: [
    createMockCompetitor({ name: 'Direct Competitor 1' }),
    createMockCompetitor({ name: 'Direct Competitor 2' }),
  ],
  indirect_competitors: [
    createMockCompetitor({ name: 'Indirect Competitor 1' }),
  ],
  competitive_moat: 'Proprietary AI technology and network effects',
  differentiation_score: 7,
  ...overrides,
});

export const createMockSWOTAnalysis = (overrides?: Partial<SWOTAnalysis>): SWOTAnalysis => ({
  strengths: [
    'Strong technical team',
    'First-mover advantage',
    'Proven market demand',
  ],
  weaknesses: [
    'Limited funding',
    'Small team size',
  ],
  opportunities: [
    'Growing market size',
    'Partnership potential',
  ],
  threats: [
    'Established competitors',
    'Regulatory changes',
  ],
  ...overrides,
});

export const createMockRiskFactor = (overrides?: Partial<RiskFactor>): RiskFactor => ({
  category: 'market',
  description: 'Market adoption may be slower than expected',
  severity: 'medium',
  mitigation: 'Conduct early customer development and pilots',
  ...overrides,
});

export const createMockGTMStrategy = (overrides?: Partial<GTMStrategy>): GTMStrategy => ({
  primary_channel: 'Content Marketing',
  secondary_channels: ['LinkedIn Ads', 'Partner Network'],
  pricing_model: 'Freemium with tiered plans',
  estimated_cac_usd: 250,
  target_icp: 'Mid-market B2B SaaS companies with 50-500 employees',
  time_to_first_revenue_months: 6,
  ...overrides,
});

export const createMockAgentThought = (overrides?: Partial<AgentThought>): AgentThought => ({
  agent_name: 'Product Strategist',
  thought: 'Analyzing market opportunity and positioning strategy',
  timestamp: '2024-01-01T12:00:00Z',
  ...overrides,
});

export const createMockResearchResult = (
  overrides?: Partial<ResearchResult>
): ResearchResult => ({
  id: 'test-research-id',
  idea_id: 'test-idea-id',
  executive_summary: 'This is a comprehensive market validation for an innovative AI-powered product idea targeting the B2B SaaS market.',
  market_analysis: '## Market Overview\n\nThe market shows strong growth potential with increasing demand for AI-powered solutions.',
  strategic_advice: '## Strategic Recommendations\n\nFocus on early adopters and iterate quickly based on feedback.',
  key_assumptions: [
    'Market will grow at 15% CAGR',
    'Early adopters will pay premium pricing',
    'Team can execute on technical roadmap',
  ],
  recommended_next_steps: [
    'Build MVP with core features',
    'Conduct customer development interviews',
    'Secure seed funding',
  ],
  feasibility_score: 72,
  confidence_level: 'high',
  investment_readiness: 'seed_ready',
  market_sizing: createMockMarketSizing(),
  competitive_analysis: createMockCompetitiveAnalysis(),
  swot_analysis: createMockSWOTAnalysis(),
  risk_factors: [
    createMockRiskFactor({
      severity: 'critical',
      category: 'technical',
      description: 'AI model performance may not meet expectations',
    }),
    createMockRiskFactor({
      severity: 'high',
      category: 'competitive',
      description: 'Established players may enter the market',
    }),
    createMockRiskFactor({
      severity: 'medium',
      category: 'market',
      description: 'Market adoption may be slower than expected',
    }),
    createMockRiskFactor({
      severity: 'low',
      category: 'regulatory',
      description: 'Minor compliance requirements',
    }),
  ],
  gtm_strategy: createMockGTMStrategy(),
  agent_thoughts: [
    createMockAgentThought({
      agent_name: 'Product Strategist',
      thought: 'Initial strategy formulation complete',
    }),
    createMockAgentThought({
      agent_name: 'Market Sizing Analyst',
      thought: 'TAM/SAM/SOM analysis complete',
    }),
  ],
  ...overrides,
});
