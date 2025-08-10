import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { ListThoughtsDTO, CreateThoughtDTO, UpdateThoughtDTO } from "@/types/thought/dto";
import {
  getThoughts,
  createThought,
  updateThought,
  deleteThought,
} from "@/services/api/thoughts/thoughts";
import { toast } from "sonner";
import { useNavigation } from "@/hooks/use-navigation";

export const useThoughts = (overrideParams: ListThoughtsDTO = {}) => {
  const { params: navigationParams, currentView } = useNavigation();
  const hasOverrideParams = Object.keys(overrideParams).length > 0;
  const apiParams: ListThoughtsDTO = hasOverrideParams
    ? overrideParams
    : { 
        search_term: currentView === "gallery" ? navigationParams?.searchTerms : undefined,
        category_ids: navigationParams?.categories?.map(cat => cat.id)
      };

  return useQuery({
    queryKey: ["thoughts", apiParams],
    refetchInterval: 5000,
    queryFn: async () => {
      const thoughts = await getThoughts(apiParams);
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

export const useUpdateThought = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: UpdateThoughtDTO) => {
      return await updateThought(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["thoughts"] });
      toast("Thought has been updated");
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
