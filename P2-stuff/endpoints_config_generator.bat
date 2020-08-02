@ECHO OFF 
:: This batch file generates the docker container
:: By Harry Nowakowski
TITLE Endpoints configuration generator
ECHO --------------------------------------------
ECHO Endpoints config generator
ECHO Generating your endpoints config... 
CMD /c gcloud endpoints services ^
        deploy endpoints_api_descriptor.pb api_config.yaml
ECHO Done
ECHO --------------------------------------------
PAUSE