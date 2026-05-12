# parik-live-scraper

CLI-інструмент для отримання live футбольних даних з Parik24.

Парсить HTML зі сторінки `parik24ua.kyiv.ua/uk/all-live` і виводить результати в консоль (таблиця або JSON). Не потребує браузера — працює через HTTP запити.

## Встановлення

```bash
pip install -e .
```

## Використання

### Таблиця всіх live матчів
```bash
parik-live
```

### JSON-формат
```bash
parik-live --json
```

### Тільки матчі в грі (без запланованих/завершених)
```bash
parik-live --live-only
```

### Фільтр по лізі
```bash
parik-live --league "Бразилія"
```

### Комбінація параметрів
```bash
parik-live --live-only --league "Бразилія" --json
```

### Інший URL (наприклад, основний домен)
```bash
parik-live --url https://parik.club
```

## Використання як бібліотеку

```python
import asyncio
from parik_scraper import ParikScraper

async def main():
    async with ParikScraper() as scraper:
        matches = await scraper.fetch_live_matches()
        for m in matches:
            print(f"{m.minute}' {m.home_team} {m.score} {m.away_team} [{m.league}]")

asyncio.run(main())
```

## Тестування

```bash
pip install -e ".[dev]"
pytest -v
```

## Обмеження

- CSS-класи на сайті обфусковані і можуть змінитися при оновленні сайту
- `parik.club` заблокований для не-українських IP — за замовчуванням використовується дзеркало `parik24ua.kyiv.ua`
- Кіберфутбол і replays також відображаються, бо знаходяться в секції "Футбол"
