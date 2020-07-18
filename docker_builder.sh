#!/bin/bash
# This batch file generates the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'Google Cloud training container builder'
echo 'Building container...'
docker build -f dockerfile \
    -t gcr.io/cloud-training-id/calculator-server:latest .
echo 'Done'
echo '--------------------------------------------'
exit