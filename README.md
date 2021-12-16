# Lesson 3 Template extension

## Что сделано
* Добавлена возможность расширения/включения шаблонов
* Добавлен базовый шаблон
* Добавлен шаблон с меню


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
