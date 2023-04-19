FROM python:3.9.16-bullseye

RUN pip install poetry
WORKDIR /cinna-bot
COPY . /cinna-bot
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
CMD python main.py