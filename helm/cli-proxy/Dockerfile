FROM python:3.14-alpine

WORKDIR /app

# Built from helm/ (docker build -f cli-proxy/Dockerfile helm), so resp.py,
# which the search image uses as well, lives once in helm/common/.
COPY cli-proxy/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common/resp.py ./
COPY cli-proxy/config.py cli-proxy/namespace.py cli-proxy/sessions.py cli-proxy/main.py ./

# A numeric UID: with a name, a kubelet enforcing runAsNonRoot cannot tell the
# user is not root and refuses to start the container. OpenShift assigns its
# own UID from the namespace's range either way.
RUN adduser -D -u 10001 appuser
USER 10001

EXPOSE 8090

# One worker, not two: sessions are held in process memory, so a second worker
# gets its own registry and a reader's next command can land on the process that
# has never heard of their session — which breaks MULTI/EXEC and doubles the
# connections. The thread count carries the concurrency the workers used to.
CMD ["gunicorn", "--bind", "0.0.0.0:8090", "--workers", "1", "--worker-class", "gthread", "--threads", "8", "--control-socket", "/tmp/gunicorn.ctl", "main:app"]
