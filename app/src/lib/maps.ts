// Build-time map geometry (no map code runs in the browser). Natural Earth via world-atlas, US Census via us-atlas.
import { geoEqualEarth, geoPath } from 'd3-geo';
import { feature, mesh } from 'topojson-client';
import { presimplify, simplify } from 'topojson-simplify';
import world from 'world-atlas/countries-110m.json';
import usRaw from 'us-atlas/states-albers-10m.json';

// The 10m state outlines are far more detailed than a 975-px map needs; simplify once at build time.
const us = simplify(presimplify(usRaw as any), 1.5);

export interface MapShape { name: string; d: string }
export interface MapMarker { n: number; name: string; x: number; y: number }

const W = 960, H = 470;
const countries = (feature(world as any, (world as any).objects.countries) as any).features as any[];
const projection = geoEqualEarth().fitExtent([[4, 4], [W - 4, H - 4]], { type: 'Sphere' } as any);
const worldPath = geoPath(projection).digits(0);

export const worldMap = {
  width: W,
  height: H,
  shapes: countries.filter((f) => f.properties.name !== 'Antarctica').map((f) => ({ name: f.properties.name as string, d: worldPath(f) ?? '' })),
  borders: worldPath(mesh(world as any, (world as any).objects.countries, (a: any, b: any) => a !== b) as any) ?? '',
};

export function worldMarkers(names: string[]): { markers: MapMarker[]; missing: string[] } {
  const markers: MapMarker[] = [], missing: string[] = [];
  names.forEach((name, i) => {
    const f = countries.find((c) => c.properties.name === name);
    if (!f) { missing.push(name); return; }
    const [x, y] = name === 'United States of America' ? projection([-98, 39])! : worldPath.centroid(f);
    markers.push({ n: i + 1, name, x, y });
  });
  return { markers, missing };
}

const states = (feature(us as any, (us as any).objects.states) as any).features as any[];
const usPath = geoPath(null).digits(0);

export const usMap = {
  width: 975,
  height: 610,
  shapes: states.map((f) => ({ name: f.properties.name as string, d: usPath(f) ?? '' })),
  borders: usPath(mesh(us as any, (us as any).objects.states, (a: any, b: any) => a !== b) as any) ?? '',
};

export function usMarkers(names: string[]): { markers: MapMarker[]; missing: string[] } {
  const markers: MapMarker[] = [], missing: string[] = [];
  names.forEach((name, i) => {
    const f = states.find((s) => s.properties.name === name);
    if (!f) { missing.push(name); return; }
    const [x, y] = usPath.centroid(f);
    markers.push({ n: i + 1, name, x, y });
  });
  return { markers, missing };
}
