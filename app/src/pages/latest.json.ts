// Id of the published edition; the "Update now" display polls it to know when a new edition is live.
import { latestEdition } from '../lib/editions';

export async function GET() {
  const e = await latestEdition();
  return new Response(JSON.stringify(e ? { id: e.id, kind: e.kind, compiledAt: e.compiledAt } : {}), {
    headers: { 'Content-Type': 'application/json' },
  });
}
