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

        self._TOKEN_LIFETIME = 30
        self.timestamp = str(datetime.timestamp(datetime.now())).split('.')[0]

        ### Google Cloud Firestore
        self.firestoreClient = firestore.Client()
        self.usersRef = self.firestoreClient.collection(u'Users')

    def verify_credentials(self) -> bool:
        """ Verify the provided username and password """
        logging.info("  --- verify creds ---")
        verifyStatus = self.usersRef.document(u'{}'.format(self.username))\
                .get().exists
        logging.info("  Outcome: %r", verifyStatus)
        return verifyStatus

    def generate_jwt(self, GenRefresh: bool) -> (str,str):
        """ 
            Generates a JWT, returns a tuple containing the serialised JWT
            and the refresh token 
        """
        # Get the private key
        key, keyAsJSON = self._get_private_jwk()
        # Create the token
        token = jwt.JWT(
            header={
                "alg": "RS256",
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
        if GenRefresh:
            userRefresh = self._set_refresh_token()
        else:
            userRefresh = ""
        # Sign and serialize JWT
        token.make_signed_token(key)
        serial_token = token.serialize()

        # return newly created JWT and refresh token
        return serial_token, userRefresh
    
    def verify_jwt(self, inputJwt: str) -> bool:
        """
        Uses the 
        """
        key, keyAsJSON = self._get_private_jwk()
        try:
            # By default, if you provide a jwt string and a key, it will
            # Run the deserialise command
            jwt.JWT(jwt=inputJwt, key=key)
            # jwt.JWT.deserialize(jwt=inputJwt, key=key)
            return True
        except ValueError as e:
            # Happens when token is not of a known format
            print("Value error")
            print(e)
        except jwt.JWTMissingKey as e:
            # Happens when we are using a jey which is not part of the keyset
            print("Key missing error")
            print(e)
        except Exception as e:
            logging.info(e)
            return False
    
    def verify_refresh(self, refresh: str) -> bool:
        # Compare the refresh token listed in the database to the one provided
        logging.info("  --- Verify Refresh ---")
        userDoc = self.usersRef.document(u'{}'.format(self.username)).get()
        logging.info("  Document {} exists?: {}".format(self.username, userDoc.exists))
        if not userDoc.exists:
            # the provided username doesn't exist
            return False
        # Provided username exists
        logging.info("userDoc dict: {}".format(userDoc.to_dict()))
        logging.info("dict_refresh_token: {}, our Refresh: {}".format(userDoc.to_dict()[u'refreshToken'], refresh))
        if userDoc.to_dict()[u'refreshToken'] == refresh:
            # refresh token matches
            return True
        else:
            return False


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
    
    def terminate_account(self) -> bool:
        """
        Terminates the users account and all related information.
        """                                           
        try:
            self.usersRef.document(u'{}'.format(self.username)).delete()
            return True
        except Exception as e:
            logging.info("%s",e)
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
        refresh = str(uuid.uuid4())
        
        # Set the refresh token in the firestore (assumes document exists)
        # if the document doesn't exist, it will create a new document.
        self.usersRef.document(u'{}'.format(self.username)).set({
            u'refreshToken' : refresh
        }, merge=True )

        return refresh
