# License: MIT
Copyright 2024 [vladislawzero@gmail.com](mailto:vladislawzero@gmail.com) | discord: _zener_dioder | [https://github.com/SchottkyDi0de](https://github.com/SchottkyDi0de)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This license applies to all files in this project that contain Python source code unless otherwise specified!

# Введение:
LocalSession - программа - оверлей для игр World of Taks Blitz | Tanks Blitz позволяющая выводить сессионные данные на экран не используя игровой API а только считывая игровые реплеи, что означает гарантированную работоспособность вне зависимости от состояния игрового API.
# Возможности:
- Моментальное обновление статистики после завершения боя
- Возможность настраивать внешний вид оверлея, менять тексты и т.д.
- Отложенная проверка реплеев (Когда вы выходите из боя который не завершён создаётся реплей без результатов боя, программа откладывает парсинг такого реплея до тех пор пока не завершится бой)
- Сброс статистики в любой момент
# Настройка:
- Скачать программу или собрать из исходников.
- Открыть программу и зайти в настройки.
- Указать папку с реплеями игры (можно легко найти если из игры экспортировать реплей)
- Пролистать в окне с настройками в самый низ и нажать кнопку сохранения настроек.
- Перезапустить программу.

После перезапуска всё должно работать корректно. Не забудьте в игре включить запись реплеев и установить максимальный лимит реплеев (если позволяет место на накопителе)
# Сборка:
1 - Скачать репозиторий

2 - Настроить виртуальное окружение:

```
python -m venv venv
```
далее
```
venv/scripts/activate
```
После настройки окружения нужно установить зависимости
```
pip install -r requirements.txt
```
Далее запускаем сборщик который есть в зависимостях
```
auto-py-to-exe
```
- Импортируем конфигурацию сборки из папки `build`
- Собираем, результат будет в папке `output`
# Скачать:
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white&link=https://github.com/SchottkyDi0de/LocalSession/releases/tag/stable)
