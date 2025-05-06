FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    APP_ENV=prod

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && apt-get clean

WORKDIR /app

# Copy dependencies first for better caching
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Add wait-for-it
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

EXPOSE 8000

CMD ["sh", "-c", "\
  wait-for-it.sh db:5432 -- \
  && if [ \"$APP_ENV\" = \"dev\" ]; then \
       uvicorn run:app --host 0.0.0.0 --port 8000 --reload; \
     else \
       uvicorn run:app --host 0.0.0.0 --port 8000; \
     fi"]