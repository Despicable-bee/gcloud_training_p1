from __future__ import print_function
import logging
import sys

import time
import grpc

import calculator_pb2
import calculator_pb2_grpc

from colours import *
from calculator_enums import *

# Host and port for the online server
host = "calculator-server-abcdefg-ts.a.run.app"
port = "443"

# Host and port for the local server
host2 = "localhost"
port2 = '50051'

def calculator_junit_test(correctStatus: int, correctValue: float, 
        stub: calculator_pb2_grpc.CloudCalculatorStub, inputArg1: float, inputArg2: float,
        inputOperation: calculator_pb2.ComputeOperations):
    """ junit test format for testing whether an expected value is correct or not """
    response = stub.compute(calculator_pb2.ComputationRequest(
        firstNumber=inputArg1,
        secondNumber=inputArg2,
        operation=inputOperation
    ))
    value = response.responseValue
    status = response.responseStatus

    if correctStatus != status or correctValue != value:
        sys.stdout.write(RED)
        print("Failed!, STATUS: {}, VALUE: {}".format(status, value))
    else:
        sys.stdout.write(GREEN)
        print("OK")
    sys.stdout.write(RESET)

def local_test():
    """ Runs a battery of tests targeted at a local container """
    channel = grpc.insecure_channel('{}:{}'.format(host2, port2))

    # Setup a new client stub
    stub = calculator_pb2_grpc.CloudCalculatorStub(channel)

    # Test the local server container
    test_battery(stub, 'local')

def server_test():
    """ Runs the same battery of tests as the local test, but on the server """
    f = open('roots.pem', 'rb')
    creds = grpc.ssl_channel_credentials(f.read())
    channel = grpc.secure_channel('{}:{}'.format(host, port), creds)

    # Setup a new client stub
    stub = calculator_pb2_grpc.CloudCalculatorStub(channel)

    # Test the deployed server container
    test_battery(stub, 'server')

def test_battery(stub: calculator_pb2_grpc.CloudCalculatorStub, type: str):
    """ A battery of tests for our calculator application """
    # Get a response back from the server
    print("-------------- [ Calculator tests ] ----------------------")
    print("")
    print("Addition test:")
    print("1 + 2 = 3 ...", end=" ")
    send_millis = 0
    recv_millis = 0
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 3.0,
            stub, 1.0, 2.0, calculator_pb2.ComputeOperations.ADD)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))

    print("-3 + -2 = -5 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, -5.0,
            stub, -3.0, -2.0, calculator_pb2.ComputeOperations.ADD)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    
    print("0 + 0 = 0 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 0.0,
            stub, 0.0, 0.0, calculator_pb2.ComputeOperations.ADD)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))

    print("")
    print("Subtraction test:")
    print("1 - 2 = -1 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, -1.0,
            stub, 1.0, 2.0, calculator_pb2.ComputeOperations.SUBTRACT)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))

    print("-3 - -2 = -1 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, -1.0,
            stub, -3.0, -2.0, calculator_pb2.ComputeOperations.SUBTRACT)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))

    print("0 - 0 = 0...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 0.0,
            stub, 0.0, 0.0, calculator_pb2.ComputeOperations.SUBTRACT)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))

    print("")
    print("Multiplication test:")
    print("4 * -12 = -48 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, -48.0,
            stub, 4.0, -12.0, calculator_pb2.ComputeOperations.MULTIPLY)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    print("4 * 0 = 0 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 0.0,
            stub, 4.0, 0.0, calculator_pb2.ComputeOperations.MULTIPLY)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    print("420 * 69 =  ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 28980.0,
            stub, 420.0, 69.0, calculator_pb2.ComputeOperations.MULTIPLY)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    
    print("")
    print("Division test:")
    print("3 / 4 = 0.75 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 0.75,
            stub, 3, 4, calculator_pb2.ComputeOperations.DIVIDE)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    print("10 / 5 = 2.0 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 2.0,
            stub, 10, 5, calculator_pb2.ComputeOperations.DIVIDE)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    print("1 / 4 = 0.25 ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.OPERATION_SUCCESSFUL, 0.25,
            stub, 1, 4, calculator_pb2.ComputeOperations.DIVIDE)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    
    print("")
    print("Error test:")
    print("3 / 0 = err ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.ILLEGAL_OPERATION, 0.0,
            stub, 3, 0, calculator_pb2.ComputeOperations.DIVIDE)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))
    print("0 / 0 = err ...", end=" ")
    if(type == 'server'):
        send_millis = int(round(time.time() * 1000))
    calculator_junit_test(calculator_pb2.ComputeStatus.ILLEGAL_OPERATION, 0.0,
            stub, 0, 0, calculator_pb2.ComputeOperations.DIVIDE)
    if(type == 'server'):
        recv_millis = int(round(time.time() * 1000))
        print("Latency: {}ms".format(recv_millis - send_millis))




if __name__ == '__main__':
    print("Hello")
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