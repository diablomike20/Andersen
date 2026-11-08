# Andersen – magyar Windows-indító

A Windowsos indító az Andersen arculatát követi: éjkék háttér, antik arany részletek, könyvszerű tipográfia és visszafogott díszítés.

## Indítás

A tárház gyökérmappájában kattints duplán a **Start-Andersen.bat** fájlra.

Az indító különálló segédprogram: nem módosítja az alkalmazás forráskódját, beállításait, hitelesítő adatait vagy projektadatait.

## Elérhető műveletek

- **Webes fejlesztői mód** – elindítja a `pnpm run dev` parancsot.
- **Asztali alkalmazás** – elindítja a `pnpm run tauri:dev` parancsot.
- **Függőségek telepítése** – elindítja a `pnpm install` parancsot.
- **Webes build készítése** – elindítja a `pnpm run build` parancsot.
- **GitHub-tárház megnyitása** – megnyitja az Andersen GitHub-oldalát.

Minden művelet külön PowerShell-ablakban fut, így a folyamat naplója és az esetleges hibaüzenetek láthatók maradnak.

## Követelmények

- Windows PowerShell 5.1 vagy újabb.
- Node.js **22.19.0 vagy újabb**.
- Corepack és/vagy pnpm. A tárház a **pnpm 12.13.0** verziót rögzíti a `package.json` fájlban.
- Az asztali változat fordításához a Tauri dokumentációjában felsorolt Windowsos előfeltételek is szükségesek.

Az indító ellenőrzi a helyi fejlesztői eszközöket és kijelzi az észlelt verziókat. Nem telepít észrevétlenül futtatókörnyezeteket, és nem módosít rendszerszintű beállításokat.

## Fájlok

- `Start-Andersen.bat` – a dupla kattintással indítható belépési pont.
- `tools/launcher/Andersen-Launcher.ps1` – a grafikus, magyar nyelvű indítófelület.
- `tools/launcher/README.md` – ez az útmutató.

Ha első indításkor hiányzik a `node_modules` mappa, az indító felajánlja a projektfüggőségek telepítését. Az alkalmazás saját előkészítő és build-parancsai továbbra is a megszokott módon futnak.
