#!/bin/bash
docker rm -f flask-jwt-app
docker build -t flask-jwt-app .
docker run --network=host --name=flask-jwt-app --rm -p 5005:5005 -it flask-jwt-app
