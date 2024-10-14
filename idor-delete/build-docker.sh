#!/bin/bash
docker rm -f flask-idor-app
docker build -t flask-idor-app .
docker run --network=host --name=flask-idor-app --rm -p 5002:5002 -it flask-idor-app
