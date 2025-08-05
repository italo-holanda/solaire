import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { ListThoughtsDTO, CreateThoughtDTO } from "@/types/thought/dto";
import {
  getThoughts,
  createThought,
  deleteThought,
} from "@/services/api/thoughts/thoughts";
import { toast } from "sonner";

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
      toast("Thought has been created");
    },
  });
};

export const useDeleteThought = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (thoughtId: string) => {
      return await deleteThought(thoughtId);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["thoughts"] });
      toast("Thought has been deleted");
    },
  });
};
