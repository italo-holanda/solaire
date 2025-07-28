import type { AxiosResponse } from 'axios';
import api from '../instance';
import type { Category } from '@/types/category/category';

/**
 * Get list of categories
 */
export const getCategories = async (): Promise<Category[]> => {
  const response: AxiosResponse<Category[]> = await api.get('/categories');
  return response.data;
}; 