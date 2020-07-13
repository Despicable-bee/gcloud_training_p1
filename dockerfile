FROM python:3.7

WORKDIR /google-cloud-training/p1

# Copy over individual files
COPY calculator_server.py .

# Install all the required dependencies
RUN pip3 install -r requirements.txt && \
    python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    calculator.proto

# Run the server
CMD ["python", "calculator_server.py"]

