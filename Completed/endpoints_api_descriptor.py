
Ò
calculator.protoendpoints.calculator"¡
ComputationRequest 
firstNumber (RfirstNumber"
secondNumber (RsecondNumberE
	operation (2'.endpoints.calculator.ComputeOperationsR	operation"ˆ
ComputationResponse$
responseValue (RresponseValueK
responseStatus (2#.endpoints.calculator.ComputeStatusRresponseStatus*D
ComputeOperations
ADD 
SUBTRACT
MULTIPLY

DIVIDE*‰
ComputeStatus
OPERATION_SUCCESSFUL 
UNKNOWN_OPERATION
ILLEGAL_OPERATION
OPERATION_UNSUCCESSFUL
INCORRECT_FORMAT2q
CloudCalculator^
compute(.endpoints.calculator.ComputationRequest).endpoints.calculator.ComputationResponseJ«

 (
±
 2¦******************************************************************************
FILENAME: calculator.proto

AUTHOR: Harry Nowakowski
DESCRIPTION: An API framework for a calculator implemented in the cloud
LICENSE:    
*****************************************************************************


 


  


 

  

  

  


 

 

 

 

 

 

 

 


 


 



 
 " All went smoothly


 

 
5
"( Like when you divide something by zero





*
" User didn't specify numbers





3
"& Something went wrong with the server





7
"* e.g. The user puts a string into a float







  


 

  

  	

  


  

 

 	

 


 

 $

 

 

 "#


! $


!

 "

 "	

 "


 "

#%

#

# 

##$


 & (


 &

  'C

  '

  '#

  '.Abproto3