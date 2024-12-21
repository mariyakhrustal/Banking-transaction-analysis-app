# Проект 1. Приложение для анализа банковских операций.

## Описание:

Проект-приложение для анализа транзакций, которые находятся в Excel-файле. Приложение генерирует JSON-данные для веб-страницы `Главная`.
Предоставляет сервис `Инвесткопилка`. А также формирует отчёты `Траты по категории`.

## Установка:

1. Клонируйте репозиторий:
```
git clone git@github.com:mariyakhrustal/Banking-transaction-analysis-app.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:

1. Перейдите в модуль main.py, который находится в корне проекта в пакете src.
2. Запустите функцию main().
3. Следуйте дальнейшим инструкциям для получения данных на экране.

## Модуль `main.py`
### Описание
Модуль `main.py` - это основной модуль программы, который выполняет запуск и управление основными процессами приложения.
Он отвечает за основную логику проекта с пользователем и связывает функциональности между собой.

## Модуль `decorators.py`
Модуль `decorators.py` содержит декоратор `report`, который будет автоматически регистрировать детали выполнения функций для формирования отчетов,
такие как: передаваемые аргументы, результат выполнения и информация об ошибках. 
Это позволит обеспечить более глубокий контроль и анализ поведения программы в процессе ее выполнения.

### Декоратор `report`
Декоратор для функций-отчетов, который записывает в файл результат, который возвращает функция, формирующая отчет.
Принимает в качестве параметра путь к файлу, в который будут записываться данные отчета. 
Если параметр не был передан, декоратор записывает данные отчета в файл с названием по умолчанию в директорию в корне проекта `reports` в файл `report.log`.

### Пример использования
```
from src.decorators import report

@report()
def example_function(a, b):
    return a + b

result = example_function(2, 4)
```

## Файл .env.sample
### Описание
Файл `.env.sample` — это пример конфигурационного файла для приложения, который содержит список переменных окружения, необходимых для его корректной работы. Этот файл служит шаблоном и не должен использоваться напрямую для запуска приложения.

### Как использовать:
Скопируйте файл `.env.sample` в новый файл с именем .env:
```
cp .env.sample .env
```

Откройте файл `.env` и заполните его значениями, соответствующими вашей среде или проекту:
Укажите значения для переменных, таких как API-ключи, строки подключения к базе данных, настройки сервера и другие параметры, которые могут отличаться в разных средах (например, локальная разработка, тестирование, продакшн).

#### Пример содержимого:
```
# Конфигурация базы данных
DATABASE_HOST=localhost     # Хост для базы данных
DATABASE_USER=username      # Имя пользователя базы данных
DATABASE_PASSWORD=password  # Пароль базы данных
DATABASE_NAME=mydatabase    # Имя базы данных

# API-ключи
API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token_here
```
#### Зачем нужен файл .env
Файл .env позволяет вам хранить чувствительные данные и конфигурационные параметры вне исходного кода проекта. Это помогает:
1. Упростить переносимость приложения между разными средами.
2. Сохранить секретные ключи и другие важные данные в безопасности, исключая их из репозиториев.
- Убедитесь, что файл .env добавлен в .gitignore, чтобы избежать его случайного коммита в репозиторий.

## Логирование 
В проекте используется система логирования для отслеживания важных событий и ошибок. Логирование помогает выявлять проблемы и анализировать поведение приложения.
### Просмотр логов
Логирование поумолчанию записывает сообщения в директорию `logs` в корне проекта. Логирование каждого модуля записывается в соответствующий ему файл.

## Тестирование
### Введение
В данном проекте тестирование проводилось с целью обеспечения корректной работы всех функциональных возможностей.
### Типы тестирования
Модульное тестирование
### Инструменты тестирования
`Pytest`
### Запуск тестов
Для запуска тестов выполните команду:
```
pytest
```
### Проверка покрытия кода
```
pytest --cov
```
Чтобы проверить какие строчки кода не покрыты тестами используйте команду:
```
pytest --cov src --cov-report term-missing
```
### Структура тестов
Тестовые файлы находятся в директории `tests/` и организованы по функциональным модулям.

## Документация:

Для получения дополнительной информации обратитесь к [документации](docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).