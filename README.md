FormWizard (бот)

Бот для автоматизированного заполнения шаблонов документов

Запуск локально

Добавляем файл .env на основе .env.example
Устанавливаем UV если отсутствует curl -LsSf https://astral.sh/uv/install.sh | sh
Создаем окружение uv sync
Запускаем PYTHONPATH=. uv run src/main.py
Запуск через DOCKER

Добавляем файл .env на основе .env.example
Собираем образ docker build . -t=form_wizard -f=docker/Dockerfile
Запускаем docker run -d --env-file=.env --name form_wizard form_wizard