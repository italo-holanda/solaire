import type { AxiosResponse } from 'axios';
import api from '../instance';
import type { Publication } from '@/types/publication/publication';
import type {
  CreatePublicationPreviewDTO,
  CreatePublicationContentDTO,
} from '@/types/publication/dto';

/**
 * Create publication preview from selected thoughts
 */
export const createPublicationPreview = async (data: CreatePublicationPreviewDTO): Promise<Publication> => {
  const response: AxiosResponse<Publication> = await api.post('/publications/preview', data);
  return response.data;
};

/**
 * Create publication content from publication id and outlining
 */
export const createPublicationContent = async (data: CreatePublicationContentDTO): Promise<Publication> => {
  const response: AxiosResponse<Publication> = await api.post('/publications/content', data);
  return response.data;
}; 