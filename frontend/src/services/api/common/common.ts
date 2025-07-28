import type { AxiosResponse } from 'axios';
import api from '../instance';

export type HealthResponse = {
  status: string;
  version: string;
};

/**
 * Get health status of the backend
 */
export const getHealth = async (): Promise<HealthResponse> => {
  const response: AxiosResponse<HealthResponse> = await api.get('/healthz');
  return response.data;
}; 