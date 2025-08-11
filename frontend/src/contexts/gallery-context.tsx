import { createContext, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type { Thought } from "@/types";

type GalleryContextValue = {
  selectedThoughts: Thought[];
  setSelectedThoughts: (thoughts: Thought[]) => void;
  getSelectedThoughts: () => Thought[];
  addSelectedThought: (thought: Thought) => void;
  removeSelectedThought: (thoughtId: string) => void;
  clearSelectedThoughts: () => void;
  isThoughtSelected: (thoughtId: string) => boolean;
};

export const GalleryContext = createContext<
  GalleryContextValue | undefined
>(undefined);

type GalleryProviderProps = {
  children: ReactNode;
};

export function GalleryProvider({ children }: GalleryProviderProps) {
  const [selectedThoughts, setSelectedThoughts] = useState<Thought[]>([]);

  const value = useMemo<GalleryContextValue>(
    () => ({
      selectedThoughts,
      setSelectedThoughts,
      getSelectedThoughts: () => selectedThoughts,
      addSelectedThought: (thought: Thought) => {
        setSelectedThoughts(prev => 
          prev.some(t => t.id === thought.id) 
            ? prev 
            : [...prev, thought]
        );
      },
      removeSelectedThought: (thoughtId: string) => {
        setSelectedThoughts(prev => 
          prev.filter(thought => thought.id !== thoughtId)
        );
      },
      clearSelectedThoughts: () => {
        setSelectedThoughts([]);
      },
      isThoughtSelected: (thoughtId: string) => {
        return selectedThoughts.some(thought => thought.id === thoughtId);
      },
    }),
    [selectedThoughts]
  );

  return (
    <GalleryContext.Provider value={value}>
      {children}
    </GalleryContext.Provider>
  );
}
