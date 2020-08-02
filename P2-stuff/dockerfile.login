FROM python:3.8

WORKDIR /google-cloud-training/p2

# Copy over individual files
COPY calculator_login.py calculator_login_helper.py owner-key.json  \
    calculator.proto requirements.txt ./

# Install all the required dependencies
RUN pip3 install -r requirements.txt && \
    python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    calculator.proto

# Run the server
CMD ["python", "calculator_login.py"]

