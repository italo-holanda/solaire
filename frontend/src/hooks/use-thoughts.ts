import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { ListThoughtsDTO, CreateThoughtDTO } from "@/types/thought/dto";
import { getThoughts, createThought } from "@/services/api/thoughts/thoughts";

export const useThoughts = (params: ListThoughtsDTO = {}) => {
  return useQuery({
    queryKey: ["thoughts", params],
    refetchInterval: 5000,
    queryFn: async () => {
      const thoughts = await getThoughts(params);
      return thoughts;
    },
  });
};

export const useCreateThought = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateThoughtDTO) => {
      return await createThought(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["thoughts"] });
    },
  });
};
