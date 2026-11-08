<div align="center">

# ANDERSEN / LAUNCHER

### A műhely kapuja. Nem maga a műhely.

**Egyetlen indítófelület az Andersen fejlesztői munkafolyamataihoz.**

<sub>WINDOWS · POWERSHELL · MAGYAR UI</sub>

<br>

<a href="https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1"><img src="https://img.shields.io/badge/BRANCH-Launcher_Design_V1-172A42?style=for-the-badge&labelColor=0A1220" alt="Launcher Design V1"></a>
<img src="https://img.shields.io/badge/SHELL-Windows%20PowerShell-D6B36D?style=for-the-badge&labelColor=0A1220" alt="Windows PowerShell">
<img src="https://img.shields.io/badge/LANGUAGE-MAGYAR-D6B36D?style=for-the-badge&labelColor=0A1220" alt="Magyar">

<br><br>

<table>
<tr>
<td align="center" width="25%"><strong>01</strong><br>ELŐKÉSZÍTÉS</td>
<td align="center" width="25%"><strong>02</strong><br>INDÍTÁS</td>
<td align="center" width="25%"><strong>03</strong><br>MUNKA</td>
<td align="center" width="25%"><strong>04</strong><br>BUILD</td>
</tr>
<tr>
<td align="center">Környezet<br>ellenőrzése</td>
<td align="center">Mód<br>kiválasztása</td>
<td align="center">Fejlesztés<br>külön ablakban</td>
<td align="center">Webes<br>csomagolás</td>
</tr>
</table>

</div>

---

## A koncepció

Az Andersen egy alkotói műhely. A launcher ennek a műhelynek a **vezérlőpultja**: nem próbálja eljátszani az alkalmazást, hanem rövid és egyértelmű utat ad a legfontosabb fejlesztői műveletekhez.

A README ezért nem az alkalmazás bemutatóoldalának másolata. Saját, műveletközpontú felépítést kapott: áttekintés, indítási útvonal, műveleti térkép és technikai feltételek.

## Műveleti térkép

| Parancs | Mit indít? | Mikor használd? |
|:--|:--|:--|
| **WEBES FEJLESZTŐI MÓD** | `pnpm run dev` | Amikor a webes felületen dolgozol. |
| **ASZTALI ALKALMAZÁS** | `pnpm run tauri:dev` | Amikor a Tauri asztali környezetet fejleszted. |
| **FÜGGŐSÉGEK TELEPÍTÉSE** | `pnpm install` | Első beállításkor vagy függőségváltozás után. |
| **WEBES BUILD KÉSZÍTÉSE** | `pnpm run build` | Amikor ellenőrizni vagy előállítani szeretnéd a webes buildet. |
| **GITHUB-TÁRHÁZ MEGNYITÁSA** | Andersen repository | A forráskód és a projekt dokumentációjának megnyitásához. |

A launcher ellenőrzi a Node.js- és pnpm-környezetet, megjeleníti az észlelt verziókat, és hiányzó `node_modules` esetén felajánlja a függőségek telepítését. A fejlesztői parancsokat külön PowerShell-ablakban indítja, így a kimenet és a hibák láthatók maradnak.

## Indítás három lépésben

### 1 — Tedd a megfelelő helyre

Ez a branch szándékosan **launcher-only**: nem tartalmazza az Andersen alkalmazás forráskódját. A teljes Andersen repositoryra szükséged lesz.

A branch három fájlját másold át a teljes Andersen repository gyökerébe. A meglévő projektfájlokat ne írd felül.

```text
Andersen/                         ← a teljes projekt
├── package.json                  ← az alkalmazás saját fájlja
├── Start-Andersen.bat            ← innen indul a launcher
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1 ← grafikus felület
```

### 2 — Indítsd el

A teljes Andersen mappájában kattints duplán a `Start-Andersen.bat` fájlra.

### 3 — Válassz munkamódot

A magyar nyelvű ablakban válaszd ki a kívánt műveletet. A launcher a parancsot külön PowerShell-ablakban futtatja.

## Technikai feltételek

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

A launcher egy kényelmi belépési pont, nem önálló alkalmazás.

- Nem tartalmazza az Andersen forráskódját.
- Nem helyettesíti a projekt `package.json` fájlját.
- Nem telepít észrevétlenül rendszerszintű futtatókörnyezeteket.
- Nem módosítja az Andersen alkalmazás forráskódját, beállításait vagy projektadatait.
- A build és a fejlesztői parancsok a teljes projekt környezetében futnak.

## Repository-térkép

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

## Közreműködés és licenc

A launcher módosításait tartsd elkülönítve az Andersen alkalmazás többi részétől. Hibajelentésben ne szerepeljen API-kulcs, token vagy más bizalmas adat.

A használatra az Andersen repository licencfeltételei vonatkoznak: [LICENSE](https://github.com/diablomike20/Andersen/blob/main/LICENSE).

---

<div align="center">

**ANDERSEN LAUNCHER**

<sub>Nyisd ki a műhelyt. A történetet te írod.</sub>

<a href="https://github.com/diablomike20/Andersen">Fő repository</a>
&nbsp;·&nbsp;
<a href="https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1">Launcher branch</a>

</div>
