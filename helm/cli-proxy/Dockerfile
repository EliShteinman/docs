FROM python:3.14-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN adduser -D appuser
USER appuser

EXPOSE 8090

CMD ["gunicorn", "--bind", "0.0.0.0:8090", "--workers", "2", "--worker-class", "gthread", "--threads", "4", "--control-socket", "/tmp/gunicorn.ctl", "main:app"]
