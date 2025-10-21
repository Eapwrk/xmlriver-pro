# Документация XMLRiver Pro

[← Назад к основному README](../README.md)

Детальная документация по использованию XMLRiver Pro - профессиональной Python библиотеки для работы с API xmlriver.com.

## 📚 Содержание документации

### 🚀 Быстрый старт
- **[Основной README](../README.md)** - установка, базовые примеры, Quick Start
- **[Примеры использования](examples.md)** - детальные примеры всех методов
- **[Асинхронные примеры](examples_async.py)** - примеры асинхронного использования
- **[Многопоточные примеры](examples_concurrent.py)** - примеры многопоточности

### 📖 Справочники
- **[API Reference](API_REFERENCE.md)** - полный справочник всех методов и типов
- **[Справочник валидаторов](VALIDATORS_REFERENCE.md)** - все валидаторы с примерами
- **[Справочник форматтеров](FORMATTERS_REFERENCE.md)** - все форматтеры с примерами

### 🎯 Продвинутое использование
- **[Продвинутое использование](ADVANCED_USAGE.md)** - сложные сценарии и оптимизация
- **[Руководство по специальным блокам](SPECIAL_BLOCKS_GUIDE.md)** - OneBox, Knowledge Graph, колдунщики
- **[Руководство по Wordstat](WORDSTAT_GUIDE.md)** - работа с Yandex Wordstat API

### 🔧 Решение проблем
- **[Решение проблем](TROUBLESHOOTING.md)** - типичные ошибки и их решения

## 🎯 Для кого эта документация

### 👶 Новички
Начните с **[основного README](../README.md)** для быстрого старта, затем изучите **[примеры использования](examples.md)**.

### 👨‍💻 Разработчики
Используйте **[API Reference](API_REFERENCE.md)** для поиска конкретных методов и **[продвинутое использование](ADVANCED_USAGE.md)** для оптимизации.

### 🔍 SEO-специалисты
Изучите **[руководство по специальным блокам](SPECIAL_BLOCKS_GUIDE.md)** для работы с OneBox и колдунщиками.

### 🐛 При проблемах
Обратитесь к **[решению проблем](TROUBLESHOOTING.md)** для диагностики и исправления ошибок.

## 📋 Структура документации

```
docs/
├── README.md                    # Этот файл - обзор документации
├── examples.md                  # Детальные примеры всех методов
├── examples_async.py            # Асинхронные примеры
├── examples_concurrent.py       # Многопоточные примеры
├── API_REFERENCE.md             # Полный справочник API
├── ADVANCED_USAGE.md            # Продвинутые сценарии
├── SPECIAL_BLOCKS_GUIDE.md      # Руководство по специальным блокам
├── WORDSTAT_GUIDE.md            # Руководство по Wordstat API
├── VALIDATORS_REFERENCE.md      # Справочник валидаторов
├── FORMATTERS_REFERENCE.md      # Справочник форматтеров
└── TROUBLESHOOTING.md           # Решение проблем
```

## 🔗 Навигация

### По типу задач

| Задача | Документ |
|--------|----------|
| 🚀 Быстрый старт | [Основной README](../README.md) |
| 📝 Базовые примеры | [examples.md](examples.md) |
| ⚡ Асинхронность | [examples_async.py](examples_async.py) |
| 🔄 Многопоточность | [examples_concurrent.py](examples_concurrent.py) |
| 📖 Справочник методов | [API_REFERENCE.md](API_REFERENCE.md) |
| 🎯 Продвинутые сценарии | [ADVANCED_USAGE.md](ADVANCED_USAGE.md) |
| 🧩 Специальные блоки | [SPECIAL_BLOCKS_GUIDE.md](SPECIAL_BLOCKS_GUIDE.md) |
| ✅ Валидация параметров | [VALIDATORS_REFERENCE.md](VALIDATORS_REFERENCE.md) |
| 📊 Форматирование результатов | [FORMATTERS_REFERENCE.md](FORMATTERS_REFERENCE.md) |
| 🐛 Решение проблем | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |

### По поисковым системам

| Система | Документы |
|---------|-----------|
| 🔍 Google | [API Reference](API_REFERENCE.md#google-client), [Special Blocks](SPECIAL_BLOCKS_GUIDE.md#google-special-blocks) |
| 🔍 Yandex | [API Reference](API_REFERENCE.md#yandex-client), [Special Blocks](SPECIAL_BLOCKS_GUIDE.md#yandex-special-blocks) |
| 📊 Yandex Wordstat | [API Reference](API_REFERENCE.md#asyncwordstatclient), [Wordstat Guide](WORDSTAT_GUIDE.md) |
| ⚡ Асинхронные клиенты | [API Reference](API_REFERENCE.md#асинхронные-клиенты), [Advanced Usage](ADVANCED_USAGE.md#асинхронный-массовый-поиск) |

### По типам поиска

| Тип поиска | Документы |
|------------|-----------|
| 🔍 Органический поиск | [API Reference](API_REFERENCE.md#основные-клиенты), [Examples](examples.md) |
| 📰 Новости | [API Reference](API_REFERENCE.md#googlenews), [Advanced Usage](ADVANCED_USAGE.md#мониторинг-позиций) |
| 🖼️ Изображения | [API Reference](API_REFERENCE.md#googleimages), [Validators](VALIDATORS_REFERENCE.md#валидаторы-изображений) |
| 🗺️ Карты | [API Reference](API_REFERENCE.md#googlemaps), [Validators](VALIDATORS_REFERENCE.md#validate_coordscoords-coords---bool) |
| 📢 Реклама | [API Reference](API_REFERENCE.md#googleads), [Formatters](FORMATTERS_REFERENCE.md#format_ads_responseresponse-adsresponse---dictstr-any) |
| 🧩 Специальные блоки | [Special Blocks Guide](SPECIAL_BLOCKS_GUIDE.md) |
| 📊 Частотность запросов (Wordstat) | [Wordstat Guide](WORDSTAT_GUIDE.md), [API Reference](API_REFERENCE.md#asyncwordstatclient) |

## 🎯 Рекомендуемый путь изучения

### 1. Начальный уровень
1. **[Основной README](../README.md)** - установка и Quick Start
2. **[Примеры использования](examples.md)** - базовые примеры
3. **[Решение проблем](TROUBLESHOOTING.md)** - типичные ошибки

### 2. Средний уровень
1. **[API Reference](API_REFERENCE.md)** - полный справочник
2. **[Справочник валидаторов](VALIDATORS_REFERENCE.md)** - валидация параметров
3. **[Справочник форматтеров](FORMATTERS_REFERENCE.md)** - форматирование результатов

### 3. Продвинутый уровень
1. **[Продвинутое использование](ADVANCED_USAGE.md)** - сложные сценарии
2. **[Руководство по специальным блокам](SPECIAL_BLOCKS_GUIDE.md)** - OneBox и колдунщики
3. **[Асинхронные примеры](examples_async.py)** - многопоточность

## 🔍 Поиск в документации

### По ключевым словам

| Ключевое слово | Документы |
|----------------|-----------|
| `асинхронность` | [Advanced Usage](ADVANCED_USAGE.md), [examples_async.py](examples_async.py) |
| `валидация` | [Validators Reference](VALIDATORS_REFERENCE.md), [Troubleshooting](TROUBLESHOOTING.md) |
| `форматирование` | [Formatters Reference](FORMATTERS_REFERENCE.md) |
| `ошибки` | [Troubleshooting](TROUBLESHOOTING.md) |
| `лимиты` | [Troubleshooting](TROUBLESHOOTING.md#превышение-лимитов) |
| `таймауты` | [Troubleshooting](TROUBLESHOOTING.md#таймауты) |
| `OneBox` | [Special Blocks Guide](SPECIAL_BLOCKS_GUIDE.md#google-special-blocks) |
| `колдунщики` | [Special Blocks Guide](SPECIAL_BLOCKS_GUIDE.md#yandex-special-blocks) |
| `массовый поиск` | [Advanced Usage](ADVANCED_USAGE.md#массовый-поиск) |
| `мониторинг` | [Advanced Usage](ADVANCED_USAGE.md#мониторинг-позиций) |

### По кодам ошибок

| Код ошибки | Документ |
|------------|----------|
| 31, 42, 45 | [Troubleshooting](TROUBLESHOOTING.md#authenticationerror-invalid-api-key) |
| 110, 111, 115 | [Troubleshooting](TROUBLESHOOTING.md#ratelimiterror-rate-limit-exceeded) |
| 200 | [Troubleshooting](TROUBLESHOOTING.md#authenticationerror-insufficient-funds) |
| 2, 102-108, 120, 121 | [Troubleshooting](TROUBLESHOOTING.md#validationerror-invalid-parameters) |

## 📞 Поддержка

Если вы не нашли ответ на свой вопрос в документации:

1. **Проверьте [Troubleshooting](TROUBLESHOOTING.md)** - возможно, ваша проблема уже описана
2. **Изучите [API Reference](API_REFERENCE.md)** - найдите нужный метод
3. **Посмотрите [примеры](examples.md)** - возможно, есть похожий случай
4. **Создайте [Issue на GitHub](https://github.com/Eapwrk/xmlriver-pro/issues)** - опишите проблему подробно

## 🔄 Обновления документации

Документация обновляется вместе с библиотекой. Следите за:

- **[Releases на GitHub](https://github.com/Eapwrk/xmlriver-pro/releases)** - новые версии
- **[CHANGELOG](../CHANGELOG.md)** - история изменений
- **[Issues на GitHub](https://github.com/Eapwrk/xmlriver-pro/issues)** - известные проблемы

## 📝 Вклад в документацию

Улучшения документации приветствуются! Создавайте [Pull Requests](https://github.com/Eapwrk/xmlriver-pro/pulls) с:

- Исправлениями ошибок
- Новыми примерами
- Улучшениями объяснений
- Переводом на другие языки

---

[← Назад к основному README](../README.md) • [GitHub](https://github.com/Eapwrk/xmlriver-pro) • [PyPI](https://pypi.org/project/xmlriver-pro/)