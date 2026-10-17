# Briefings

The pipeline writes one JSON file per edition into this folder (for example `2026-10-19-daily.json`).
The web app reads every file here at build time. Agents write only into this folder.
The full schema is fixed in build step 3; the app currently needs `id`, `kind`, `date` and `compiledAt`.
