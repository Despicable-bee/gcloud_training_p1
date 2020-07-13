from __future__ import print_function
import logging
import sys

import grpc

import calculator_pb2
import calculator_pb2_grpc

# Host and port for the online server
host = ""
port = ""

# Host and port for the local server
host2 = "localhost"
port2 = '50051'

def local_test():
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

def server_test():
    """ Runs the same battery of tests as the local test, but on the server """
    pass


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "local":
        local_test()
    elif len(sys.argv) == 2 and sys.argv[1] == "server":
        server_test()
    else:
        print("------------------- [ PARAMETER ERROR ]---------------------")
        print("")
        print("Incorrect input parameters, please use the following format:")
        print("")
        print("./calculator_client.py local|server")
        print("")
        print("------------------------------------------------------------")