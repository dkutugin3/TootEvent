#!/bin/bash
cd backend 
docker build -t mai_app .
cd ..
docker compose up -d 