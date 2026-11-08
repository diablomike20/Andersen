<p align="center">
  <img src="public/icon-512.png" width="128" height="128" alt="Andersen emblem">
</p>

<h1 align="center">Andersen</h1>

<p align="center">
  <strong>Creative Writing Studio</strong><br>
  <em>A home for stories worth telling.</em>
</p>

<p align="center">
  <a href="https://github.com/diablomike20/Andersen"><img src="https://img.shields.io/badge/GitHub-Andersen-181717?logo=github" alt="Andersen on GitHub"></a>
  <img src="https://img.shields.io/badge/Language-Hungarian%20(default)-white?labelColor=555" alt="Hungarian default">
  <img src="https://img.shields.io/badge/Platform-Web%20%7C%20PWA%20%7C%20Desktop-8B6B35" alt="Web, PWA and desktop">
  <img src="https://img.shields.io/badge/License-MIT-2E8B57" alt="MIT License">
</p>

---

**Andersen** is an open-source creative-writing environment for authors, storytellers and worldbuilders. It brings the pieces of a long-form creative project into one focused workspace: manuscript, characters, fictional worlds, plot structure, research, revision, and publishing.

The interface starts in **Hungarian**. English and the other supported languages remain available.

> [!NOTE]
> Andersen is the independent product identity of a continuation of the WorldScript Studio codebase. This repository preserves upstream technical identifiers where changing them would create unnecessary compatibility risks. The product name and user-facing experience are Andersen.

## The idea

Writing a book is more than filling pages. It means keeping track of people, places, timelines, motivations, plot threads, research, drafts and revisions—without losing sight of the story itself.

Andersen is built around the project as the author's source of truth. AI can assist, but it does not own the manuscript and is not required to use the core writing workspace.

## What you can do

- **Write and organize manuscripts** — work with structured sections and a dedicated writing surface.
- **Build story worlds** — maintain character dossiers, locations, world details and story-bible material.
- **Plan narratives** — develop plot structures, outlines, mind maps and character relationships.
- **Research and revise** — keep supporting material close to the project and work through revisions.
- **Use AI on your terms** — connect supported providers, use local/browser-based inference where available, or write without AI.
- **Track creative progress** — use project goals, progress views and planning tools.
- **Export and publish** — prepare work for supported export workflows.
- **Choose your workspace** — use the web application, installable PWA or Tauri desktop application.

Feature availability can vary by platform, configuration and maturity. Optional networked services require connectivity.

## Principles

### Your project comes first

The manuscript and project data are the central assets. AI output is assistance—not an authority that silently replaces the author's work.

### Local-first, with honest network boundaries

Core project workflows are designed around local project ownership. Some optional capabilities—such as cloud AI providers, collaboration services, language tools, model downloads and update checks—use the network. Review each integration before enabling it.

### AI is optional

Andersen remains a writing environment when no API key is configured, no provider is reachable, or AI features are turned off.

### Open development

The project is intended to be inspectable, extensible and welcoming to contributors. Clear documentation, reproducible checks and honest statements about feature maturity matter more than inflated claims.

## Getting started

### Use the application

The public standalone Andersen deployment and release downloads will be listed here when the new repository and its distribution channels are ready.

### Run from source

The project uses Node.js and pnpm. Check the exact versions in `package.json` before starting.

```bash
corepack enable
pnpm install
pnpm run dev
```

For a production web build:

```bash
pnpm run build
```

For the desktop development shell:

```bash
pnpm run tauri:dev
```

Some native build targets require the platform-specific Tauri toolchain. Installing dependencies or building the project is not performed by this README.

## Language

- Default interface language: **Hungarian**
- English and additional translations are included.
- Translation completeness does not automatically guarantee native-speaker editorial quality. Contributions to terminology, consistency and proofreading are welcome.

## Technology

The current codebase includes:

- React and TypeScript
- Vite
- Tauri 2 for the desktop shell
- A modular internationalization system
- Optional AI provider and local inference integrations

The exact dependency versions and available scripts are maintained in `package.json`.

## Contributing

Contributions are welcome. Before opening a pull request:

1. Read the repository's contribution and security guidance.
2. Explain the problem being solved and the intended user impact.
3. Keep changes focused and avoid unrelated refactors.
4. Include or update tests for behavior changes.
5. Do not commit API keys, credentials, private manuscripts or personal data.
6. Clearly identify any feature that is experimental, platform-limited or dependent on an external service.

For substantial changes, open an issue first so the direction can be discussed.

## Security and privacy

Do not report security vulnerabilities in public issues. Use the repository's private vulnerability reporting channel when available. Never include real API keys, tokens, personal information or private manuscript content in bug reports.

Andersen does not make the network disappear: when you choose a cloud provider or online integration, the information required by that service may leave your device. Consult the relevant provider's privacy terms and the project's security documentation.

## License

This project retains the license included in the source repository. See [LICENSE](LICENSE) for the complete terms.

---

<p align="center">
  <strong>Andersen</strong><br>
  <sub>Make room for the story.</sub>
</p>
