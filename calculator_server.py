import logging
import os
from concurrent import futures

from typing import Text

import calculator_pb2
import calculator_pb2_grpc

import grpc

import calculator_helper

_PORT = os.environ["PORT"]

class CloudCalculator(calculator_pb2_grpc.CloudCalculatorServicer):
    def compute(self, 
            request: calculator_pb2.ComputationRequest, 
            context: grpc.ServicerContext) -> calculator_pb2.ComputationResponse:
        """ Performs a specific computation """
        # Initialise the calculator helper
        ch = calculator_helper.Calculator_Helper(request.firstNumber,
                request.secondNumber)
        # Set Default return values
        returnStatus = calculator_pb2.ComputeStatus.OPERATION_UNSUCCESSFUL
        returnValue = 0
        try:
            # Determine what operation we want to perform
            method = ch.get_operation(request.operation)
            if method == None:
                # Unknown/Illegal operation
                returnStatus = calculator_pb2.ComputeStatus.UNKNOWN_OPERATION
            else:
                # Call the function
                returnValue = method()
                if returnValue == None:
                    if not ch.check_operands():
                        # Either information missing or wrong format 
                        # (i.e. string when it should be a float)
                        returnStatus = calculator_pb2.ComputeStatus.\
                                INCORRECT_FORMAT
                    elif request.operation == calculator_pb2.ComputeStatus.\
                            DIVIDE and request.secondNumber == 0:
                        # Divide by zero case
                        returnStatus = calculator_pb2.ComputeStatus.\
                                ILLEGAL_OPERATION
                    returnValue = 0
                else:
                    returnStatus = calculator_pb2.ComputeStatus.\
                            OPERATION_SUCCESSFUL
        except Exception as e:
            returnStatus = calculator_pb2.ComputeStatus.OPERATION_UNSUCCESSFUL
            returnValue = 0
        
        # Return the result
        return calculator_pb2.ComputationResponse(
            responseStatus=returnStatus,
            responseValue=returnValue
<<<<<<< HEAD
        )
=======
        )

def _server(port: Text):
    bind_address = f"[::]:{port}"
    server = grpc.server(futures.ThreadPoolExecutor())
    calculator_pb2_grpc.add_CloudCalculatorServicer_to_server(
        CloudCalculator(), server)
    server.add_insecure_port(bind_address)
    server.start()
    logging.info("Listening on %s.", bind_address)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _server(_PORT)
>>>>>>> 833775cbe70facda16858660f9845c2f94925c10
