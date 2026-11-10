# Changelog

All notable changes to Andersen are documented in this file.

## [Unreleased]

### Fixed

- Converted the Tauri bundle icons to RGBA so the Linux Rust compile gate can generate the app context.

## [1.29.3] - 2026-11-10
<!-- release-candidate: v1.29.3 -->

### Added

- Unsloth Studio as a local model provider: the new `unsloth` preset targets its OpenAI-compatible server at `http://localhost:8888`, appears in the local endpoint scan, and stores its bearer key in the encrypted local key store.
- The settings AI card exposes the Unsloth API-key field and sends the stored key with discovery and generation requests.

### Changed

- Local OpenAI-compatible providers can authenticate with a bearer token resolved at request time; the token is never persisted in settings.
- The Tauri CSP allowlist now includes `http://localhost:8888` and `http://127.0.0.1:8888`.

### Fixed

- The updater manifest notes are encoded safely for GitHub raw hosting.
- Restored the security, encryption, secure-storage, and core-migration documentation required by the CI gates.
- TypeScript checks ignore the local Tauri build output under `src-tauri/target`.

## [1.29.2] - 2026-11-09

### Added

- Windows desktop release: the Tauri app now opens in its own native window, with NSIS and MSI installers.
- A portable downloader (`Letoltes.bat` / `Letoltes.ps1`) in the launcher that fetches the latest GitHub release installer and verifies its SHA-256 digest.

### Changed

- Rebranded the product as **Andersen**.
- Pointed repository, GitHub Pages, updater, documentation, and in-app links to `https://github.com/diablomike20/Andersen`.
- The Windows binary is now built as `Andersen.exe`.
