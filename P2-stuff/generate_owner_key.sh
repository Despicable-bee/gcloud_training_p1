#!/bin/bash
# This batch file generates the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'Generate Owner Key'
echo -e "\e[91mWARNING\e[0m This file gives root"
echo "  access to your applications, don't use"
echo "  in production builds"
echo 'Generating owner key...'
gcloud iam service-accounts keys create ~/owner-key.json \
    --iam-account owner-account@cloud-training-id.iam.gserviceaccount.com
echo 'Done'
echo '--------------------------------------------'
exit