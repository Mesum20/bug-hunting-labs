#!/bin/bash
docker rm -f flask-jwt-challenge
docker build -t flask-jwt-challenge .
docker run --network=host --name=flask-jwt-challenge --rm -p 5004:5004 -it flask-jwt-challenge
