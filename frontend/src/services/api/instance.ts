import { logger } from "@/utils/logging";
import axios, {
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
} from "axios";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export const api: AxiosInstance = axios.create({
  baseURL: BACKEND_URL,
  timeout: 100000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    logger.info(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    logger.error("Request Error:", error);
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response: AxiosResponse) => {
    logger.info(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    logger.error("Response Error:", error);

    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          logger.error("Unauthorized access", data);
          break;
        case 403:
          logger.error("Access forbidden", data);
          break;
        case 404:
          logger.error("Resource not found", data);
          break;
        case 500:
          logger.error("Server error", data);
          break;
        default:
          logger.error(`HTTP Error ${status}:`, data);
      }
    } else if (error.request) {
      logger.error("Network error - no response received");
    } else {
      logger.error("Request setup error:", error.message);
    }

    return Promise.reject(error);
  }
);

export type { AxiosInstance, AxiosRequestConfig, AxiosResponse };

export default api;
