@ECHO OFF 
:: This batch file deploys the docker container
:: By Harry Nowakowski
TITLE Calculator docker builder
ECHO --------------------------------------------
ECHO Google Cloud training login container deployer
ECHO Deploying container...
docker push gcr.io/cloud-training-id/calculator-login:latest

gcloud run deploy calculator-login --image^
 gcr.io/cloud-training-id/calculator-login:latest^
 --platform managed^
 --region australia-southeast1
ECHO Done
ECHO --------------------------------------------
PAUSE