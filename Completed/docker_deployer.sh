#!/bin/bash
# This batch file deploys the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'Google Cloud training container deployer'
echo 'Deploying container...'
docker push gcr.io/cloud-training-id/calculator-server:latest

gcloud run deploy calculator-server --image\
 gcr.io/cloud-training-id/calculator-server:latest\
 --platform managed\
 --region australia-southeast1
echo 'Done'
echo '--------------------------------------------'
exit