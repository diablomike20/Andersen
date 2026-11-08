<div align="center">

<img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-emblem.svg" alt="Andersen embléma" width="96">

# ANDERSEN
### LAUNCHER

**A műhely kapuja. Nem maga a műhely.**

A fejlesztői környezeted legfontosabb műveletei — egyetlen, magyar nyelvű indítófelületen.

<p>
  <img src="https://img.shields.io/badge/WINDOWS-172A42?style=flat-square&labelColor=0A1220" alt="Windows">
  <img src="https://img.shields.io/badge/POWERSHELL-172A42?style=flat-square&labelColor=0A1220" alt="PowerShell">
  <img src="https://img.shields.io/badge/INTERFÉSZ-MAGYAR-C9A96E?style=flat-square&labelColor=0A1220" alt="Magyar felület">
  <a href="https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1"><img src="https://img.shields.io/badge/BRANCH-Launcher_Design_V1-172A42?style=flat-square&labelColor=0A1220" alt="Launcher Design V1"></a>
</p>

<table>
  <tr>
    <td align="center" width="25%"><strong>01</strong><br><sub>ELŐKÉSZÍTÉS</sub></td>
    <td align="center" width="25%"><strong>02</strong><br><sub>INDÍTÁS</sub></td>
    <td align="center" width="25%"><strong>03</strong><br><sub>FEJLESZTÉS</sub></td>
    <td align="center" width="25%"><strong>04</strong><br><sub>BUILD</sub></td>
  </tr>
</table>

<sub>KEVESEBB KERESGÉLÉS. ÁTLÁTHATÓBB INDÍTÁS. TÖBB IDŐ AZ ALKOTÁSRA.</sub>

</div>

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## A launcher feladata

Az Andersen egy alkotói műhely. Ez a kis segédprogram a fejlesztői környezet bejárata: **nem maga az Andersen alkalmazás**, hanem egy áttekinthető vezérlőfelület a leggyakoribb fejlesztői parancsokhoz.

- ellenőrzi a szükséges Node.js- és pnpm-környezetet;
- jelzi a függőségek állapotát;
- felajánlja a telepítést, ha hiányzik a `node_modules` könyvtár;
- külön PowerShell-ablakban indítja a kiválasztott feladatot.

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-start-here.svg" alt="Az Andersen projekt indításának vizuális útmutatója" width="100%">
  <br>
  <sub>ELŐKÉSZÍTÉS → INDÍTÁS → ALKOTÁS → ELLENŐRZÉS</sub>
</p>

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Műveleti központ

| Művelet | Futtatott parancs | Mire szolgál? |
|:--|:--|:--|
| **Webes fejlesztői mód** | `pnpm run dev` | A webes felület helyi fejlesztése. |
| **Asztali alkalmazás** | `pnpm run tauri:dev` | A Tauri-alapú asztali változat indítása. |
| **Függőségek telepítése** | `pnpm install` | A projektcsomagok telepítése. |
| **Webes build készítése** | `pnpm run build` | A webes build előállítása. |
| **GitHub-tárház megnyitása** | Andersen repository | A projekt GitHub-oldalának megnyitása. |

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Első indítás

<div align="center">

| <sub>01 · ELŐKÉSZÍTÉS</sub> | <sub>02 · INDÍTÁS</sub> | <sub>03 · VÁLASZTÁS</sub> |
|:--:|:--:|:--:|
| Legyen meg a teljes Andersen projekt a gépeden. | Másold be a launcher három fájlját a projekt gyökerébe, majd indítsd el a BAT fájlt. | Kattints a kívánt műveletre. |

</div>

### Helyes mappaszerkezet

A branch szándékosan csak a launchert tartalmazza. A futtatáshoz a teljes Andersen repository szükséges; a launcherfájlok annak gyökerébe kerüljenek.

```text
Andersen/
├── package.json
├── Start-Andersen.bat
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1
```

**Fontos:** a három launcherfájlt másold át a teljes projekt megfelelő helyére. A projekt meglévő fájljait ne írd felül.

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Rendszerkövetelmények

| Összetevő | Követelmény |
|:--|:--|
| Operációs rendszer | Windows |
| PowerShell | Windows PowerShell 5.1 vagy újabb |
| Node.js | 22.19.0 vagy újabb |
| Csomagkezelő | Corepack vagy pnpm |
| Projektben rögzített pnpm | 12.13.0 |
| Asztali fejlesztés | A Tauri Windowsos előfeltételei |

A verziókövetelményeket és a futtatott parancsokat a teljes Andersen projekt `package.json` fájljával együtt érdemes ellenőrizni.

## Mit tesz — és mit nem?

| A launcher elvégzi | A launcher nem végzi el |
|:--|:--|
| Elindítja a kiválasztott fejlesztői parancsot. | Nem tartalmazza az Andersen alkalmazás forráskódját. |
| Megmutatja a Node.js, pnpm és függőségek állapotát. | Nem helyettesíti a teljes projektet. |
| Külön ablakban hagyja láthatóan a parancsok kimenetét. | Nem telepíti automatikusan a Node.js-t vagy a Tauri előfeltételeit. |

## A branch tartalma

```text
Launcher_Design_V1/
├── README.md
├── Start-Andersen.bat
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1
```

A branch célja egy könnyen áttekinthető, a teljes Andersen projekthez hozzáadható indítócsomag. A fő alkalmazás forráskódját és a `main` branch tartalmát nem módosítja.

## Közreműködés és licenc

A launcherrel kapcsolatos módosításokat tartsd elkülönítve az alkalmazás többi részétől. Hibajelentésben ne ossz meg API-kulcsot, tokent vagy más bizalmas adatot.

A használatra az Andersen repository licencfeltételei vonatkoznak: [LICENSE](https://github.com/diablomike20/Andersen/blob/main/LICENSE).

---

<div align="center">

<img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-emblem.svg" alt="Andersen embléma" width="54">

**ANDERSEN LAUNCHER**

<em>Nyisd ki a műhelyt. A történetet te írod.</em>

<a href="https://github.com/diablomike20/Andersen">Fő repository</a>
&nbsp; · &nbsp;
<a href="https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1">Launcher branch</a>

</div>
