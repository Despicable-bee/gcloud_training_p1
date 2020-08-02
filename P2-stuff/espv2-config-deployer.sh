#!/bin/bash
# This batch file generates the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'ESPv2 Beta Container updater'
echo 'Building the updated container...'
gcloud_build_image.sh -s espv2-beta-test-dmf4chgjea-ts.a.run.app \
    -c 2020-08-01r0 \
    -p cloud-training-id

gcloud run deploy espv2-beta-test \
    --image="gcr.io/cloud-training-id/endpoint-runtime-serverless:espv2-beta-test-dmf4chgjea-ts.a.run.app-2020-08-01r0" \
    --allow-unauthenticated \
    --platform managed \
    --project cloud-training-id
echo 'Done'
echo '--------------------------------------------'
exit