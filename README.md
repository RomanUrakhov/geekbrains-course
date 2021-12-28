# Lesson 6 Behavioral patterns

## Что сделано
* Реализован паттерн Стратегия (с интерфейсом `ILogger`)
* Реализован паттерн Observer (уведомление при получении фидбэка)
* Добавлен `JSONSerializer` (работает по адресу `/api/feedback/`)
 

## Установка (локально)

#### requirements
* ставим виртаульное окружение `python -m venv .venv`
* активируем окружение `source .venv/bin/activate`
* ставим зависимости `pip install -r requirements.txt`

#### .env
* Необходимо создать `.env` на основе `.env.dist`
* Установить свое значение `SECRET_TOKEN`
* [OPTIONAL] Установить значение `WSGI_APP_TYPE` (класс приложения)
  * `default` - для экземпляра `Flex` (по-умолчанию)
  * `with_logs` - для экземпляра `FlexWithLogs`
  * `fake` - для экземпляра `FlexFake`

## Запуск (локально)

### gunicorn
`gunicorn run:app`

Апп запустится на `http://127.0.0.1:8000` 
