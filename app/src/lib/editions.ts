// Access to published editions and small formatting helpers. All times shown in Berlin time.
import { getCollection, type CollectionEntry } from 'astro:content';

export type Edition = CollectionEntry<'briefings'>['data'];
export type Story = Edition['stories'][number];
export type Claim = Story['claims'][number];
export type Vote = Edition['floor']['votes'][number];

export async function listEditions(): Promise<Edition[]> {
  const entries = await getCollection('briefings');
  const sample = entries.find((e) => e.data.sample);
  if (sample && !process.env.BRIEFINGS_DIR) {
    throw new Error(`Refusing to publish sample edition "${sample.data.id}": sample data belongs in test fixtures only.`);
  }
  return entries.map((e) => e.data).sort((a, b) => b.compiledAt.localeCompare(a.compiledAt));
}

export async function latestEdition(): Promise<Edition | undefined> {
  return (await listEditions())[0];
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

// Calendar dates ("2026-10-21") are shown as written, without time-zone shifts.
export function formatDay(date: string, opts: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' }): string {
  return new Intl.DateTimeFormat('en-US', { ...opts, timeZone: 'UTC' }).format(new Date(`${date.slice(0, 10)}T12:00:00Z`));
}

export function storyUrl(base: string, story: Story): string {
  return `${base}stories/${story.id}/`;
}

export const PILLARS = {
  top: 'Top stories',
  foreign: 'Foreign Policy Desk',
  midterms: 'Midterms 2026',
  floor: 'Floor and committees',
  notable: 'Also notable',
} as const;

export const STATUS_LABEL = {
  verified: 'Verified',
  multiple: 'Multiple reports',
  unconfirmed: 'Unconfirmed',
} as const;

// Feedback (FT 8): a prefilled GitHub issue that the next run reads.
export function feedbackUrl(kind: 'error' | 'not-important', edition: Edition, story: Story): string {
  const title = kind === 'error' ? `Error: ${story.headline}` : `Less important: ${story.headline}`;
  const body = [
    `Edition: ${edition.id}`,
    `Story: ${story.id}`,
    '',
    kind === 'error' ? 'What is wrong, and where did you see the correct information?' : 'Why is this less important to you?',
    '',
  ].join('\n');
  const label = kind === 'error' ? 'feedback:error' : 'feedback:not-important';
  const q = new URLSearchParams({ title, body, labels: label });
  return `https://github.com/andreaskallenbach1/Congress-Terminal/issues/new?${q}`;
}
