#!/bin/bash
docker rm -f idor-challenge
docker build -t idor-challenge .
docker run --network=host --name=idor-challenge --rm -p 5001:5001 -it idor-challenge
