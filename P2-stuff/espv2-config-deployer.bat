@ECHO OFF 
:: This batch file generates the docker container
:: By Harry Nowakowski
TITLE ESPv2 Beta Container Updater
ECHO --------------------------------------------
ECHO ESPv2 Beta Container updater
ECHO Building the updated container... 
CMD /c D:\Git\bin\bash.exe gcloud_build_image.sh -s espv2-beta-test-dmf4chgjea-ts.a.run.app -c 2020-08-02r1 -p cloud-training-id
CMD /c gcloud run deploy espv2-beta-test ^
    --image="gcr.io/cloud-training-id/endpoints-runtime-serverless:2.14.0-espv2-beta-test-dmf4chgjea-ts.a.run.app-2020-08-02r1" ^
    --allow-unauthenticated ^
    --platform managed ^
    --project cloud-training-id
    --region australia-southeast1

ECHO Done
ECHO --------------------------------------------
PAUSE