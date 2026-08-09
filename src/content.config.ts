import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tags: z.array(z.string()),
    emoji: z.string().optional(),
    color: z.string().optional(),
    category: z.string().optional(),
  }),
});

export const collections = { posts };
