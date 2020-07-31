#!/bin/bash
# This batch file generates the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'Docker local server'
echo 'Starting up local server...' 
echo "(Use 'docker kill [container-id]' to stop)"
docker run -p 50051:50051 -e PORT=50051 \
    gcr.io/cloud-training-id/calculator-server:latest
echo 'Done'
echo '--------------------------------------------'
exit