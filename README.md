<div align="center">

<p>
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-emblem.svg" alt="Andersen embléma" width="112">
</p>

# ANDERSEN
## LAUNCHER

### A műhely kapuja. Nem maga a műhely.

**A fejlesztői környezeted egyetlen, áttekinthető indítófelületen.**

<sub>WINDOWS&nbsp; · &nbsp;POWERSHELL&nbsp; · &nbsp;MAGYAR FELÜLET</sub>

<br>

<a href="https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1"><img src="https://img.shields.io/badge/BRANCH-Launcher_Design_V1-172A42?style=for-the-badge&labelColor=0A1220" alt="Launcher Design V1"></a>
<img src="https://img.shields.io/badge/PLATFORM-WINDOWS-172A42?style=for-the-badge&labelColor=0A1220" alt="Windows">
<img src="https://img.shields.io/badge/INTERFACE-MAGYAR-D6B36D?style=for-the-badge&labelColor=0A1220" alt="Magyar felület">

<br><br>

<table>
  <tr>
    <td align="center" width="25%"><strong>01</strong><br><sub>ELŐKÉSZÍTÉS</sub></td>
    <td align="center" width="25%"><strong>02</strong><br><sub>INDÍTÁS</sub></td>
    <td align="center" width="25%"><strong>03</strong><br><sub>FEJLESZTÉS</sub></td>
    <td align="center" width="25%"><strong>04</strong><br><sub>BUILD</sub></td>
  </tr>
</table>

<sub>AZ ÖTLETTŐL A FUTTATHATÓ FEJLESZTŐI KÖRNYEZETIG</sub>

</div>

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## A launcher szerepe

Az Andersen egy alkotói műhely. Ez a launcher a fejlesztői műhely bejárata: nem maga az alkalmazás, hanem egy célzott vezérlőfelület, ahonnan a legfontosabb fejlesztői műveletek indíthatók.

A felület feladata egyszerű: ellenőrizni az alapvető környezetet, jelezni, ha valami hiányzik, és egyértelművé tenni, melyik munkafolyamatot szeretnéd elindítani.

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-start-here.svg" alt="Az Andersen projekt elindításának vizuális útmutatója" width="100%">
</p>

<p align="center"><sub>ELŐKÉSZÍTÉS → INDÍTÁS → ALKOTÁS → ELLENŐRZÉS</sub></p>

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Műveleti központ

| Művelet | Parancs / cél | Mire való? |
|:--|:--|:--|
| **WEBES FEJLESZTŐI MÓD** | `pnpm run dev` | A webes felület fejlesztése és helyi futtatása. |
| **ASZTALI ALKALMAZÁS** | `pnpm run tauri:dev` | A Tauri-alapú asztali alkalmazás fejlesztői indítása. |
| **FÜGGŐSÉGEK TELEPÍTÉSE** | `pnpm install` | A projekt függőségeinek telepítése. |
| **WEBES BUILD KÉSZÍTÉSE** | `pnpm run build` | A webes build előállítása. |
| **GITHUB-TÁRHÁZ MEGNYITÁSA** | Andersen repository | A forráskód és a fejlesztési anyagok megnyitása. |

### Környezetellenőrzés

A launcher ellenőrzi a Node.js- és pnpm-környezetet, megjeleníti az észlelt verziókat, és hiányzó `node_modules` könyvtár esetén felajánlja a függőségek telepítését. A fejlesztői parancsokat külön PowerShell-ablakban indítja, így a futási kimenet és az esetleges hibák láthatók maradnak.

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Indítás — három lépésben

<div align="center">

| <sub>01 · HELYEZD EL</sub> | <sub>02 · INDÍTSD EL</sub> | <sub>03 · VÁLASSZ</sub> |
|:--:|:--:|:--:|
| Másold a launcher fájljait a teljes Andersen projekt gyökerébe. | Kattints duplán a `Start-Andersen.bat` fájlra. | Válaszd ki a kívánt fejlesztői műveletet. |

</div>

### A szükséges mappaszerkezet

Ez a branch szándékosan **launcher-only**: nem tartalmazza az Andersen alkalmazás forráskódját. A teljes Andersen repositoryra szükséged van.

```text
Andersen/                         ← a teljes projekt mappája
├── package.json                  ← az alkalmazás projektbeállításai
├── Start-Andersen.bat            ← launcher belépési pont
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1 ← grafikus felület
```

A három launcherfájlt a teljes projekt megfelelő helyére másold át. A meglévő projektfájlokat ne írd felül.

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Rendszerkövetelmények

| Összetevő | Elvárás |
|:--|:--|
| Operációs rendszer | Windows |
| PowerShell | Windows PowerShell 5.1 vagy újabb |
| Node.js | 22.19.0 vagy újabb |
| Csomagkezelő | Corepack / pnpm |
| Projektben rögzített pnpm | 12.13.0 |
| Tauri | Az asztali fejlesztéshez szükséges Windowsos előfeltételek |

A projekt pontos parancsait és verzióit a teljes Andersen repository `package.json` fájlja határozza meg.

## A launcher határai

- **Nem önálló Andersen-alkalmazás:** a teljes projekt megléte szükséges.
- **Nem helyettesíti a projektet:** a `package.json` és az alkalmazás forráskódja a teljes repository része.
- **Nem rejti el a parancsok kimenetét:** a fejlesztői műveletek külön PowerShell-ablakban futnak.
- **Nem módosítja a fő alkalmazást:** a launcher a fejlesztői parancsok indítására szolgál.

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## A branch tartalma

```text
Launcher_Design_V1/
│
├── README.md
│   └── Ez az útmutató
│
├── Start-Andersen.bat
│   └── Windows belépési pont
│
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1
            └── Magyar nyelvű grafikus launcher
```

A branch célja, hogy a launcher önállóan áttekinthető és a teljes Andersen projekthez egyszerűen hozzáadható legyen.

## Közreműködés és licenc

A launcher módosításait tartsd elkülönítve az Andersen alkalmazás többi részétől. Hibajelentésben ne szerepeljen API-kulcs, token vagy más bizalmas adat.

A használatra az Andersen repository licencfeltételei vonatkoznak: [LICENSE](https://github.com/diablomike20/Andersen/blob/main/LICENSE).

---

<div align="center">

<img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-emblem.svg" alt="Andersen embléma" width="64">

**ANDERSEN LAUNCHER**

<em>Nyisd ki a műhelyt. A történetet te írod.</em>

<br>

<a href="https://github.com/diablomike20/Andersen">Fő repository</a>
&nbsp; · &nbsp;
<a href="https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1">Launcher branch</a>

</div>
