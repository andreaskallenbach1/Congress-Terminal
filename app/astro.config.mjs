import { defineConfig } from 'astro/config';

// Served by GitHub Pages at https://andreaskallenbach1.github.io/Congress-Terminal/
export default defineConfig({
  site: 'https://andreaskallenbach1.github.io',
  base: '/Congress-Terminal',
  trailingSlash: 'always',
  build: { format: 'directory' },
  // Sample builds keep their own content cache, so test data can never leak into a real build.
  cacheDir: process.env.BRIEFINGS_DIR ? './node_modules/.astro-sample' : './node_modules/.astro',
});
