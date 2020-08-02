#!/bin/bash
# This batch file generates the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'Google Cloud training login container builder'
echo 'Building container...'
docker build -f dockerfile.login \
    -t gcr.io/cloud-training-id/calculator-login:latest .
echo 'Done'
echo '--------------------------------------------'
exit