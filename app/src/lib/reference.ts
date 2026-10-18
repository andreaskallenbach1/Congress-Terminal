// Member profiles and committees from open data (pipeline/reference.py): congress-legislators and Voteview.
import fs from 'node:fs';
import path from 'node:path';

export interface MemberProfile {
  bioguideId: string; name: string; party: 'R' | 'D' | 'I'; state: string; chamber: 'senate' | 'house';
  district: number | null; since: string; website?: string;
  committees: { committee: string; id: string; title: string | null }[];
  nominate: number | null;
}
export interface Committee {
  id: string; name: string; chamber: 'house' | 'senate' | 'joint'; url?: string; jurisdiction?: string;
  chair: { bioguide: string; name: string } | null; ranking: { bioguide: string; name: string } | null; members: number;
}

const DATA = path.resolve(process.cwd(), '..', 'data');
const read = <T>(file: string, fallback: T): T => {
  const p = path.join(DATA, file);
  return fs.existsSync(p) ? (JSON.parse(fs.readFileSync(p, 'utf8')) as T) : fallback;
};

export const memberProfiles = new Map(read<MemberProfile[]>('members.json', []).map((m) => [m.bioguideId, m]));
export const committees = read<Committee[]>('committees.json', []);

export interface WatchedBill {
  number: string; title: string; congressGovUrl: string;
  stages: { key: string; label: string; date?: string; done: boolean; setback: boolean }[];
  latestAction: { date: string; text: string } | null; story: string; edition: string;
}
// Watchlist (FT 5), refreshed from the Congress.gov API on every run (pipeline/watchlist.py).
export const watchlist = read<WatchedBill[]>('watchlist.json', []);
