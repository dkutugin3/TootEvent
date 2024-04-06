#!/bin/bash
cd backend 
echo "SECRET_KEY=fj4tQHvxG55c7srYFSotUv+XHvkchI56GyBRmd9z9AM=
ALGORITHM=HS256
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres" > .env
docker build -t mai_app .
cd ..
docker compose up -d 
open -u http://localhost:8000/docs