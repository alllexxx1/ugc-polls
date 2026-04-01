FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
RUN pip install -e .

COPY src/ ./src/

EXPOSE 8000

CMD sh -c "python src/manage.py migrate && python src/manage.py seed_data && python src/manage.py runserver 0.0.0.0:8000"
