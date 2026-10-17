// Reads the briefing files the pipeline publishes into /briefings at the repository root.
// The full edition schema is fixed in build step 3; this loader only needs id, date and compiledAt.
import fs from 'node:fs';
import path from 'node:path';

export interface EditionMeta {
  id: string;          // e.g. "2026-10-19-daily"
  kind: 'daily' | 'weekly';
  date: string;        // ISO date of the edition, e.g. "2026-10-19"
  compiledAt: string;  // ISO timestamp with offset
  readingMinutes?: number;
}

const BRIEFINGS_DIR = path.resolve(process.cwd(), '..', 'briefings');

export function listEditions(): EditionMeta[] {
  if (!fs.existsSync(BRIEFINGS_DIR)) return [];
  return fs
    .readdirSync(BRIEFINGS_DIR)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(fs.readFileSync(path.join(BRIEFINGS_DIR, f), 'utf8')) as EditionMeta)
    .sort((a, b) => b.compiledAt.localeCompare(a.compiledAt));
}

export function latestEdition(): EditionMeta | undefined {
  return listEditions()[0];
}

const BERLIN = 'Europe/Berlin';

export function formatEditionDate(iso: string): string {
  return new Intl.DateTimeFormat('en-US', { timeZone: BERLIN, weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
    .format(new Date(iso));
}

export function formatBerlinTime(iso: string): string {
  return new Intl.DateTimeFormat('en-GB', { timeZone: BERLIN, hour: '2-digit', minute: '2-digit', timeZoneName: 'short' })
    .format(new Date(iso));
}
