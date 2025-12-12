import { z } from "zod";

export const researchRequestSchema = z.object({
    content: z.string().min(10, "Idea must be at least 10 characters"),
    target_audience: z.string().min(3, "Target audience must be specified"),
});

export const researchResultSchema = z.object({
    market_analysis: z.string(),
    feasibility_score: z.number().min(0).max(100),
    competitors: z.array(z.string()),
    strategic_advice: z.string(),
});

export type ResearchRequestInput = z.infer<typeof researchRequestSchema>;
export type ResearchResult = z.infer<typeof researchResultSchema>;
