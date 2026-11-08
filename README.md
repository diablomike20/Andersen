<div align="center">

<a href="https://github.com/diablomike20/Andersen">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-hero.svg" alt="Andersen — Ne csak történeteket írj. Teremts világokat." width="100%">
</a>

# ANDERSEN LAUNCHER

### A műhely kapuja. Nem maga a műhely.

<p><em>Egy apró ajtó egy nagy alkotói világhoz.</em></p>

[![Windows](https://img.shields.io/badge/WINDOWS-172A42?style=flat-square&labelColor=091321)](https://www.microsoft.com/windows)
![Python 3.10+](https://img.shields.io/badge/PYTHON_3.10%2B-172A42?style=flat-square&labelColor=091321)
![Magyar felület](https://img.shields.io/badge/MAGYAR_FELÜLET-C9A96E?style=flat-square&labelColor=091321)
[![Launcher branch](https://img.shields.io/badge/BRANCH-Launcher-172A42?style=flat-square&labelColor=091321)](https://github.com/diablomike20/Andersen/tree/Launcher)

</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

<div align="center">

## Minden történet valahol elkezdődik.

</div>

Az Andersen azoknak készül, akik nem csupán szöveget szeretnének írni, hanem karaktereket, helyeket, emlékeket és egész világokat akarnak életre kelteni.

Ehhez az alkotáshoz készült ez a launcher: **egy gondosan kialakított, magyar nyelvű indítófelület, amely segít megnyitni a fejlesztői műhelyt.**

Nem akar többnek látszani annál, ami. Nem maga az alkotói alkalmazás, és nem helyettesíti annak teljes forráskódját. A feladata az, hogy az indulás egyszerű, átlátható és kényelmes legyen — hogy hamarabb juthass el oda, ami igazán számít: az alkotáshoz.

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-writing-oath.svg" alt="Az Andersen írásművészetet idéző könyvészeti illusztrációja" width="100%">
</p>

<p align="center"><em>„A történetek nem készen várnak ránk. Mi teremtjük meg őket.”</em></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

## A műhely bejárata

A launcher egyetlen felületen fogja össze a mindennapi fejlesztői műveleteket. Indítás előtt ellenőrzi a Git, a Node.js és a pnpm/corepack meglétét, figyeli a forrásmappát és a 3000-es portot, a folyamatok kimenetét pedig a beépített naplóban jeleníti meg.

<div align="center">

| **01 · ELLENŐRZÉS** | **02 · INDÍTÁS** | **03 · ALKOTÁS** | **04 · FRISSÍTÉS** |
|:--:|:--:|:--:|:--:|
| Környezet és forrás | Fejlesztői szerver | Böngészőben nyílik | Git pull + pnpm |

</div>

### A választható műveletek

| Művelet | Mit csinál? |
|:--|:--|
| **INDÍTÁS / MEGNYITÁS** | Elindítja a webes fejlesztői szervert (`pnpm run dev`), majd megnyitja a böngészőt a `http://127.0.0.1:3000/Andersen/` címen. |
| **Asztali mód** | A Tauri asztali alkalmazást indítja (`pnpm run tauri:dev`). Az első indítás Rust-fordítás miatt hosszabb lehet. |
| **Frissítés** | `git pull --ff-only` + `pnpm install`. Csak tiszta munkakönyvtárnál frissít. |
| **Leállítás** | Leállítja a futó szervert vagy telepítést. |
| **Mappa** | Megnyitja a forrásmappát az Intézőben. |
| **Újraellenőrzés** | Újra ellenőrzi a Git, Node.js, pnpm, forrás és port állapotát. |
| **Módosítás** | Másik forrásmappa kiválasztása. Üres mappa esetén oda tölti le az Andersent. |

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-creative-journey.svg" alt="Az Andersen alkotói folyamatát bemutató illusztráció" width="100%">
  <sub>Az alkotói út hangulati illusztrációja — nem a launcher kezelőfelületének képernyőképe.</sub>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

## Az első indítás

<div align="center">

### Három lépés. És nyitva a műhely.

</div>

**01 — Legyen meg a teljes Andersen projekt**

A launcher önmagában nem tartalmazza az alkalmazás forráskódját. Először klónozd vagy töltsd le a teljes [Andersen repositoryt](https://github.com/diablomike20/Andersen):

```bash
git clone https://github.com/diablomike20/Andersen.git
```

**02 — Klónozd a launchert külön mappába**

A launcher szándékosan külön mappában él, hogy a `git pull` ne írja felül:

```bash
git clone --branch Launcher --single-branch https://github.com/diablomike20/Andersen.git AndersenLauncher
```

**03 — Indítsd el**

Nyisd meg az `AndersenLauncher` mappában a `Start-Andersen.bat` fájlt (látható konzollal), vagy az `Inditas.vbs` fájlt (konzolablak nélkül).

Az első indításkor a launcher megkeresi az Andersen forrásmappáját. Alapértelmezésben a `%USERPROFILE%\Andersen` mappát használja; ha máshol van, a **Módosítás** gombbal választhatod ki. Ha a függőségek még hiányoznak, a launcher felajánlja a telepítést.

### A launcher mappája így nézzen ki

```text
AndersenLauncher/
├── Start-Andersen.bat        ← indítás látható konzollal (hibakereséshez)
├── Inditas.vbs               ← indítás konzolablak nélkül
├── andersen_launcher.py      ← a grafikus launcher
├── create_shortcut.ps1       ← asztali parancsikon készítése
├── assets/
│   ├── andersen-icon.ico
│   ├── andersen-icon.png
│   └── andersen-emblem.png
└── tools/
    └── make_assets.py
```

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

## Amire szükséged lesz

| Összetevő | Követelmény |
|:--|:--|
| Operációs rendszer | Windows 10/11 |
| Python | 3.10 vagy újabb, `tkinter` támogatással |
| Képkezelés | `Pillow` (opcionális — az embléma megjelenítéséhez) |
| Node.js | 22.19.0 vagy újabb |
| Csomagkezelő | Corepack vagy pnpm |
| Projektben rögzített pnpm | 12.13.0 |
| Git | a forrás letöltéséhez és a frissítéshez |
| Asztali fejlesztés | a Tauri Windowsos előfeltételei (Rust, WebView2) |

A launcher a `corepack pnpm` parancsot használja, így nem kell globálisan telepíteni a pnpm-et. A Python és a Node.js telepítése nem része a launchernek.

## Jó tudni

- A fejlesztői szerver az **`/Andersen/`** útvonalon szolgál ki; a launcher `VITE_BASE=/Andersen/` beállítással indítja.
- Az első betöltésnél a Vite előkészíti a modulokat, ilyenkor néhány másodpercig csak az **Andersen** betöltőképernyő látszik.
- Az upstream projekt `predev` lépése megköveteli az `AGENTS.md` fájlt, amely a repóban nem található. A launcher szükség esetén létrehoz egy megjelölt placeholdert, és frissítés előtt eltávolítja azt.
- A `predev` a `public/locales/*/bundle.json` fájlokat is újragenerálja; a launcher frissítés előtt visszaállítja ezeket, hogy a `git pull` ne akadjon el.
- A `launcher_config.json` helyi beállításokat tartalmaz, ezért nincs a repóban. A launcher első indításkor hozza létre.

## Egy fontos különbség

Ez a repository-ág **launcher-only csomag**. Nem az Andersen teljes alkalmazása, nem tartalmazza annak forráskódját, és nem telepíti automatikusan a Node.js-t vagy a Tauri rendszerkövetelményeit.

A launcher a fejlesztői parancsok indítására szolgál. A parancsok kimenete a launcher naplójában követhető; a `Start-Andersen.bat` használatakor külön konzolablakban is látható.

## Közreműködés

Az Andersen egy alkotói projekt — örömmel fogadjuk az átgondolt és építő hozzájárulásokat. A launcherrel kapcsolatos módosításokat tartsd elkülönítve az alkalmazás többi részétől. Hibajelentésben ne ossz meg API-kulcsot, tokent vagy más bizalmas adatot.

A használatra az Andersen repository licencfeltételei vonatkoznak: [LICENSE](https://github.com/diablomike20/Andersen/blob/main/LICENSE).

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

### Ne csak történeteket írj. Teremts világokat.

<em>Nyisd ki a műhelyt. A történetet te írod.</em>

<br>

[**Andersen**](https://github.com/diablomike20/Andersen)
&nbsp; · &nbsp;
[**Launcher**](https://github.com/diablomike20/Andersen/tree/Launcher)

<sub>MADE FOR THE LOVE OF STORIES, BOOKS & CREATION</sub>

</div>
