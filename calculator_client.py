from __future__ import print_function
import logging

import grpc

import calculator_pb2
import calculator_pb2_grpc

host2 = "localhost"
port2 = '50051'

def local_test():
    print("Hello")
    """ Runs a battery of tests targeted at a local container """
    channel = grpc.insecure_channel('{}:{}'.format(host2, port2))

    # Setup a new client stub
    stub = calculator_pb2_grpc.CloudCalculatorStub(channel)

    # Get a response back from the server
    response = stub.compute(calculator_pb2.ComputationRequest(
        firstNumber=1.0,
        secondNumber=2.0,
        operation=calculator_pb2.ComputeOperations.ADD
    ))

    # print the response
    print(response)

if __name__ == '__main__':
    local_test()