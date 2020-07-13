@ECHO OFF 
:: This batch file deploys the docker container
:: By Harry Nowakowski
TITLE Calculator docker builder
ECHO --------------------------------------------
ECHO Google Cloud training container deployer
ECHO Deploying container...
:: The CMD part causes the gcloud function to run in its own nested environment
::  which won't interfere with the top level environment.
CMD /c gcloud config set run/region australia-southeast1
ECHO Done
ECHO Here is a summary of your config info
CMD /c gcloud config list
ECHO --------------------------------------------
PAUSE