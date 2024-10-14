#!/bin/bash
docker rm -f flask-challenge
docker build -t flask-challenge .
docker run --network=host --name=flask-challenge --rm -p 5000:5000 -it flask-challenge
