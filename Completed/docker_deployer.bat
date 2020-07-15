@ECHO OFF 
:: This batch file deploys the docker container
:: By Harry Nowakowski
TITLE Calculator docker builder
ECHO --------------------------------------------
ECHO Google Cloud training container deployer
ECHO Deploying container...
docker push gcr.io/cloud-training-id/calculator-server:latest

gcloud run deploy calculator-server --image^
 gcr.io/cloud-training-id/calculator-server:latest^
 --platform managed^
 --region australia-southeast1
ECHO Done
ECHO --------------------------------------------
PAUSE