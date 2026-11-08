<p align="center">
  <img src="public/icon-512.png" width="128" height="128" alt="Andersen embléma">
</p>

<h1 align="center">Andersen</h1>

<p align="center">
  <strong>Kreatív írói műhely</strong><br>
  <em>Adj teret a történetnek!</em>
</p>

<p align="center">
  <a href="https://github.com/diablomike20/Andersen"><img src="https://img.shields.io/badge/GitHub-Andersen-181717?logo=github" alt="Andersen a GitHubon"></a>
  <img src="https://img.shields.io/badge/Nyelv-Magyar%20(alapértelmezett)-white?labelColor=555" alt="Magyar alapértelmezett nyelv">
  <img src="https://img.shields.io/badge/Platform-Web%20%7C%20PWA%20%7C%20Asztali-8B6B35" alt="Web, PWA és asztali alkalmazás">
  <img src="https://img.shields.io/badge/Licenc-MIT-2E8B57" alt="MIT licenc">
</p>

---

**Az Andersen** egy nyílt forráskódú alkotói környezet regényíróknak, történetmesélőknek és világépítőknek. Egyetlen, átlátható munkaterületen fogja össze mindazt, amire egy összetett kreatív projekthez szükség lehet: a kéziratot, a szereplőket, a kitalált világokat, a cselekmény felépítését, a kutatást, a szerkesztést és a publikálás előkészítését.

A kezelőfelület alapértelmezett nyelve **magyar**. Az angol és a további támogatott nyelvek szintén elérhetők.

> [!NOTE]
> Az Andersen a WorldScript Studio kódbázisára épülő, önálló termékidentitással rendelkező folytatás. A kompatibilitás megőrzése érdekében egyes belső technikai azonosítók változatlanok maradnak; a felhasználók által látható terméknév és arculat az Andersené.

## Az elképzelés

Egy könyv megírása jóval több, mint mondatok egymás után rendezése. Szereplőket, helyszíneket, idővonalakat, motivációkat, cselekményszálakat, kutatási anyagokat, változatokat és javításokat kell összefogni úgy, hogy közben maga a történet maradjon a középpontban.

Az Andersen alapja maga az alkotói projekt. A kézirat és a hozzá tartozó adatok az alkotó tulajdonában és irányítása alatt maradnak. A mesterséges intelligencia segítséget nyújthat, de nem veszi át az irányítást a történet vagy a szerző munkája felett.

## Mire használhatod?

- **Kéziratírás és rendszerezés** – dolgozz fejezetekre és részekre tagolt kéziraton, dedikált írófelületen.
- **Világépítés** – tartsd egy helyen a szereplők adatlapjait, helyszíneket, háttérinformációkat és a történet világának szabályait.
- **Cselekménytervezés** – építs történetvázlatokat, cselekményszerkezeteket, gondolattérképeket és szereplői kapcsolatokat.
- **Kutatás és szerkesztés** – rendszerezd a háttéranyagokat, és dolgozd át a szöveget a projekten belül.
- **MI a saját feltételeid szerint** – használhatsz támogatott szolgáltatókat, ahol elérhető, helyi vagy böngészőben futó modelleket, de akár teljesen MI nélkül is alkothatsz.
- **Haladáskövetés** – kövesd a célokat, a projekt állapotát és az alkotói folyamatot.
- **Exportálás és publikálás** – készítsd elő a munkádat a támogatott exportfolyamatokhoz.
- **Szabad munkakörnyezet-választás** – használd böngészőből, telepíthető PWA-ként vagy Tauri-alapú asztali alkalmazásként.

Az egyes funkciók elérhetősége platformonként és beállításonként eltérhet. A hálózati szolgáltatások internetkapcsolatot igényelnek.

## Alapelveink

### A projekt és az alkotó az első

A kézirat és a projekt adatai jelentik a munka alapját. A mesterséges intelligencia által készített tartalom javaslat, nem pedig olyan tekintély, amely észrevétlenül felülírhatja a szerző munkáját.

### Helyi működés, őszinte adatkezelési határokkal

Az alapvető projektmunkafolyamatok a helyi adattulajdonlásra épülnek. Bizonyos választható funkciók – például a felhőalapú MI-szolgáltatók, az együttműködési szolgáltatások, a nyelvi ellenőrzők, a modellletöltések és a frissítés-ellenőrzések – hálózati kapcsolatot használnak. Minden integrációt csak a működésének megismerése után engedélyezz.

### A mesterséges intelligencia választható

Az Andersen akkor is használható írói környezet marad, ha nincs beállított API-kulcsod, nem érhető el egyetlen szolgáltató sem, vagy egyszerűen kikapcsolod az MI-funkciókat.

### Nyílt és átlátható fejlesztés

A projekt célja, hogy a működése megismerhető, továbbfejleszthető és a közreműködők számára is hozzáférhető legyen. A pontos dokumentáció, az ellenőrizhető tesztek és a funkciók érettségének őszinte bemutatása fontosabb a hangzatos ígéreteknél.

## Első lépések

### Az alkalmazás használata

Az önálló Andersen-webes kiadás és a letölthető telepítők hivatkozásai az új repository és a terjesztési csatornák elkészülte után jelennek meg itt.

### Futtatás forráskódból

A projekt Node.js-t és pnpm-et használ. A pontos verziókat indulás előtt ellenőrizd a `package.json` fájlban.

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

Egyes natív célplatformokhoz a Tauri platformfüggő fejlesztői eszközei is szükségesek. Ez a leírás nem telepít függőségeket és nem indít buildfolyamatot.

## Nyelvek

- Alapértelmezett kezelőfelületi nyelv: **magyar**
- Az angol és további fordítások is részei a projektnek.
- A fordítási kulcsok teljessége önmagában nem garantálja a szakmailag és nyelvileg kifogástalan szöveget. Szívesen fogadunk javaslatokat a terminológia, az egységesség és a nyelvi minőség javítására.

## Technológiai háttér

A jelenlegi kódbázis főbb technológiái:

- React és TypeScript
- Vite
- Tauri 2 az asztali alkalmazáshoz
- Moduláris többnyelvűségi rendszer
- Választható MI-szolgáltatói és helyi modellintegrációk

A pontos függőségverziókat és az elérhető parancsokat a `package.json` tartalmazza.

## Közreműködés

Örömmel fogadjuk a közösség hozzájárulását. Pull request beküldése előtt:

1. Olvasd el a repository közreműködési és biztonsági útmutatóját.
2. Írd le, milyen problémát old meg a módosítás, és hogyan segíti a felhasználókat.
3. Tartsd a változtatásokat célzottan, kerüld a témához nem kapcsolódó átalakításokat.
4. Viselkedésváltozás esetén egészítsd ki vagy frissítsd a teszteket.
5. Soha ne tölts fel API-kulcsokat, hitelesítő adatokat, személyes kéziratokat vagy más bizalmas adatokat.
6. Jelezd egyértelműen, ha egy funkció kísérleti, platformfüggő vagy külső szolgáltatástól függ.

Nagyobb változtatás előtt nyiss egy issue-t, hogy egyeztethessük az irányt.

## Biztonság és adatvédelem

Biztonsági sérülékenységet ne nyilvános issue-ban jelents. Használd a repository privát sérülékenység-bejelentési lehetőségét, amikor elérhető. Hibajelentésben soha ne szerepeljen valódi API-kulcs, token, személyes adat vagy bizalmas kéziratrészlet.

Az Andersen nem tünteti el a hálózati adatforgalmat: ha felhőszolgáltatót vagy online integrációt választasz, az adott szolgáltatás működéséhez szükséges információ elhagyhatja az eszközödet. Az integráció használata előtt ismerd meg a szolgáltató adatvédelmi feltételeit és a projekt biztonsági dokumentációját.

## Licenc

A projekt megtartja a forráskódban szereplő licencet. A teljes feltételeket a [LICENSE](LICENSE) fájl tartalmazza.

---

<p align="center">
  <strong>Andersen</strong><br>
  <sub>Adj teret a történetnek.</sub>
</p>
