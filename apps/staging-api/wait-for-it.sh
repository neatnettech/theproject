#!/usr/bin/env bash
set -e

hostport="$1"
shift
cmd="$@"

host=$(echo "$hostport" | cut -d: -f1)
port=$(echo "$hostport" | cut -d: -f2)

until nc -z "$host" "$port"; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "✅ Postgres is up - executing command"
exec $cmd