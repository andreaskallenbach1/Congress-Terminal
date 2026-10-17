// Edition schema (version 1). Every briefing file in /briefings must match it, or the build fails:
// this is the machine check of pipeline stage 7 for structure. Hard facts (votes, bill numbers,
// dates, member names) are filled by code from primary data; agents must not change them.
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const briefingsDir = process.env.BRIEFINGS_DIR ?? '../briefings';

const status = z.enum(['verified', 'multiple', 'unconfirmed']);

const source = z.object({
  id: z.string(),
  name: z.string(),                       // "Congress.gov", "Reuters (via Google News)"
  tier: z.enum(['primary', 'agency', 'media', 'partisan-left', 'partisan-right', 'international', 'specialist', 'elections', 'video']),
  url: z.string().url(),
  retrievedAt: z.string(),                // ISO timestamp
});

const claim = z.object({
  id: z.string(),
  text: z.string(),
  weight: z.enum(['core', 'minor']),
  status,
  origin: z.enum(['code', 'agent']),      // "code" = taken directly from primary data
  evidence: z.array(z.object({
    sourceId: z.string(),
    quote: z.string(),                    // verbatim quote, found in the source text by code
    url: z.string().url(),
  })).min(1),
  checkA: z.enum(['confirmed', 'rejected']).optional(),
  checkB: z.enum(['confirmed', 'rejected']).optional(),
});

// Paragraphs are plain text; "[[c3]]" after a sentence attaches claim c3 and shows its status.
const paragraphs = z.array(z.string());

const image = z.object({
  src: z.string(),
  alt: z.string(),
  credit: z.string(),                     // "Carol M. Highsmith, Library of Congress"
  license: z.string(),                    // "No known restrictions", "Public domain", "Unsplash License"
  sourceUrl: z.string().url(),
});

const stage = z.object({
  key: z.enum(['introduced', 'committee', 'passed-house', 'passed-senate', 'resolved', 'to-president', 'signed', 'vetoed', 'waived', 'other']),
  label: z.string(),
  date: z.string().optional(),
  done: z.boolean(),
  setback: z.boolean().default(false),    // drawn in red: veto, waiver, failed vote
});

const bill = z.object({
  number: z.string(),                     // "H.R. 6500"
  title: z.string(),
  congressGovUrl: z.string().url(),
  stages: z.array(stage).min(1),
});

const race = z.object({
  state: z.string(),                      // "Maine"
  chamber: z.enum(['senate', 'house', 'governor']),
  district: z.string().optional(),        // "10th District"
  rating: z.string().optional(),
  ratingSource: z.string().optional(),
});

const story = z.object({
  id: z.string(),                         // stable across editions for follow-ups
  pillar: z.enum(['top', 'foreign', 'midterms', 'floor', 'notable']),
  continuing: z.boolean().default(false), // follow-up of an earlier story
  headline: z.string(),
  dek: z.string(),                        // one-sentence summary under the headline
  whatsNew: paragraphs,
  whyItMatters: paragraphs,
  whatsNext: paragraphs,
  background: paragraphs.optional(),      // expandable, not counted in reading time
  words: z.number().int().positive(),
  readingMinutes: z.number().positive(),
  status,                                 // weakest status among the core claims
  claims: z.array(claim).min(1),
  image: image.optional(),
  members: z.array(z.object({ bioguideId: z.string(), name: z.string(), party: z.enum(['R', 'D', 'I']), state: z.string() })).default([]),
  bill: bill.optional(),
  race: race.optional(),
  countries: z.array(z.string()).default([]),   // Natural Earth names (world-atlas), for the Foreign Policy map
  relevance: z.object({
    rank: z.number().int().positive(),
    reason: z.string(),
    dissent: z.string().optional(),       // counter-agent objection, shown expandable
  }),
});

const partyCount = z.object({ yea: z.number().int(), nay: z.number().int(), present: z.number().int().default(0), notVoting: z.number().int() });

const vote = z.object({
  chamber: z.enum(['senate', 'house']),
  rollCall: z.number().int(),
  date: z.string(),
  question: z.string(),                   // "On the Nomination"
  description: z.string(),                // "Confirmation of Keith Sonderling as Secretary of Labor"
  result: z.string(),                     // "Confirmed"
  byParty: z.object({ R: partyCount, D: partyCount, I: partyCount }),
  sourceUrl: z.string().url(),
});

const agendaItem = z.object({
  date: z.string(),
  time: z.string().optional(),
  chamber: z.enum(['senate', 'house', 'joint']),
  kind: z.enum(['floor', 'hearing', 'markup', 'deadline', 'other']),
  title: z.string(),
  committee: z.string().optional(),
  url: z.string().url().optional(),
});

const clip = z.object({
  title: z.string(),
  channel: z.string(),                    // "C-SPAN (YouTube)"
  date: z.string(),
  url: z.string().url(),
  startSeconds: z.number().int().nonnegative(),
  why: z.string(),
  thumbnail: z.string().optional(),
});

const notable = z.object({ headline: z.string(), sentence: z.string(), outlet: z.string(), url: z.string().url() });

const armsSale = z.object({
  purchaser: z.string(),
  system: z.string(),
  valueUSD: z.number().nonnegative(),
  date: z.string(),
  url: z.string().url(),
});

// Title image of an edition: chosen for the lead story where a fitting licensed image exists,
// otherwise a symbolic photo of the Capitol or Congress from a curated library.
const hero = image.extend({
  relation: z.enum(['story', 'symbolic']),
  caption: z.string(),                    // what the image shows, in one line
});

const briefings = defineCollection({
  loader: glob({ pattern: '*.json', base: briefingsDir }),
  schema: z.object({
    schemaVersion: z.literal(1),
    sample: z.boolean().default(false),   // true only for test fixtures; never published
    id: z.string(),
    kind: z.enum(['daily', 'weekly']),
    date: z.string(),
    compiledAt: z.string(),
    readingMinutes: z.number().positive(),
    hero: hero.optional(),
    stories: z.array(story),
    floor: z.object({ votes: z.array(vote), summary: z.string().optional() }),
    agenda: z.array(agendaItem),          // next seven days
    overnight: z.array(z.string()).default([]),
    today: z.array(z.string()).default([]),
    armsSales: z.array(armsSale).default([]),
    watch: z.array(clip).default([]),
    notable: z.array(notable).default([]),
    sources: z.array(source),
    process: z.object({
      sourcesChecked: z.number().int(),
      claimsChecked: z.number().int(),
      objections: z.number().int(),
      objectionsAccepted: z.number().int(),
    }),
  }),
});

export const collections = { briefings };
