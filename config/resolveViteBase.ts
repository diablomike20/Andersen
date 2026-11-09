// QNBS-v3: Single source for Vite `base`. Extracted from vite.config.ts so the Tauri-detection
// regression is permanently unit-tested: a desktop build that fell through to the GitHub Pages base
// ('/Andersen/') 404'd every hashed asset under tauri://localhost/ → blank webview (only the
// native file/help menu rendered). Root cause was checking the Tauri 1.x env var name.

export const GITHUB_PAGES_BASE = '/Andersen/';

// QNBS-v3: local dev default — a plain `pnpm run dev` (no launcher, no VITE_BASE) serves /Andersen/; production builds keep GITHUB_PAGES_BASE so the CI GitHub Pages deploy (NODE_ENV=production, no VITE_BASE) is unaffected.
export const LOCAL_DEV_BASE = '/Andersen/';

/**
 * True when the active `vite build` is the one Tauri's `beforeBuildCommand` hook invokes to
 * produce the desktop bundle, as opposed to the web/PWA build.
 *
 * QNBS-v3: Tauri 2.x sets TAURI_ENV_PLATFORM for hook commands; the legacy Tauri 1.x name was
 * TAURI_PLATFORM. Accept both so a CLI downgrade/upgrade can't silently reintroduce a
 * platform-detection regression. Single source of truth — reused by both the `base` resolution
 * below and `vite.config.ts`'s `rollupOptions.external` (a desktop build that externalized
 * `@tauri-apps/*` left an unresolvable bare module specifier in the shipped bundle; see
 * docs/adr/0012-local-server-connectivity-tauri-http.md).
 */
export function isTauriBuild(env: Record<string, string | undefined> = process.env): boolean {
  // QNBS-v3: require a trimmed, non-empty value — an empty-string env var (e.g. a CI matrix
  // that sets TAURI_ENV_PLATFORM="" to "unset" it) must not be read as "Tauri build".
  return Boolean(env['TAURI_ENV_PLATFORM']?.trim()) || Boolean(env['TAURI_PLATFORM']?.trim());
}

/**
 * Resolve the Vite `base` for the active build target.
 * - Tauri desktop  → './'  (relative; assets must load from tauri://localhost/ root)
 * - explicit VITE_BASE → normalised with a trailing slash
 * - edge (Vercel/Cloudflare root domain) → '/'
 * - local dev default (NODE_ENV !== 'production') → '/Andersen/'
 * - production build default (GitHub Pages project page) → '/Andersen/'
 */
export function resolveViteBase(env: Record<string, string | undefined> = process.env): string {
  if (isTauriBuild(env)) {
    return './';
  }
  const viteBase = env['VITE_BASE']?.trim();
  if (viteBase) {
    return viteBase.endsWith('/') ? viteBase : `${viteBase}/`;
  }
  if (env['DEPLOY_TARGET'] === 'edge') {
    return '/';
  }
  return env['NODE_ENV'] === 'production' ? GITHUB_PAGES_BASE : LOCAL_DEV_BASE;
}
