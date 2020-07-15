@ECHO OFF 
:: This batch file generates the docker container
:: By Harry Nowakowski
TITLE Calculator docker builder
ECHO --------------------------------------------
ECHO Google Cloud training container builder
ECHO Building container...
CMD /c docker build -f dockerfile ^
    -t gcr.io/cloud-training-id/calculator-server:latest .
ECHO Done
ECHO --------------------------------------------
PAUSE