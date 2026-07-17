import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://openthedoor.cn',
  integrations: [tailwind()],
});
