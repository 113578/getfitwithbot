FROM python:3.11-slim

WORKDIR /usr/local/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=${PYTHONPATH}
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV OPENWEATHERMAP_TOKEN=${OPENWEATHERMAP_TOKEN}
ENV NUTRITIONIX_ID=${NUTRITIONIX_ID}
ENV NUTRITIONIX_TOKEN=${NUTRITIONIX_TOKEN}
ENV APININJAS_TOKEN=${APININJAS_TOKEN}

CMD ["python", "src/bot.py"]
