import type { Entity } from '../common/entity';
import type { Category } from '../category/category';

export type Thought = Entity & {
  title: string;
  summary: string;
  text: string;
  categories: Category[];
  embeddings: number[];
}; 