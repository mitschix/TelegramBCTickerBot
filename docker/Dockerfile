FROM python:3.14-alpine

WORKDIR /app
COPY src/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src/ .

# SQLite file will live in /data (mounted as volume)
RUN mkdir -p /data

CMD ["python", "bot.py"]
