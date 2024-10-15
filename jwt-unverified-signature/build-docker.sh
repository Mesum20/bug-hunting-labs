#!/bin/bash
docker rm -f flask-jwt-demo
docker build -t flask-jwt-demo .
docker run --network=host --name=flask-jwt-demo --rm -p 5003:5003 -it flask-jwt-demo
