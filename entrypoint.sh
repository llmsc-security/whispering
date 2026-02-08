#!/bin/bash
set -e

echo "Starting Whispering Tiger audio processing..."

cd /app

# Run audioWhisper.py with reasonable defaults for container
# Using websocket on port 5000 with 0.0.0.0 to bind to all interfaces
exec python audioWhisper.py --websocket_ip 0.0.0.0 --websocket_port 5000 "$@"
