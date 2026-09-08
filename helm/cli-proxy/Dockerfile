FROM python:3.14-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py resp.py namespace.py sessions.py main.py ./

# The docs search service. It shares this image rather than getting one of its
# own: it needs the same flask, the same gunicorn and resp.py itself, and a
# third image would be a third thing to build, mirror and carry through the
# air gap. The chart runs it from a separate deployment with its own command,
# so enabling search does not enable the playground or the other way round.
COPY search/__init__.py search/config.py search/paths.py search/product.py \
     search/sources.py search/hierarchy.py search/indexer.py search/query.py \
     search/main.py ./search/

RUN adduser -D appuser
USER appuser

EXPOSE 8090 8091

# One worker, not two: sessions are held in process memory, so a second worker
# gets its own registry and a reader's next command can land on the process that
# has never heard of their session — which breaks MULTI/EXEC and doubles the
# connections. The thread count carries the concurrency the workers used to.
CMD ["gunicorn", "--bind", "0.0.0.0:8090", "--workers", "1", "--worker-class", "gthread", "--threads", "8", "--control-socket", "/tmp/gunicorn.ctl", "main:app"]
