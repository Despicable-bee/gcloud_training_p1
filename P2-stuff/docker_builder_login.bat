@ECHO OFF 
:: This batch file generates the docker container
:: By Harry Nowakowski
TITLE Calculator docker builder
ECHO --------------------------------------------
ECHO Google Cloud training login container builder
ECHO Building container...
CMD /c docker build -f dockerfile.login ^
    -t gcr.io/cloud-training-id/calculator-login:latest .
ECHO Done
ECHO --------------------------------------------
PAUSE