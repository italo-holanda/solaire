import { useQuery } from "@tanstack/react-query";
import type { ListThoughtsDTO } from "@/types/thought/dto";
import { getThoughts } from "@/services/api/thoughts/thoughts";

export const useThoughtsQuery = (params: ListThoughtsDTO = {}) => {
  return useQuery({
    queryKey: ["thoughts", params],
    queryFn: async () => {
      const thoughts = await getThoughts(params);
      return thoughts;
    },
  });
};
