from typing import Text
from typing import Optional
import logging 

from google.cloud import storage, firestore
from jwcrypto import jwt, jwk
import json, uuid

import calculator_pb2
import calculator_pb2_grpc

from datetime import datetime

class Calculator_Login_Helper:
    def __init__(self, username: str, password: str) -> None:
        """ Initialises the class variables """
        self.username = username
        self.password = password

        ### Google Cloud Storage
        self.storageClient = storage.Client()
        # Whatever you named the bucket
        self.bucketName = 'cloud-training-bucket-69'
        self.privateKeyLocation = 'keys/cloud-training-PRIVATE-key.json'

        self._TOKEN_LIFETIME = 60*60
        self.timestamp = str(datetime.timestamp(datetime.now())).split('.')[0]

        ### Google Cloud Firestore
        self.firestoreClient = firestore.Client()
        self.usersRef = self.firestoreClient.collection(u'Users')

    def verify_credentials(self) -> bool:
        """ Verify the provided username and password """
        return self.usersRef.document(u'{}'.format(self.username)).get().\
                exists()

    def generate_jwt(self) -> (str,str):
        """ 
            Generates a JWT, returns a tuple containing the serialised JWT
            and the refresh token 
        """
        # Get the private key
        key, keyAsJSON = self._get_private_jwk()

        # Create the token
        token = jwt.JWT(
            header={
                "typ": "JWT",
                "kid": keyAsJSON["kid"]
            },
            claims= {
                "iss": "panzerkampfwagen-funf-ausfurung-D-Panther",
                "sub": self.username,
                "aud": ["customers"],
                "exp": int(self.timestamp) + self._TOKEN_LIFETIME,
                "iat": int(self.timestamp)
            }
        )
        
        # Generate the refresh token
        userRefresh = self._set_refresh_token()

        # Sign and serialize JWT
        token.make_signed_token(key)
        serial_token = token.serialize()

        # return newly created JWT and refresh token
        return serial_token, userRefresh

    def create_new_account(self) -> bool:
        """ 
        Creates a new account in the users database, upon success, the
        function will return True, otherwise will return false
        """
        try:
            # Create a new profile (assumes that none already exists)
            self.usersRef.document(u'{}'.format(self.username)).set({
                "profileVersion" : "1.0.0",
                "username" : self.username,
                "password" : self.password
            })
            return True
        except Exception as e:
            logging.info("%s", e)
            return False

    def _get_private_jwk(self) -> (object, dict):
        """ PRIVATE METHOD: Gets the private key from Google Storage """
        bucket = self.storageClient.bucket(self.bucketName)
        blob = bucket.blob(self.privateKeyLocation)
        keyAsJSON = json.loads(blob.download_as_string())
        # The double asterisk (**) is used to group all key value pairs into 
        # a single variable in python. This is particularly useful here.
        key = jwk.JWK(**keyAsJSON)
        return key, keyAsJSON

    def _set_refresh_token(self) -> str:
        """ Creates a refresh token and logs said refresh token to the users
            firestore account
        """
        # Generate the refresh token
        refresh = uuid.uuid4()
        
        # Set the refresh token in the firestore (assumes document exists)
        # if the document doesn't exist, it will create a new document.
        self.usersRef.document(u'{}'.format(self.username)).set({
            u'refreshToken' : refresh
        }, merge=True )

        return refresh
