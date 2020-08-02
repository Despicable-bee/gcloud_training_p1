"""
    Filename: calculator_login.py
    Description: Contains the classes and methods that implement the login
            API as outlined in the UsrLogin section of the pluto-website.proto
            file.
    Author: Harry Nowakowski
    License: Property of Momo Money Australia LTD
"""

import logging
import os
from concurrent import futures

from typing import Text
import calculator_pb2
import calculator_pb2_grpc
import grpc

# JWT stuff
from jwcrypto import jwt, jwk
import uuid

# Date and time information
from datetime import datetime

from calculator_login_helper import Calculator_Login_Helper

# Internet get stuff
import urllib.request, json, requests

# Environment variable specified on startup for port assigned to _PORT
_PORT = os.environ["PORT"]

# Token lifetime (30 seconds)
_TOKEN_LIFETIME = 30

# URL for the public key
jwk_public_url = ""

class CloudLogin(calculator_pb2_grpc.CloudLoginServicer):
    def login(self,
            request: calculator_pb2.LoginRequest,
            context: grpc.ServicerContext) -> None:
        """
        Checks to see if the users credentials are in the database, if so, 
            issue said user a JWT.
        """
        jwt = ""
        refresh = ""
        logging.info("--- Login ---")
        clh = Calculator_Login_Helper(request.username, request.password)
        try:
            if request.username == "" or request.password == "" or \
                    not clh.verify_credentials():
                # User has provided illegal input or doesn't exist
                status = calculator_pb2.LOGIN_UNSUCCESSFUL
                logging.info("Login unsuccessful")
            else:
                # User exists, hence return a valid JWT and a refresh token
                jwt, refresh = clh.generate_jwt(False)
                status = calculator_pb2.LOGIN_SUCCESSFUL
                logging.info("Login successful")
        except Exception as e:
            # Right now all this does is log the error, In future you should
            # figure out what kind of errors are thrown and modify this with a
            # Several exception block statement.
            logging.info("%s", e)
            status = calculator_pb2.LOGIN_ERROR
        # Return the response
        logging.info("--- Done ---")
        return calculator_pb2.LoginResponse(
            jwt=jwt,
            refresh=refresh,
            status=status
        )
    
    def create_account(self,
            request: calculator_pb2.CreateAccountRequest,
            context: grpc.ServicerContext) -> None:
        """
        Creates an account for a user, issues a JWT if the account creation was
        successful.
        """
        clh = Calculator_Login_Helper(request.username, request.password)
        jwt = ""
        refresh = ""
        logging.info("--- Create Account ---")
        logging.info("%s %s", request.username, request.password)
        try:
            if request.username == "" or request.password == "" or \
                    clh.verify_credentials():
                # User has provided illegal input or already exists
                status = calculator_pb2.ACCOUNT_CREATION_UNSUCCESSFUL
                logging.info("Account creation unsuccessful")
            else:
                # Username doesn't exist, create a new account and return a jwt and
                #   refresh token
                clh.create_new_account()
                jwt, refresh = clh.generate_jwt(True)
                status = calculator_pb2.ACCOUNT_CREATION_SUCCESSFUL
                logging.info("Account creation successful")
        except Exception as e:
            # Right now all this does is log the error, In future you should
            # figure out what kind of errors are thrown and modify this with a
            # Several exception block statement.
            logging.info("%s", e)
            status = calculator_pb2.ACCOUNT_CREATION_ERROR
        logging.info("Status: %r", status)
        logging.info("--- Done ---")
        return calculator_pb2.CreateAccountResponse(
            jwt=jwt,
            refresh=refresh,
            status=status
        )
    
    def terminateAccount(self,
            request: calculator_pb2.terminateRequest,
            context: grpc.ServicerContext) -> None:
        """
        Deletes the specified account
        """
        clh = Calculator_Login_Helper(request.username, request.password)
        logging.info("--- terminate account ---")
        try:
            if request.username == "" or request.password == "" or \
                   not clh.verify_credentials():
                status = calculator_pb2.I_DONT_KNOW
                logging.info("termination unsuccessful")
            else:
                if clh.terminate_account():
                    status = calculator_pb2.HASTA_LA_VISTA_BABY
                    logging.info("termination successful")
                else:
                    status = calculator_pb2.I_DONT_KNOW
                    logging.info("termination unsuccessful")
        except Exception as e:
            logging.info("%s",e)
            status = calculator_pb2.T_1000_SYS_ERR
        logging.info("--- Done ---")
        return calculator_pb2.terminateResponse(status=status)
    
    def refresh(self,
            request: calculator_pb2.RefreshRequest,
            context: grpc.ServicerContext) -> None:
        """
        Checks whether the given token is valid, if so it issues a new one
        """
        clh = Calculator_Login_Helper(request.username, "")
        output = clh.verify_jwt(request.jwt)
        logging.info(output)
        if not output:
            # Token is not valid, do not check refresh token
            return calculator_pb2.RefreshResponse(new_jwt="", 
                    status=calculator_pb2.REFRESH_TOKEN_INVALID)
        # Token is valid, now just check refresh token
        if not clh.verify_refresh(request.refresh):
            # Refresh token is not valid or username doesn't match
            return calculator_pb2.RefreshResponse(new_jwt="", 
                    status=calculator_pb2.REFRESH_TOKEN_INVALID)
        # Everything matches, let's get this person a new token
        newJwt, dummy = clh.generate_jwt(False)
        return calculator_pb2.RefreshResponse(new_jwt=newJwt, 
                    status=calculator_pb2.REFRESH_TOKEN_VALID)

        

def _server(port: Text):
    bind_address = f"[::]:{port}"
    server = grpc.server(futures.ThreadPoolExecutor())
    calculator_pb2_grpc.add_CloudLoginServicer_to_server(
        CloudLogin(), server)
    server.add_insecure_port(bind_address)
    server.start()
    logging.info("Listening on %s.", bind_address)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _server(_PORT)