# Lesson 5 Structural patterns

## Что сделано
* Реализован Decorator:  
  * flask-like `@route('/')`
  * для профилирования `@profile`

## Установка (локально)

#### requirements
* ставим виртаульное окружение `python -m venv .venv`
* активируем окружение `source .venv/bin/activate`
* ставим зависимости `pip install -r requirements.txt`

#### .env
* Необходимо создать `.env` на основе `.env.dist`
* Установить свое значение `SECRET_TOKEN`

## Запуск (локально)

### gunicorn
`gunicorn run:app`

Апп запустится на `http://127.0.0.1:8000` 
