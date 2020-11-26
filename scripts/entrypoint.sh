#!/bin/bash

while ! nc -zvw3 redis 6379; do echo waiting for Redis; sleep 30; done;
echo "Redis is up"

while ! nc -zvw3 postgres 5432; do echo waiting for Postgres; sleep 30; done;
echo "Postgres is up"

exec guicorn wsgi:app --host 0.0.0.0 --port 5000

exec celery --app=fileapi.api.tasks.celery:celeryApp worker -l=${LOG_LEVEL:-INFO} -n worker@%h --concurrency=${CONCURRENCY:-9}