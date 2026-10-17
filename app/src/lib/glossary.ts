// Glossary (FT 7): fixed, checked definitions quoted from the U.S. Senate glossary.
import entries from '../data/glossary.json';

export interface GlossaryEntry { term: string; definition: string; source: string; url: string; retrieved: string }
export const glossary = (entries as GlossaryEntry[]).slice().sort((a, b) => a.term.localeCompare(b.term));
export const termId = (term: string) => term.toLowerCase().replace(/[^a-z0-9]+/g, '-');

// Longest terms first, so "joint resolution" wins over "resolution"-like shorter matches.
const byLength = glossary.slice().sort((a, b) => b.term.length - a.term.length);
const pattern = new RegExp(`\\b(${byLength.map((e) => e.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})s?\\b`, 'i');

export type Segment = { text: string } | { text: string; entry: GlossaryEntry };

// Splits text into plain parts and glossary hits; each term is marked once per story (tracked in `used`).
export function markTerms(text: string, used: Set<string>): Segment[] {
  const out: Segment[] = [];
  let rest = text;
  while (rest) {
    const m = rest.match(pattern);
    if (!m || m.index === undefined) { out.push({ text: rest }); break; }
    const entry = glossary.find((e) => e.term.toLowerCase() === m[1].toLowerCase())!;
    // Capitalised mid-sentence means a proper name ("Continuing Appropriations Act"), not the procedure.
    const atSentenceStart = /(^|[.!?:]\s+)$/.test(text.slice(0, text.length - rest.length) + rest.slice(0, m.index));
    const properName = m[0] !== m[0].toLowerCase() && !atSentenceStart;
    if (used.has(entry.term) || properName) {
      out.push({ text: rest.slice(0, m.index + m[0].length) });
    } else {
      used.add(entry.term);
      if (m.index > 0) out.push({ text: rest.slice(0, m.index) });
      out.push({ text: m[0], entry });
    }
    rest = rest.slice(m.index + m[0].length);
  }
  return out;
}
