FROM python:3.11-slim

WORKDIR /usr/local/app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir --upgrade pip==24.3.1 \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ENV PYTHONPATH=${PYTHONPATH}
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV OPENWEATHERMAP_TOKEN=${OPENWEATHERMAP_TOKEN}
ENV NUTRITIONIX_ID=${NUTRITIONIX_ID}
ENV NUTRITIONIX_TOKEN=${NUTRITIONIX_TOKEN}
ENV APININJAS_TOKEN=${APININJAS_TOKEN}

CMD ["python", "src/bot.py"]
