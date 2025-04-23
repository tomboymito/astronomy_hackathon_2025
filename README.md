# Astronomy Hackathon 2025: Comet Analysis Tool

## О проекте

Проект разработан для Астрономического Хакатона 2025 и включает набор инструментов для анализа комет:
- Расчет массы кометы на основе видимой звездной величины и расстояний
- Определение размера ядра кометы по данным альбедо
- Визуализация астрономических данных

## Технологический стек

### Backend
- **Языки**: Python 3.9, C++17
- **Библиотеки**:
  - PyBind11 (интеграция C++/Python)
  - Astropy (работа с FITS)
  - NumPy (векторизированные вычисления)

### Frontend
- PyQt5 (GUI)
- Matplotlib (визуализация графиков)

### Тестирование
- Google Test (C++)
- pytest (Python)

## Структура проекта

```
astronomy_hackathon_2025/
├── backend/          # Вычислительные модули
│   ├── comet_mass/   # Расчет массы кометы (C++)
│   ├── comet_size/   # Размер ядра кометы (Python)
│   └── shared/       # Общие утилиты
├── frontend/         # Пользовательский интерфейс
│   ├── assets/       # Ресурсы (иконки, стили)
│   ├── ui/           # Файлы интерфейса
│   └── views/        # Вкладки приложения
├── design/           # Дизайн-материалы
├── docs/             # Документация
├── scripts/          # Вспомогательные скрипты
└── tests/            # Тесты
```

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/astronomy_hackathon_2025.git
cd astronomy_hackathon_2025
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Соберите C++ модуль:
```bash
cd backend/comet_mass
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make
```

## Запуск приложения

```bash
python frontend/main_window.py
```

## Тестирование

### C++ тесты
```bash
cd backend/comet_mass/build
ctest
```

### Python тесты
```bash
pytest tests/
```

## Особенности реализации

### Backend
- Оптимизированные вычисления на C++ (<0.1 сек на расчет)
- Поддержка форматов:
  - Текстовые файлы (.txt)
  - FITS-изображения (.fits)
- Кастомная обработка ошибок

### Frontend
- Интуитивный интерфейс с вкладками
- Подсказки при вводе параметров
- Экспорт результатов в PNG/CSV

## Лицензия

MIT License. Подробнее см. в файле LICENSE.

## Контакты

По вопросам сотрудничества:
- Email: пока хз 
- Telegram: пока хз 

---

**Примечание**: Для работы с FITS-файлами требуется установка библиотеки Astropy:
```bash
pip install astropy
```

Для сборки C++ модуля на Windows используйте:
```bash
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
mingw32-make
```
