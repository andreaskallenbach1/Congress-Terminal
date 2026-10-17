import { defineConfig } from 'astro/config';

// Served by GitHub Pages at https://andreaskallenbach1.github.io/Congress-Terminal/
export default defineConfig({
  site: 'https://andreaskallenbach1.github.io',
  base: '/Congress-Terminal',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
