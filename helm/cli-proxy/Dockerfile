FROM python:3.14-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN adduser -D appuser
USER appuser

EXPOSE 8090

# One worker, not two: sessions are held in process memory, so a second worker
# gets its own registry and a reader's next command can land on the process that
# has never heard of their session — which breaks MULTI/EXEC and doubles the
# connections. The thread count carries the concurrency the workers used to.
CMD ["gunicorn", "--bind", "0.0.0.0:8090", "--workers", "1", "--worker-class", "gthread", "--threads", "8", "--control-socket", "/tmp/gunicorn.ctl", "main:app"]
