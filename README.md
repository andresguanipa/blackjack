# Blackjack Trainer · Entrenador de Blackjack

A bilingual (English / Español) web app for learning and practicing the Hi-Lo card counting system in blackjack. It installs as an app (PWA) and works offline.

Una app web bilingüe (English / Español) para aprender y practicar el sistema de conteo de cartas Hi-Lo en blackjack. Se instala como app (PWA) y funciona sin internet.

## Features · Funciones

- **Learn / Aprende:** card values, running count, true count, bet ramp and count-based deviations.
- **Values / Valores:** card value drill.
- **Count / Conteo:** running count drill, automatic or against the clock, with records and goals.
- **True / Real:** true count conversion for 6-deck shoe and single deck.
- **Play / Jugar:** a full blackjack table with a 6-deck shoe or single deck, up to 4 players, splits, doubles, insurance, teaching mode, a count check before each bet, shoe summaries and adjustable dealing speed.

## Development · Desarrollo

The page sources are in `src/app-es.html` and `src/app-en.html`. After editing them, rebuild `index.html`:

Las fuentes están en `src/app-es.html` y `src/app-en.html`. Después de editarlas, reconstruye `index.html`:

```
python3 build.py
```

The script also bumps the service-worker cache version so installed copies update.

## License · Licencia

© 2026 Andres Guanipa. All rights reserved. · Todos los derechos reservados.

No permission is granted to copy, modify or redistribute this software without the author's written consent.
