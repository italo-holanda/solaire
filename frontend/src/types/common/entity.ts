export type Entity = {
  id: string;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  deleted_at?: string; // ISO datetime string, optional
} 