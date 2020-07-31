#!/bin/bash
echo '--------------------------------------------'
echo 'Calculator Protoc Generator'
echo 'Generating client and server stubs...'
python3 -m grpc_tools.protoc --include_imports --include_source_info\
 --proto_path=. --descriptor_set_out=endpoints_api_descriptor.py\
 --python_out=. --grpc_python_out=. calculator.proto
echo 'Done'
echo '--------------------------------------------'
exit 