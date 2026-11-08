<p align="center">
  <img src="docs/branding/andersen-hero.svg" alt="Andersen — Ne csak történeteket írj. Teremts világokat." width="100%">
</p>

<p align="center">
  <a href="https://github.com/diablomike20/Andersen"><img src="https://img.shields.io/badge/GitHub-Andersen-181717?logo=github" alt="Andersen a GitHubon"></a>
  <img src="https://img.shields.io/badge/Nyelv-Magyar%20(alapértelmezett)-white?labelColor=555" alt="Magyar alapértelmezett nyelv">
  <img src="https://img.shields.io/badge/Platform-Web%20%7C%20PWA%20%7C%20Asztali-8B6B35" alt="Web, PWA és asztali alkalmazás">
  <img src="https://img.shields.io/badge/Licenc-MIT-2E8B57" alt="MIT licenc">
</p>

---

Minden nagy történet egyetlen gondolattal kezdődik. Egy karakterrel. Egy hellyel. Egy lehetetlennel, ami egyszer csak valósággá válik.

**Az Andersen egy nyílt forráskódú kreatív alkotóműhely íróknak, történetmesélőknek és világépítőknek.** Egyetlen összefüggő munkakörnyezetben kapcsolja össze a kéziratírást, a karakteralkotást, a világépítést, a cselekménytervezést, a kutatást és a szerkesztést – hogy ne a szétszórt eszközökkel, hanem az alkotással foglalkozhass.

**A történet a tiéd. Az irányítás is.**

<p align="center">
  <img src="docs/branding/andersen-workflow.svg" alt="Az Andersen öt összekapcsolt alkotói területe" width="100%">
</p>

<p align="center">
  <img src="docs/branding/andersen-ecosystem.svg" alt="Az Andersen teljes alkotói ökoszisztémája" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/WRITE-Kézirat-1B2A41?style=for-the-badge&labelColor=0B1220" alt="Kéziratírás">
  <img src="https://img.shields.io/badge/BUILD-Világépítés-9B7540?style=for-the-badge&labelColor=0B1220" alt="Világépítés">
  <img src="https://img.shields.io/badge/CREATE-Karakterek-9B7540?style=for-the-badge&labelColor=0B1220" alt="Karakteralkotás">
  <img src="https://img.shields.io/badge/IMAGINE-Történettervezés-1B2A41?style=for-the-badge&labelColor=0B1220" alt="Történettervezés">
</p>

Az Andersenben a mesterséges intelligencia lehet alkotótárs, ötletadó vagy szerkesztési segítség, de soha nem kötelező főszereplő. Használhatod a támogatott szolgáltatókkal, helyi vagy böngészőben futó modellekkel, de akár teljesen MI nélkül is.

> [!NOTE]
> Az Andersen a WorldScript Studio kódbázisára épülő, önálló termékidentitással rendelkező folytatás. A kompatibilitás megőrzése érdekében egyes belső technikai azonosítók változatlanok maradnak; a felhasználók által látható terméknév és arculat az Andersené.

## ✨ Egy alkotói tér. Egy teljes univerzum.

- **Kéziratírás** – dolgozz fejezetekre és részekre tagolt kéziraton, dedikált írófelületen.
- **Világépítés** – rendszerezd a szereplőket, helyszíneket, háttérinformációkat és a világod szabályait.
- **Karakterek és kapcsolatok** – építs összetett szereplőket, motivációkat és kapcsolatrendszereket.
- **Cselekménytervezés** – alakíts történetvázlatokat, cselekményszerkezeteket, gondolattérképeket és idővonalakat.
- **Kutatás és szerkesztés** – tartsd kéznél a háttéranyagokat, és finomítsd a szöveget a projekten belül.
- **Választható mesterséges intelligencia** – dolgozz támogatott szolgáltatókkal, helyi vagy böngészőben futó modellekkel, vagy MI nélkül.
- **Haladáskövetés** – kövesd az alkotói célokat és a projekt állapotát.
- **Exportálás és publikálás** – készítsd elő a munkádat a támogatott exportfolyamatokhoz.
- **Szabad munkakörnyezet** – használd böngészőből, telepíthető PWA-ként vagy Tauri-alapú asztali alkalmazásként.

## 🖼️ Pillants be az alkotói térbe

Az alábbi képek a repository vizuális regressziós tesztjeinek tényleges, 1280 × 720-as alkalmazásképernyőképei.

<table>
  <tr>
    <td width="50%"><strong>Áttekintés és kezdőfelület</strong><br><img src="tests/e2e/visual-regression.spec.ts-snapshots/home-chromium.png" alt="Andersen kezdőfelület" width="100%"></td>
    <td width="50%"><strong>Írói munkafelület</strong><br><img src="tests/e2e/visual-regression.spec.ts-snapshots/writer-chromium.png" alt="Andersen írói nézet" width="100%"></td>
  </tr>
  <tr>
    <td width="50%"><strong>Karakteralkotás</strong><br><img src="tests/e2e/visual-regression.spec.ts-snapshots/characters-chromium.png" alt="Andersen karakterek nézet" width="100%"></td>
    <td width="50%"><strong>Beállítások</strong><br><img src="tests/e2e/visual-regression.spec.ts-snapshots/settings-chromium.png" alt="Andersen beállítások nézet" width="100%"></td>
  </tr>
</table>

<p align="center"><sub>A képernyőképek a jelenlegi teszt-bázisállapotot mutatják; a felület és a funkciók fejlesztés közben változhatnak.</sub></p>

Az egyes funkciók elérhetősége platformonként és beállításonként eltérhet. A hálózati szolgáltatások internetkapcsolatot igényelnek.

## 🧭 Alapelveink

<p align="center">
  <img src="docs/branding/andersen-principles.svg" alt="Az Andersen négy alapelve: alkotói kontroll, adattulajdonlás, választható MI és nyílt közösség" width="100%">
</p>

### Az alkotóé az utolsó szó

A kézirat és a projekt adatai jelentik a munka alapját. Az MI által készített tartalom javaslat, nem pedig olyan tekintély, amely észrevétlenül felülírhatja a szerző munkáját.

### Helyi működés, átlátható adatkezelés

Az alapvető projektmunkafolyamatok a helyi adattulajdonlásra épülnek. Bizonyos választható funkciók – például a felhőalapú MI-szolgáltatók, az együttműködési szolgáltatások, a nyelvi ellenőrzők, a modellletöltések és a frissítés-ellenőrzések – hálózati kapcsolatot használnak. Minden integrációt csak a működésének megismerése után engedélyezz.

### MI, amikor szeretnéd. Szabadság, mindig.

Az Andersen akkor is használható írói környezet marad, ha nincs beállított API-kulcsod, nem érhető el egyetlen szolgáltató sem, vagy egyszerűen kikapcsolod az MI-funkciókat.

### Nyílt fejlesztés, valódi közreműködés

A projekt célja, hogy a működése megismerhető, továbbfejleszthető és a közreműködők számára is hozzáférhető legyen. A pontos dokumentáció, az ellenőrizhető tesztek és a funkciók érettségének őszinte bemutatása fontosabb a hangzatos ígéreteknél.

## 🚀 Első lépések

### Az alkalmazás használata

Ez a repository az Andersen forráskódját és fejlesztési anyagait tartalmazza. A kiadott, futtatható webes változatok és telepítők a projekt GitHub Releases oldalán jelennek meg, amint közzétételre kerülnek.

### Futtatás forráskódból

A projekt Node.js-t és pnpm-et használ. A pontos verziókat és parancsokat indulás előtt ellenőrizd a `package.json` fájlban.

```bash
corepack enable
pnpm install
pnpm run dev
```

Éles webes build készítése:

```bash
pnpm run build
```

Asztali fejlesztői környezet indítása:

```bash
pnpm run tauri:dev
```

Egyes natív célplatformokhoz a Tauri platformfüggő fejlesztői eszközei is szükségesek. A fenti parancsok a forráskód futtatásához adnak kiindulópontot; nem garantálják, hogy minden célplatform külön konfiguráció nélkül buildelhető.

## 🌍 Nyelvek

- Alapértelmezett kezelőfelületi nyelv: **magyar**
- Az angol és további fordítások is részei a projektnek.
- A fordítási kulcsok teljessége önmagában nem garantálja a szakmailag és nyelvileg kifogástalan szöveget. Szívesen fogadunk javaslatokat a terminológia, az egységesség és a nyelvi minőség javítására.

<p align="center">
  <img src="docs/branding/andersen-platforms.svg" alt="Andersen webes, PWA és asztali platformokon, választható MI-vel" width="100%">
</p>

## 🛠️ Technológiai háttér

A jelenlegi kódbázis főbb technológiái:

- React és TypeScript
- Vite
- Tauri 2 az asztali alkalmazáshoz
- Moduláris többnyelvűségi rendszer
- Választható MI-szolgáltatói és helyi modellintegrációk

A pontos függőségverziókat és az elérhető parancsokat a `package.json` tartalmazza.

## 🤝 Közreműködés

Az Andersen nyílt projekt: örömmel fogadjuk az ötleteket, hibajelentéseket és a közösség érdemi hozzájárulását.

Pull request beküldése előtt:

1. Olvasd el a repository közreműködési és biztonsági útmutatóját.
2. Írd le, milyen problémát old meg a módosítás, és hogyan segíti a felhasználókat.
3. Tartsd a változtatásokat célzottan, kerüld a témához nem kapcsolódó átalakításokat.
4. Viselkedésváltozás esetén egészítsd ki vagy frissítsd a teszteket.
5. Soha ne tölts fel API-kulcsokat, hitelesítő adatokat, személyes kéziratokat vagy más bizalmas adatokat.
6. Jelezd egyértelműen, ha egy funkció kísérleti, platformfüggő vagy külső szolgáltatástól függ.

Nagyobb változtatás előtt nyiss egy issue-t, hogy egyeztethessük az irányt.

## 🔐 Biztonság és adatvédelem

Biztonsági sérülékenységet ne nyilvános issue-ban jelents. Használd a repository privát sérülékenység-bejelentési lehetőségét, amikor elérhető. Hibajelentésben soha ne szerepeljen valódi API-kulcs, token, személyes adat vagy bizalmas kéziratrészlet.

Az Andersen nem tünteti el a hálózati adatforgalmat: ha felhőszolgáltatót vagy online integrációt választasz, az adott szolgáltatás működéséhez szükséges információ elhagyhatja az eszközödet. Az integráció használata előtt ismerd meg a szolgáltató adatvédelmi feltételeit és a projekt biztonsági dokumentációját.

## 📜 Licenc

A projekt megtartja a forráskódban szereplő licencet. A teljes feltételeket a [LICENSE](LICENSE) fájl tartalmazza.

---

<p align="center">
  <strong>ANDERSEN</strong><br>
  <em>Give your imagination a universe.</em><br><br>
  <sub>Adj teret a történetnek.</sub>
</p>
