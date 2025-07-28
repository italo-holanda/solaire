import type { AxiosResponse } from 'axios';
import api from '../instance';
import type { Thought } from '@/types/thought/thought';
import type {
  CreateThoughtDTO,
  UpdateThoughtDTO,
  ListThoughtsDTO,
  DeleteThoughtDTO,
  ListRelatedThoughtsDTO,
  SuggestRelevantTopicsDTO,
} from '@/types/thought/dto';

/**
 * Get list of thoughts with optional search term
 */
export const getThoughts = async (params: ListThoughtsDTO): Promise<Thought[]> => {
  const response: AxiosResponse<Thought[]> = await api.get('/thoughts', { params });
  return response.data;
};

/**
 * Create a new thought
 */
export const createThought = async (data: CreateThoughtDTO): Promise<void> => {
  await api.post('/thoughts', data);
};

/**
 * Delete a thought by ID
 */
export const deleteThought = async (thoughtId: string): Promise<void> => {
  await api.delete(`/thoughts/${thoughtId}`);
};

/**
 * Get topic suggestions for a thought
 */
export const getRelevantTopics = async (thoughtId: string): Promise<string[]> => {
  const response: AxiosResponse<string[]> = await api.get(`/thoughts/${thoughtId}/relevant-topics`);
  return response.data;
};

/**
 * Get related thoughts for a given thought
 */
export const getRelatedThoughts = async (thoughtId: string): Promise<Thought[]> => {
  const response: AxiosResponse<Thought[]> = await api.get(`/thoughts/${thoughtId}/related`);
  return response.data;
};

/**
 * Update a thought
 */
export const updateThought = async (data: UpdateThoughtDTO): Promise<Thought> => {
  const response: AxiosResponse<Thought> = await api.patch('/thoughts', data);
  return response.data;
}; 