from __future__ import print_function
import logging
import sys

import time
import grpc

import calculator_pb2
import calculator_pb2_grpc

from colours import *

# Host and port for the online server
host = "espv2-beta-test-dmf4chgjea-ts.a.run.app"
port = "443"

# Host and port for the local server
host2 = "localhost"
port2 = '50051'

def local_test():
    """ Runs a battery of tests targeted at a local container """
    channel = grpc.insecure_channel('{}:{}'.format(host2, port2))

    # Setup a new client stub
    stub = calculator_pb2_grpc.CloudLoginStub(channel)

    # Test the local server container

    # Test the create account mechanism
    print("Create Account test ...", end=" ")
    response = stub.create_account(calculator_pb2.CreateAccountRequest(
        username="BlueSoldier09",
        password="1111"
    ))
    calculator_login_junit_test(calculator_pb2.ACCOUNT_CREATION_SUCCESSFUL,
            response.status)
    
    jwt = response.jwt
    refresh = response.refresh
    print("----- OUR JWT -----")
    print("{}".format(jwt))
    print("")
    print("----- OUR REFRESH -----")
    print("{}".format(refresh))
    print("----- END -----")
    print("")

    # Test the login mechanism
    print("Login Account test ...", end=" ")
    response = stub.login(calculator_pb2.LoginRequest(
        username="BlueSoldier09",
        password="1111"
    ))
    calculator_login_junit_test(calculator_pb2.LOGIN_SUCCESSFUL,
            response.status)
    
    # Test Account already exists
    print("Account already exists test ...", end=" ")
    response = stub.create_account(calculator_pb2.CreateAccountRequest(
        username="BlueSoldier09",
        password="1111"
    ))
    calculator_login_junit_test(calculator_pb2.ACCOUNT_CREATION_UNSUCCESSFUL,
            response.status)

    # Test Login doesn't exist
    print("Login doesn't exist test ...", end=" ")
    response = stub.login(calculator_pb2.LoginRequest(
        username="BlueSpy09",
        password="1111"
    ))
    calculator_login_junit_test(calculator_pb2.LOGIN_UNSUCCESSFUL,
            response.status)
    
    # Test the refresh thing
    print("Test refresh token ...", end=" ")
    response = stub.refresh(calculator_pb2.RefreshRequest(
        jwt=jwt,
        refresh=refresh,
        username="BlueSoldier09"
    ))
    calculator_login_junit_test(calculator_pb2.REFRESH_TOKEN_VALID,
        response.status)

    # Test delete account
    print("Delete account test ...", end=" ")
    response = stub.terminateAccount(calculator_pb2.terminateRequest(
        username="BlueSoldier09",
        password="1111"
    ))
    calculator_login_junit_test(calculator_pb2.HASTA_LA_VISTA_BABY,
            response.status)

    # Test delete account that doesn't exist
    print("Delete account non-existent test ...", end=" ")
    response = stub.terminateAccount(calculator_pb2.terminateRequest(
        username="BlueSoldier09",
        password="1111"
    ))
    calculator_login_junit_test(calculator_pb2.I_DONT_KNOW,
            response.status)

    

    # test_battery(stub, 'local')

def server_test():
    """ Runs the same battery of tests as the local test, but on the server """
    f = open('roots.pem', 'rb')
    creds = grpc.ssl_channel_credentials(f.read())
    channel = grpc.secure_channel('{}:{}'.format(host, port), creds)

    # Setup a new client stub
    stub = calculator_pb2_grpc.CloudLoginStub(channel)
    calcStub = calculator_pb2_grpc.CloudCalculatorStub(channel)
    
    # Place where we put the jwt
    metadata = []

    # Start by creating an account
    # Test the create account mechanism
    print("Create Account test ...", end=" ")
    response = stub.create_account(calculator_pb2.CreateAccountRequest(
        username="BlueSoldier09",
        password="1111"
    ))
    returnStatus = calculator_login_junit_test(calculator_pb2.ACCOUNT_CREATION_SUCCESSFUL,
            response.status)
    jwt = response.jwt
    refresh = response.refresh

    if returnStatus:
        # Test ESPv2 container
        metadata.append(('authorization', "Bearer " + response.jwt))
        print("Compute test through the ESPv2 container ...", end=" ")
        response = calcStub.compute(calculator_pb2.ComputationRequest(
                firstNumber=1,
                secondNumber=2,
                operation=calculator_pb2.ADD
            ), metadata=metadata
        )
        value = response.responseValue
        status = response.responseStatus
        calculator_login_junit_test(calculator_pb2.OPERATION_SUCCESSFUL, status)
        
        # Expire token
        print("Waiting for JWT to expire...")
        for i in range(0,35):
            print("\r>> Expire progress: {}%".format(round((i/34)*100)), end='')
            time.sleep(1)
        print("\r>> Done                                ")
        # Test expired token recovery
        print("Compute test with expired token...", end=" ")
        try:
            response = calcStub.compute(calculator_pb2.ComputationRequest(
                    firstNumber=1,
                    secondNumber=2,
                    operation=calculator_pb2.ADD
                ), metadata=metadata
            )
            print("Result: {}".format(response.responseStatus))
        except grpc.RpcError as e:
            statusCode = e.code()
            if statusCode.name == 'UNAUTHENTICATED':
                sys.stdout.write(GREEN)
                print("OK")
            else:
                sys.stdout.write(RED)
                print("Failed!, STATUS: {}".format(statusCode.name))
            sys.stdout.write(RESET)
        except Exception as e:
            print(e)
        
        # Get a new JWT with your refresh token
        # Test the refresh thing
        print("Test refresh token ...", end=" ")
        response = stub.refresh(calculator_pb2.RefreshRequest(
            jwt=jwt,
            refresh=refresh,
            username="BlueSoldier09"
        ))
        newJwt = response.new_jwt
        calculator_login_junit_test(calculator_pb2.REFRESH_TOKEN_VALID,
            response.status)

        metadata.clear()
        metadata.append(('authorization', "Bearer " + newJwt))
        # Wrap this up with an account deleteion
        print("Delete account test ...", end=" ")
        response = stub.terminateAccount(calculator_pb2.terminateRequest(
            username="BlueSoldier09",
            password="1111"
        ), metadata=metadata)
        calculator_login_junit_test(calculator_pb2.HASTA_LA_VISTA_BABY,
                response.status)

        # value = response.responseValue
        # status = response.responseStatus
        # calculator_login_junit_test(calculator_pb2.OPERATION_SUCCESSFUL, status)
    else:
        print("Error")


    # Test the deployed server container
    # test_battery(stub, 'server')

def calculator_login_junit_test(correctStatus: int, givenStatus: int) -> bool:
    if correctStatus != givenStatus:
        sys.stdout.write(RED)
        print("Failed!, STATUS: {}".format(givenStatus))
        returnStatus = False
    else:
        sys.stdout.write(GREEN)
        print("OK")
        returnStatus = True
    sys.stdout.write(RESET)
    return returnStatus

def test_battery(stub: calculator_pb2_grpc.CloudLoginStub, type: str):
    pass

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