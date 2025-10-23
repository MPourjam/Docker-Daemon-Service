import os, docker
from celery import Celery
from celery.schedules import crontab


BROKER = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

app = Celery("tasks", broker=BROKER, backend=BACKEND)


@app.task
def heartbeat_container():
    """Start a short container on the remote daemon as a heartbeat"""
    print("[heartbeat] starting container on remote daemon")
    client = docker.from_env()  # uses DOCKER_HOST, DOCKER_TLS_VERIFY, DOCKER_CERT_PATH
    container = client.containers.run(
        "alpine:3.20",
        ["sh", "-c", "echo heartbeat from $(hostname) && sleep 5"],
        detach=True,
        remove=True,
        network_disabled=True,
        user="root",
    )
    # NOTE: The task might fail due to docker-daemon service being set up and thus not reachable yet.
    print("[heartbeat] started:", container.short_id)
    result = container.wait()
    logs = container.logs().decode().strip()
    print("[heartbeat] exit:", result, "logs:", logs)
    return {"status": result, "logs": logs}

# Celery Beat schedule (recurrent task setup)
app.conf.beat_schedule = {
    "run-heartbeat-every-30-seconds": {
        "task": "tasks.heartbeat_container",
        "schedule": 30.0,  # seconds
    },
}

app.conf.timezone = "UTC"
