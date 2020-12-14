#!/bin/bash
app="docker.webapp.dcm"
docker build -t ${app} .
docker run -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}