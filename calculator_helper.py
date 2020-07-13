from typing import Text
from typing import Optional

import calculator_pb2
import calculator_pb2_grpc

class Calculator_Helper:
    def __init__(self, firstNumber: float, secondNumber: float) -> None:
        """ Sets the operands to be used in the computation """
        """ Sets the ready status based on the inputs """
        if isinstance(firstNumber, float) and isinstance(secondNumber, float):
            self.first = firstNumber
            self.second = secondNumber
            self.operandsReady = True
        else:
            self.operandsReady = False

    def set_operands(self, firstNumber: float, secondNumber: float) -> None:
        """ Sets the operands to be used in the computation """
        """ Sets the ready status based on the inputs """
        if isinstance(firstNumber, float) and isinstance(secondNumber, float):
            self.first = firstNumber
            self.second = secondNumber
            self.operandsReady = True
        else:
            self.operandsReady = False

    def check_operands(self) -> bool:
        """ Checks to see if both operands are valid """
        if isinstance(self.first, float) and isinstance(self.second, float):
            return True
        else:
            return False
    
    def get_operation(self, operation: calculator_pb2.ComputeOperations) -> \
            Optional[object]:
        """ Gets the function that corresponds to the request """
        method = getattr(self, str(operation).lower() + '_operation', 
                lambda: None)
        return method

    def add_operation(self) -> Optional[float]:
        if self.operandsReady:
            return self.first + self.second
        else:
            return None

    def subtract_operation(self) -> Optional[float]:
        if self.operandsReady:
            return self.first - self.second
        else:
            return None

    def multiply_operation(self) -> Optional[float]:
        if self.operandsReady:
            return self.first * self.second
        else:
            return None

    def division_operation(self) -> Optional[float]:
        if self.operandsReady and self.second != 0:
            return self.first / self.second
        else:
            return None