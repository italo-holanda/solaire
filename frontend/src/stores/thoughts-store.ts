import { create } from 'zustand';
import { useQuery } from '@tanstack/react-query';
import type { Thought } from '@/types/thought/thought';
import type { ListThoughtsDTO } from '@/types/thought/dto';
import { getThoughts } from '@/services/api/thoughts/thoughts';

interface ThoughtsState {
  thoughts: Thought[];
  isLoading: boolean;
  error: string | null;
}

interface ThoughtsActions {
  setThoughts: (thoughts: Thought[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

type ThoughtsStore = ThoughtsState & ThoughtsActions;

export const useThoughtsStore = create<ThoughtsStore>((set) => ({
  thoughts: [],
  isLoading: false,
  error: null,

  setThoughts: (thoughts) => set({ thoughts }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
}));

export const useThoughtsQuery = (params: ListThoughtsDTO = {}) => {
  const { setThoughts, setLoading, setError } = useThoughtsStore();

  return useQuery({
    queryKey: ['thoughts', params],
    queryFn: async () => {
      setLoading(true);
      setError(null);
      try {
        const thoughts = await getThoughts(params);
        setThoughts(thoughts);
        return thoughts;
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to fetch thoughts';
        setError(errorMessage);
        throw error;
      } finally {
        setLoading(false);
      }
    },
  });
};
