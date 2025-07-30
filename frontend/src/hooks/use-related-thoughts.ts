import { useQuery } from "@tanstack/react-query";
import { getRelatedThoughts } from "@/services/api/thoughts/thoughts";

export const useRelatedThoughts = (params: { thoughtId?: string }) => {
  return useQuery({
    queryKey: ["related-thoughts", params],
    enabled: !!params.thoughtId,
    queryFn: async () => {
      if (!params.thoughtId) return [];
      const thoughts = await getRelatedThoughts(params.thoughtId);
      return thoughts;
    },
  });
};
