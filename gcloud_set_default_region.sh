#!/bin/bash 
# This batch file deploys the docker container
# By Harry Nowakowski
echo '--------------------------------------------'
echo 'Google Cloud Region setter'
echo 'Setting region...'
# The CMD part causes the gcloud function to run in its own 
# nested environment
#  which won't interfere with the top level environment.
gcloud config set run/region australia-southeast1
echo 'Done'
echo 'Here is a summary of your config info'
gcloud config list
echo '--------------------------------------------'
exit