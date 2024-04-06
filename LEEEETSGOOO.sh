#!/bin/bash
cd backend 
docker build -t mai_app .
cd ..
docker compose up -d 
open -u http://localhost:8000/docs