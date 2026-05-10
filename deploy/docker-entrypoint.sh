#!/bin/bash
set -e

# 启动 nginx
nginx

# 启动后端
cd /app/src/backend
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
