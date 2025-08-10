export type CreateThoughtDTO = {
  text: string;
};

export type UpdateThoughtDTO = {
  thought_id: string;
  text: string;
};

export type ListThoughtsDTO = {
  search_term?: string;
  category_ids?: string[];
};

export type DeleteThoughtDTO = {
  thought_id: string;
};

export type ListRelatedThoughtsDTO = {
  thought_id: string;
};

export type SuggestRelevantTopicsDTO = {
  thought_id: string;
}; 