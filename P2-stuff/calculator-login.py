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

# Token lifetime (1 hour)
_TOKEN_LIFETIME = 60*60

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
        status = 0
        clh = Calculator_Login_Helper(request.username, request.password)
        try:
            if request.username == "" or request.password == "" or \
                    not clh.verify_credentials():
                # User has provided illegal input or doesn't exist
                status = calculator_pb2.LOGIN_UNSUCCESSFUL
            else:
                # User exists, hence return a valid JWT and a refresh token
                jwt, refresh = clh.generate_jwt()
                status = calculator_pb2.LOGIN_SUCCESSFUL
        except Exception as e:
            # Right now all this does is log the error, In future you should
            # figure out what kind of errors are thrown and modify this with a
            # Several exception block statement.
            logging.info("%s", e)
            status = calculator_pb2.LOGIN_ERROR
        # Return the response
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
        status = 0
        jwt = ""
        refresh = ""
        try:
            if request.username == "" or request.password == "" or \
                    clh.verify_credentials():
                # User has provided illegal input or already exists
                status = calculator_pb2.ACCOUNT_CREATION_UNSUCCESSFUL
            # Username doesn't exist, create a new account and return a jwt and
            #   refresh token
            clh.create_new_account()
            jwt, refresh = clh.generate_jwt()
            status = calculator_pb2.ACCOUNT_CREATION_SUCCESSFUL
        except Exception as e:
            # Right now all this does is log the error, In future you should
            # figure out what kind of errors are thrown and modify this with a
            # Several exception block statement.
            logging.info("%s", e)
            status = calculator_pb2.ACCOUNT_CREATION_ERROR
        return calculator_pb2.LoginResponse(
            jwt=jwt,
            refresh=refresh,
            status=status
        )