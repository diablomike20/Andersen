<div align="center">

<a href="https://github.com/diablomike20/Andersen">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-hero.svg" alt="Andersen — Ne csak történeteket írj. Teremts világokat." width="100%">
</a>

<br>

<img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-emblem.svg" alt="Andersen embléma" width="76">

# ANDERSEN LAUNCHER

### A műhely kapuja. Nem maga a műhely.

<p><em>Egy apró ajtó egy nagy alkotói világhoz.</em></p>

[![Windows](https://img.shields.io/badge/WINDOWS-172A42?style=flat-square&labelColor=091321)](https://www.microsoft.com/windows)
![PowerShell](https://img.shields.io/badge/POWERSHELL-172A42?style=flat-square&labelColor=091321)
![Magyar felület](https://img.shields.io/badge/MAGYAR_FELÜLET-C9A96E?style=flat-square&labelColor=091321)
[![Launcher branch](https://img.shields.io/badge/BRANCH-Launcher_Design_V1-172A42?style=flat-square&labelColor=091321)](https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1)

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

A launcher a legfontosabb fejlesztői műveleteket rendezi egyetlen felületre. Elindítás előtt ellenőrzi az alapvető környezetet, a hiányzó függőségekre figyelmeztet, a kiválasztott feladatot pedig külön PowerShell-ablakban futtatja.

<div align="center">

| **01 · ELŐKÉSZÍTÉS** | **02 · MEGNYITÁS** | **03 · ALKOTÁS** | **04 · ÉPÍTÉS** |
|:--:|:--:|:--:|:--:|
| Környezetellenőrzés | Launcher indítása | Fejlesztői mód | Build készítése |

</div>

### A választható műveletek

| Művelet | Parancs | Cél |
|:--|:--|:--|
| **Webes fejlesztői mód** | <code>pnpm run dev</code> | Az Andersen webes felületének helyi fejlesztése. |
| **Asztali alkalmazás** | <code>pnpm run tauri:dev</code> | A Tauri-alapú asztali változat fejlesztői indítása. |
| **Függőségek telepítése** | <code>pnpm install</code> | A projekt szükséges csomagjainak telepítése. |
| **Webes build készítése** | <code>pnpm run build</code> | A webes build előállítása. |
| **GitHub-tárház megnyitása** | — | Az Andersen forráskódjának megnyitása. |

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

A launcher önmagában nem tartalmazza az alkalmazás forráskódját. Először klónozd vagy töltsd le a teljes [Andersen repositoryt](https://github.com/diablomike20/Andersen).

**02 — Helyezd el a launcher fájljait**

A Launcher_Design_V1 branch három fájlját másold a teljes projekt megfelelő helyére. A meglévő projektfájlokat ne írd felül.

**03 — Nyisd meg a műhelyt**

Indítsd el dupla kattintással a Start-Andersen.bat fájlt, majd válaszd ki a kívánt műveletet.

### A teljes projektben így nézzen ki

```text
Andersen/                              ← a teljes alkalmazás projektje
├── package.json
├── Start-Andersen.bat                 ← launcher belépési pont
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1      ← grafikus indítófelület
```

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

## Amire szükséged lesz

| Összetevő | Követelmény |
|:--|:--|
| Operációs rendszer | Windows |
| PowerShell | Windows PowerShell 5.1 vagy újabb |
| Node.js | 22.19.0 vagy újabb |
| Csomagkezelő | Corepack vagy pnpm |
| Projektben rögzített pnpm | 12.13.0 |
| Asztali fejlesztés | A Tauri Windowsos előfeltételei |

A launcher ellenőrzi a Node.js és a pnpm elérhetőségét, valamint a függőségek meglétét. Ha a node_modules könyvtár hiányzik, felajánlja a telepítést.

## Egy fontos különbség

Ez a repository-ág **launcher-only csomag**. Nem az Andersen teljes alkalmazása, nem tartalmazza annak forráskódját, és nem telepíti automatikusan a Node.js-t vagy a Tauri rendszerkövetelményeit.

A launcher a fejlesztői parancsok indítására szolgál. A parancsok kimenete külön PowerShell-ablakban marad látható, így a hibák és a folyamat állapota követhető.

## A csomag tartalma

```text
Launcher_Design_V1/
├── README.md
├── Start-Andersen.bat
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1
```

A szándékos egyszerűség itt fontos: ez a branch csak azt tartalmazza, ami a launcher működéséhez és bemutatásához szükséges.

## Közreműködés

Az Andersen egy alkotói projekt — örömmel fogadjuk az átgondolt és építő hozzájárulásokat. A launcherrel kapcsolatos módosításokat tartsd elkülönítve az alkalmazás többi részétől. Hibajelentésben ne ossz meg API-kulcsot, tokent vagy más bizalmas adatot.

A használatra az Andersen repository licencfeltételei vonatkoznak: [LICENSE](https://github.com/diablomike20/Andersen/blob/main/LICENSE).

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

<div align="center">

<img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-emblem.svg" alt="Andersen embléma" width="88">

## ANDERSEN

### Ne csak történeteket írj. Teremts világokat.

<em>Nyisd ki a műhelyt. A történetet te írod.</em>

<br>

[**Andersen — fő repository**](https://github.com/diablomike20/Andersen)
&nbsp; · &nbsp;
[**Launcher branch**](https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1)

<sub>MADE FOR THE LOVE OF STORIES, BOOKS & CREATION</sub>

</div>
