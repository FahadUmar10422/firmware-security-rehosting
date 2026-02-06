#!/bin/bash

docker build -t group1 -f Dockerfile .
docker run -v .:/workspace -it group1
