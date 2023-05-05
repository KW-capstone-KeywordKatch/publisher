#!/bin/bash

docker rm -f $(docker ps -qa);
docker image rm -f $(docker image ls -q);