<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-hero.svg" alt="Andersen — Ne csak történeteket írj. Teremts világokat." width="100%">
</p>

<p align="center">
  <a href="https://github.com/diablomike20/Andersen/tree/Launcher_Design_V1"><img src="https://img.shields.io/badge/ANDERSEN-LAUNCHER-172A42?style=for-the-badge&labelColor=0A1220" alt="Andersen Launcher"></a>
  <img src="https://img.shields.io/badge/WINDOWS-POWERSHELL-D6B36D?style=for-the-badge&labelColor=0A1220" alt="Windows PowerShell">
  <img src="https://img.shields.io/badge/INTERFACE-MAGYAR-D6B36D?style=for-the-badge&labelColor=0A1220" alt="Magyar kezelőfelület">
  <img src="https://img.shields.io/badge/OPEN%20SOURCE-LAUNCHER-172A42?style=for-the-badge&labelColor=0A1220" alt="Nyílt forráskódú indító">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-emblem.svg" alt="Andersen nyitott könyv emblémája" width="112">
</p>

<p align="center">
  <em>Your world. Your story. Your creation.</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-writing-oath.svg" alt="Andersen könyvészeti illusztrációja" width="100%">
</p>

---

<p align="center">
  <strong>Adj teret a történetnek.</strong><br>
  Az Andersen Windows-indító egy letisztult, magyar nyelvű belépési pont az alkotói műhely fejlesztői környezetéhez.
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%">
</p>

## Az alkotói műhely indítása

<p align="center">
  <img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-start-here.svg" alt="Az Andersen használatának első lépései" width="100%">
</p>

Az indító az Andersen vizuális világához igazodik: éjkék háttér, antik arany részletek, könyvszerű tipográfia és visszafogott díszítés. A kezelőfelület magyar nyelvű, a fejlesztői műveleteket pedig külön PowerShell-ablakban indítja el.

## Funkciók

| Művelet | Leírás |
|---|---|
| **Webes fejlesztői mód** | Elindítja a `pnpm run dev` parancsot. |
| **Asztali alkalmazás** | Elindítja a `pnpm run tauri:dev` parancsot. |
| **Függőségek telepítése** | Elindítja a `pnpm install` parancsot. |
| **Webes build készítése** | Elindítja a `pnpm run build` parancsot. |
| **GitHub-tárház megnyitása** | Megnyitja az Andersen fő repositoryját. |

Az indító ellenőrzi a szükséges Node.js- és pnpm-környezetet, kijelzi az észlelt verziókat, valamint első indításkor felajánlja a hiányzó projektfüggőségek telepítését.

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Első lépések

### 1. Helyezd el az indítót

Ez a branch kizárólag az indító fájljait tartalmazza. Az Andersen alkalmazás forráskódját nem tartalmazza.

Az indító használatához másold át a branch fájljait az Andersen teljes repositoryjának gyökérmappájába, az alábbi könyvtárszerkezetet megtartva:

```text
Andersen/
├── package.json
├── Start-Andersen.bat
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1
```

### 2. Indítsd el

A repository gyökerében kattints duplán a **Start-Andersen.bat** fájlra.

### 3. Válaszd ki a kívánt műveletet

A megjelenő magyar nyelvű felületen válaszd ki a webes fejlesztői módot, az asztali alkalmazást, a függőségek telepítését vagy a webes build készítését.

## Követelmények

- Windows PowerShell 5.1 vagy újabb.
- Node.js **22.19.0 vagy újabb**.
- Corepack és/vagy pnpm. Az Andersen projekt a **pnpm 12.13.0** verziót rögzíti a `package.json` fájlban.
- Az asztali alkalmazás fejlesztéséhez a Tauri Windowsos előfeltételei is szükségesek.

A launcher nem telepít észrevétlenül rendszerszintű futtatókörnyezeteket, és nem módosítja az Andersen alkalmazás forráskódját, beállításait vagy projektadatait.

<p align="center"><img src="https://raw.githubusercontent.com/diablomike20/Andersen/main/branding/andersen-ornamental-divider.svg" alt="" width="100%"></p>

## Fájlszerkezet

```text
/
├── README.md
├── Start-Andersen.bat
└── tools/
    └── launcher/
        └── Andersen-Launcher.ps1
```

- **README.md** – ez az útmutató, a repository gyökerében.
- **Start-Andersen.bat** – dupla kattintással indítható Windows-belépési pont.
- **tools/launcher/Andersen-Launcher.ps1** – a grafikus, magyar nyelvű launcher.

## Fontos tudnivalók

Ez a launcher önmagában nem az Andersen alkalmazás, és nem tartalmazza annak forráskódját. A fejlesztői parancsok futtatásához az Andersen teljes repositoryja szükséges.

A launcher külön folyamatablakban indítja a parancsokat, hogy a napló és az esetleges hibaüzenetek láthatók maradjanak. A projektfüggőségek telepítése az Andersen saját `package.json` fájlja alapján történik.

## Közreműködés

A launcher módosításait célzottan, az alkalmazás többi részétől elkülönítve érdemes kezelni. Hibajelentésben ne szerepeljen API-kulcs, token vagy más bizalmas adat.

## Licenc

A launcher az Andersen repository licencfeltételei szerint használható. A teljes licencszöveg az eredeti projekt [LICENSE](https://github.com/diablomike20/Andersen/blob/main/LICENSE) fájljában található.

---

<p align="center">
  <strong>ANDERSEN</strong><br>
  <em>Give your imagination a universe.</em><br>
  <sub>Adj teret a történetnek.</sub>
</p>
