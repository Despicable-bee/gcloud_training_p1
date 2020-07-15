@ECHO OFF 
:: This batch file generates the client and server API descriptors required 
::  for gRPC communication.
:: By Harry Nowakowski
TITLE Calculator Protoc Generator
ECHO --------------------------------------------
ECHO Calculator Protoc Generator
ECHO Generating client and server stubs...
python -m grpc_tools.protoc --include_imports --include_source_info^
 --proto_path=. --descriptor_set_out=endpoints_api_descriptor.py^
 --python_out=. --grpc_python_out=. calculator.proto
ECHO Done
ECHO --------------------------------------------
PAUSE