#!/bin/bash
# This batch file generates the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'ESPv2 Beta Container init'
echo 'Deploying base ESPv2 Beta container...'
gcloud run deploy espv2-beta-test \
    --image="gcr.io/endpoints-release/endpoints-runtime-serverless:2" \
    --allow-unauthenticated \
    --platform managed \
    --project=cloud-training-id
echo 'Done'
echo '--------------------------------------------'
exit