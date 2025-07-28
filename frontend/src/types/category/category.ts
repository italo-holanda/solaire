import type { Entity } from '../common/entity';

export type Category = Entity & {
  name: string;
  color?: string; // Optional hex color code
}; 