import { useQuery } from "@tanstack/react-query";
import { researchService } from "../../data/services/researchService";

export const useResearchQuery = (ideaId: string) => {
    return useQuery({
        queryKey: ['research', ideaId],
        queryFn: () => researchService.getResearch(ideaId),
        enabled: !!ideaId,
    });
};
