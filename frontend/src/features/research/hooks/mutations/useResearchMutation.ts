import { useMutation } from "@tanstack/react-query";
import { researchService } from "../../data/services/researchService";
import { ResearchRequestInput } from "../../data/schemas/researchSchemas";

export const useResearchMutation = () => {
    return useMutation({
        mutationFn: (data: ResearchRequestInput) => researchService.createResearch(data),
    });
};
