/**
 * Centralized product identity — the single source for the display name and the file-name slug.
 *
 * QNBS-v3: brand strings are intentionally NOT in the i18n catalog. A product name is identical
 * across every locale and must never be accidentally translated (or drift between components).
 * Prefer these constants over hardcoding `'Andersen'` / `'andersen'` in components.
 */
export const APP_NAME = 'Andersen';

/** Lowercase, filesystem-safe slug for generated artefacts (download filenames, key prefixes). */
export const APP_FILE_SLUG = 'andersen';

// QNBS-v3 (F-10): single source of truth for the canonical, live production URL. Andersen is
// published as a GitHub Pages project site under /Andersen/; every in-app or documentation link
// must match this value.
export const PRODUCTION_URL = 'https://diablomike20.github.io/Andersen/';
