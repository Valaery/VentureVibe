import { z } from "zod";

export const researchRequestSchema = z.object({
    content: z.string().min(10, "Idea must be at least 10 characters"),
    target_audience: z.string().min(3, "Target audience must be specified"),
});

export type ResearchRequestInput = z.infer<typeof researchRequestSchema>;
