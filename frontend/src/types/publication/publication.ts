import type { Entity } from '../common/entity';
import type { Category } from '../category/category';

export type PublicationFormat = 
  | "linkedin_post"
  | "blog_post"
  | "short_video"
  | "long_video";

export type PublicationStage = 
  | "preview"
  | "ready";

export type Publication = Entity & {
  title: string;
  content: string;
  categories: Category[];
  outlining: string[];
  format: PublicationFormat;
  stage: PublicationStage;
  thought_ids: string[];
  user_guideline: string;
}; 