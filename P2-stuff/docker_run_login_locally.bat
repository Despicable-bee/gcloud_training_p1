@ECHO OFF 
:: This batch file generates the docker container
:: By Harry Nowakowski
TITLE Calculator docker local server
ECHO --------------------------------------------
ECHO Docker local server
ECHO Starting up local server... 
ECHO (Use 'docker kill [container-id]' to stop)
CMD /c docker run -p 50051:50051 -e PORT=50051 ^
    -e GOOGLE_APPLICATION_CREDENTIALS=/google-cloud-training/p2/owner-key.json ^
    gcr.io/cloud-training-id/calculator-login:latest
    
ECHO Done
ECHO --------------------------------------------
PAUSE