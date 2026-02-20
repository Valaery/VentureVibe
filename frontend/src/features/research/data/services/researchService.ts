import { api } from "@/core/data/api";
import { ResearchRequestInput } from "../schemas/researchSchemas";

export interface MarketSizing {
    tam_usd_billion: number;
    sam_usd_billion: number;
    som_usd_million: number;
    sizing_methodology: 'top_down' | 'bottom_up' | 'hybrid';
    tam_source_basis: string;
    growth_rate_pct: number | null;
}

export interface Competitor {
    name: string;
    positioning: string;
    primary_weakness: string;
    estimated_funding_usd_million: number | null;
    business_model: string;
}

export interface CompetitiveAnalysis {
    direct_competitors: Competitor[];
    indirect_competitors: Competitor[];
    competitive_moat: string;
    differentiation_score: number;
}

export interface SWOTAnalysis {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
}

export type RiskSeverity = 'low' | 'medium' | 'high' | 'critical';
export type RiskCategory = 'market' | 'technical' | 'regulatory' | 'competitive' | 'financial' | 'execution';

export interface RiskFactor {
    category: RiskCategory;
    description: string;
    severity: RiskSeverity;
    mitigation: string;
}

export interface GTMStrategy {
    primary_channel: string;
    secondary_channels: string[];
    pricing_model: string;
    estimated_cac_usd: number | null;
    target_icp: string;
    time_to_first_revenue_months: number;
}

export type ConfidenceLevel = 'low' | 'medium' | 'high';
export type InvestmentReadiness = 'pre_idea' | 'idea_stage' | 'mvp_ready' | 'seed_ready' | 'series_a_ready';

export interface AgentThought {
    agent_name: string;
    thought: string;
    timestamp: string;
}

export interface ResearchResult {
    id: string;
    idea_id: string;
    executive_summary: string;
    market_analysis: string;
    strategic_advice: string;
    key_assumptions: string[];
    recommended_next_steps: string[];
    feasibility_score: number;
    confidence_level: ConfidenceLevel;
    investment_readiness: InvestmentReadiness;
    market_sizing: MarketSizing;
    competitive_analysis: CompetitiveAnalysis;
    swot_analysis: SWOTAnalysis;
    risk_factors: RiskFactor[];
    gtm_strategy: GTMStrategy;
    agent_thoughts: AgentThought[];
}

export const researchService = {
    createResearch: async (data: ResearchRequestInput): Promise<ResearchResult> => {
        const response = await api.post<ResearchResult>('/research/', data);
        return response.data;
    },

    getResearch: async (ideaId: string): Promise<ResearchResult> => {
        const response = await api.get<ResearchResult>(`/research/${ideaId}`);
        return response.data;
    }
}
