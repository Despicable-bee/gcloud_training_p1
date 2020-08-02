@ECHO off
ECHO --------------------------------------------
ECHO Generate Owner Key
ECHO [91mWARNING[0m This file gives root
echo   access to your applications, don't use
echo   in production builds
echo Generating owner key...
gcloud iam service-accounts keys create ./owner-key.json ^
    --iam-account owner-key@cloud-training-id.iam.gserviceaccount.com
echo Done
echo --------------------------------------------
PAUSE