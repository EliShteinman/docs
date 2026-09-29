FROM python:3.14-alpine

WORKDIR /app

# Built from helm/ (docker build -f search/Dockerfile helm), so resp.py, which
# the CLI image uses as well, lives once in helm/common/.
COPY search/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common/resp.py ./
COPY search/search/__init__.py search/search/config.py search/search/paths.py \
     search/search/product.py search/search/sources.py search/search/hierarchy.py \
     search/search/indexer.py search/search/query.py search/search/main.py ./search/

RUN adduser -D appuser
USER appuser

EXPOSE 8091

# The chart replaces this command: it builds the index with
# `python -m search.indexer` first and serves only once the index exists.
CMD ["gunicorn", "--bind", "0.0.0.0:8091", "--workers", "1", "--worker-class", "gthread", "--threads", "8", "--control-socket", "/tmp/gunicorn-search.ctl", "search.main:app"]
