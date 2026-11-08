# Andersen Launcher for Windows

A lightweight Windows launcher styled after the Andersen README identity: midnight navy, antique gold, bookish typography and restrained ornamental framing.

## Start

Double-click **Start-Andersen.bat** in the repository root.

The launcher is separate from the application runtime. It does not modify application source, configuration, credentials, or project data.

## Actions

- **Webes fejlesztői mód** — runs `pnpm run dev`.
- **Asztali alkalmazás** — runs `pnpm run tauri:dev`.
- **Függőségek telepítése** — runs `pnpm install`.
- **Webes build készítése** — runs `pnpm run build`.
- **Repository megnyitása** — opens the GitHub repository.

Each task runs in its own PowerShell window so logs remain visible.

## Requirements

- Windows PowerShell 5.1 or newer.
- Node.js **22.19.0 or newer**.
- Corepack / pnpm. The repository pins **pnpm 12.13.0** in `package.json`.
- For the desktop target, install the platform prerequisites documented by Tauri.

The launcher checks the local toolchain and reports detected versions. It does not silently install runtimes or change machine-wide settings.

## Files

- `Start-Andersen.bat` — double-click entry point.
- `tools/launcher/Andersen-Launcher.ps1` — graphical launcher.
- `tools/launcher/README.md` — this guide.

The first run may offer to install project dependencies when `node_modules` is missing. The app's own predev/build scripts remain responsible for normal preparation steps.
