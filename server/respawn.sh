#!/bin/bash

until python server.py; do
    echo "server crashed. exit code: $?. Respawning..." >&2
    sleep 1
done
