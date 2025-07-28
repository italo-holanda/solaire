import type { PublicationFormat } from './publication';

export type CreatePublicationPreviewDTO = {
  selected_thought_ids: string[];
  publication_format: PublicationFormat;
  user_guideline: string;
};

export type CreatePublicationContentDTO = {
  publication_id: string;
  publication_outlining: string[];
}; 