import { api } from "@/core/data/api";
import { ResearchRequestInput } from "../schemas/researchSchemas";

export interface AgentThought {
    agent_name: string;
    thought: string;
    timestamp: string;
}

export interface ResearchResult {
    id: string;
    idea_id: string;
    market_analysis: string;
    feasibility_score: number;
    competitors: string[];
    strategic_advice: string;
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
