#!/bin/bash

#local에서
if [ $1 == "build" ]; then
  sudo docker build -t hungkunge/keywordkatch_docker -f docker/Dockerfile .
elif [ $1 == "reset" ]; then
  sudo docker rm -f $(docker ps -qa);
  sudo docker image rm -f $(docker image ls -q);
elif [ $1 == "push" ]; then
  docker push hungkunge/keywordkatch_docker
#ec2에서
elif [ $1 == "pull" ]; then
  sudo docker pull hungkunge/keywordkatch_docker
elif [ $1 == "run" ]; then
  sudo docker run -d -p 5001:5001 hungkunge/keywordkatch_docker
elif [ $1 == "stop" ]; then
  sudo docker stop $(sudo docker ps -aq)
else
  echo "wrong command!"
fi